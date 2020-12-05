from helpers import get_arguments
from service.github_api import MostActiveParticipant, CountPullRequests, CountIssues
from datetime import datetime

from settings import DEFAULT_BRANCH


def most_active_participant(url_public_repository: str,
                            start_date_analysis: datetime,
                            end_date_analysis: datetime,
                            branch_repository: str = DEFAULT_BRANCH) -> None:
    MostActiveParticipant(url_public_repository=url_public_repository,
                          start_date_analysis=start_date_analysis,
                          end_date_analysis=end_date_analysis,
                          branch_repository=branch_repository)()


def count_pull_requests(url_public_repository: str,
                        start_date_analysis: datetime,
                        end_date_analysis: datetime,
                        branch_repository: str = DEFAULT_BRANCH) -> None:
    CountPullRequests(url_public_repository=url_public_repository,
                      start_date_analysis=start_date_analysis,
                      end_date_analysis=end_date_analysis,
                      branch_repository=branch_repository).count_open_and_closed_pr()


def count_old_pull_requests(url_public_repository: str,
                            start_date_analysis: datetime,
                            end_date_analysis: datetime,
                            branch_repository: str = DEFAULT_BRANCH) -> None:
    CountPullRequests(url_public_repository=url_public_repository,
                      start_date_analysis=start_date_analysis,
                      end_date_analysis=end_date_analysis,
                      branch_repository=branch_repository).count_old_pr()


def count_issues(url_public_repository: str,
                 start_date_analysis: datetime,
                 end_date_analysis: datetime,
                 **kwargs) -> None:
    CountIssues(url_public_repository=url_public_repository,
                start_date_analysis=start_date_analysis,
                end_date_analysis=end_date_analysis).count_open_and_closed_issue()


def count_old_issues(url_public_repository: str,
                     start_date_analysis: datetime,
                     end_date_analysis: datetime,
                     **kwargs) -> None:
    CountIssues(url_public_repository=url_public_repository,
                start_date_analysis=start_date_analysis,
                end_date_analysis=end_date_analysis).count_old_issue()


if __name__ == '__main__':
    arguments = get_arguments()

    most_active_participant(**arguments)
    count_pull_requests(**arguments)
    count_old_pull_requests(**arguments)
    count_issues(**arguments)
    count_old_issues(**arguments)
