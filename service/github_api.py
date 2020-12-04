import datetime
from collections import OrderedDict
from typing import Dict

import requests

from exceptions import RequestLimitExceededError, UnknownResponseCodeError, UnknownErrorWhenRequestError
from settings import URL_GITHUB_API, DEFAULT_BRANCH


class Base:
    url_github_api: str = URL_GITHUB_API
    url_public_repository: str = None
    start_date_analysis: datetime.datetime = None
    end_date_analysis: datetime.datetime = None
    repository_name: str = None

    def __init__(self, *args, **kwargs):
        self.url_public_repository = kwargs.get('url_public_repository')
        self.start_date_analysis = kwargs.get('start_date_analysis')
        self.end_date_analysis = kwargs.get('end_date_analysis')
        self.repository_name = '/'.join(self.url_public_repository.split('/')[3:5])

    def get_requests(self, url: str, params: Dict = None):
        try:
            response = requests.get(url=url, params=params)
        except Exception as e:
            raise UnknownErrorWhenRequestError(f'Неизвестная ошибка при запросе. url{url}, param:{params}, error:{e}')

        if response.status_code == 200:
            return response
        elif response.status_code == 403 and 'API rate limit exceeded' in response.json()['message']:
            raise RequestLimitExceededError('Превышен лимит запросов к github api')
        raise UnknownResponseCodeError(f'Получен не известный код ответа от github api. '
                                       f'status_code:{response.status_code}, message{response.json()["message"]}')

    def get_query_params(self, *args, **kwargs):
        params = [
            f'{i}:{j}' for i, j in kwargs.items()
        ]

        if self.repository_name:
            params.append(f'repo:{self.repository_name}')

        return '?q=' + '+'.join(params)

    def get_start_date_analysis(self):
        if self.start_date_analysis:
            return self.start_date_analysis.strftime("%Y-%m-%d")
        return '*'

    def get_end_date_analysis(self):
        if self.end_date_analysis:
            return self.end_date_analysis.strftime("%Y-%m-%d")
        return '*'


class MostActiveParticipant(Base):
    url_path: str
    branch_repository: str = DEFAULT_BRANCH

    def __init__(self, *args, **kwargs):
        if kwargs.get('branch_repository'):
            self.branch_repository = kwargs.pop('branch_repository')
        super().__init__(*args, **kwargs)
        self.url_path = f'/repos/{self.repository_name}/commits'

    def __call__(self, *args, **kwargs):
        active_participants = self._get_list_active_participants()
        for participant, count_comment in active_participants.items():
            print(participant, count_comment)

    def _get_url(self) -> str:
        return self.url_github_api + self.url_path

    def _get_params(self) -> Dict:
        params = {
            'sha': self.branch_repository,
            'per_page': 100,
        }
        since, until = self.get_start_date_analysis(), self.get_end_date_analysis()
        if since and since != '*':
            params.update({'since': since})
        if until and until != '*':
            params.update({'until': until})
        return params

    def _get_list_active_participants(self) -> Dict:
        response = self.get_requests(url=self._get_url(), params=self._get_params())
        commits = response.json()
        while response.links.get('next'):
            response = self.get_requests(url=response.links['next']['url'])
            commits += response.json()

        participants = {}
        count_no_login_author = 0
        for commit in commits:
            try:
                participants[commit['author']['login']] += 1
            except KeyError:
                participants[commit['author']['login']] = 1
            except TypeError:
                count_no_login_author += 1
        if count_no_login_author:
            participants.update({'Коммиты без логина': count_no_login_author})
        return OrderedDict(sorted(participants.items(), key=lambda item: item[1], reverse=True)[:30])


class CountPullRequests(Base):
    url_path: str = '/search/issues'
    branch_repository: str = DEFAULT_BRANCH

    def __init__(self, *args, **kwargs):
        self.branch_repository = kwargs.pop('branch_repository')
        super().__init__(*args, **kwargs)

    def count_old_pr(self):
        query_params = {
            'state': 'open',
            'is': 'pr',
            'base': self.branch_repository,
            'created': f'{self.get_start_date_analysis()}..{self._get_old_end_date_analysis()}'
        }
        count_old_pr = self._get_count_pull_requests(query_params=query_params)
        print('Количество старых pull requests =', count_old_pr)

    def count_open_and_closed_pr(self):
        count_open_pr = self._get_count_pull_requests(query_params=self._get_query_params_for_count_open_pr())
        count_closed_pr = self._get_count_pull_requests(query_params=self._get_query_params_for_count_closed_pr())
        print('Количество открытых pull requests =', count_open_pr)
        print('Количество закрытых pull requests =', count_closed_pr)

    def _get_query_params_for_count_open_pr(self) -> Dict:
        return {
            'state': 'open',
            'is': 'pr',
            'base': self.branch_repository,
            'created': f'{self.get_start_date_analysis()}..{self.get_end_date_analysis()}'
        }

    def _get_query_params_for_count_closed_pr(self) -> Dict:
        return {
            'state': 'closed',
            'is': 'pr',
            'base': self.branch_repository,
            'created': f'{self.get_start_date_analysis()}..{self.get_end_date_analysis()}'
        }

    def _get_url(self, query_params) -> str:
        return self.url_github_api + self.url_path + self.get_query_params(**query_params)

    def _get_old_end_date_analysis(self) -> str:
        old_date = datetime.datetime.now() - datetime.timedelta(days=30)
        if self.end_date_analysis and self.end_date_analysis < old_date:
            return self.end_date_analysis.strftime("%Y-%m-%d")
        return old_date.strftime("%Y-%m-%d")

    def _get_count_pull_requests(self, query_params: Dict) -> int:
        response = self.get_requests(self._get_url(query_params)).json()
        return int(response['total_count'])


class CountIssues(Base):
    url_path = '/search/issues'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def count_old_issue(self):
        query_params = {
            'state': 'open',
            'is': 'issue',
            'created': f'{self.get_start_date_analysis()}..{self._get_old_end_date_analysis()}'
        }
        count_old_pr = self._get_count_pull_requests(query_params=query_params)
        print('Количество старых issue =', count_old_pr)

    def count_open_and_closed_issue(self):
        count_open_issue = self._get_count_pull_requests(query_params=self._get_query_params_for_count_open_issue())
        count_closed_issue = self._get_count_pull_requests(query_params=self._get_query_params_for_count_closed_issue())
        print('Количество открытых issue =', count_open_issue)
        print('Количество закрытых issue =', count_closed_issue)

    def _get_query_params_for_count_open_issue(self) -> Dict:
        return {
            'state': 'open',
            'is': 'issue',
            'created': f'{self.get_start_date_analysis()}..{self.get_end_date_analysis()}'
        }

    def _get_query_params_for_count_closed_issue(self) -> Dict:
        return {
            'state': 'closed',
            'is': 'issue',
            'created': f'{self.get_start_date_analysis()}..{self.get_end_date_analysis()}'
        }

    def _get_url(self, query_params) -> str:
        return self.url_github_api + self.url_path + self.get_query_params(**query_params)

    def _get_old_end_date_analysis(self) -> str:
        old_date = datetime.datetime.now() - datetime.timedelta(days=14)
        if self.end_date_analysis and self.end_date_analysis < old_date:
            return self.end_date_analysis.strftime("%Y-%m-%d")
        return old_date.strftime("%Y-%m-%d")

    def _get_count_pull_requests(self, query_params: Dict) -> int:
        response = self.get_requests(self._get_url(query_params)).json()
        return int(response['total_count'])
