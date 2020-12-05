from datetime import datetime

from main import count_pull_requests, count_old_pull_requests, count_issues, count_old_issues
import requests_mock


def test_count_pull_requests(capsys):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/search/issues?q=state:open+is:pr+base:master+created:2020-01-01..2020-12-31+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        m.get('https://api.github.com/search/issues?q=state:closed+is:pr+base:master+created:2020-01-01..2020-12-31+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        count_pull_requests('https://github.com/fastlane/fastlane/',
                            datetime(2020, 1, 1),
                            datetime(2020, 12, 31),
                            'master')
    captured = capsys.readouterr()
    assert captured.out == 'Количество открытых pull requests = 5\nКоличество закрытых pull requests = 5\n'


def test_count_old_pull_requests(capsys):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/search/issues?q=state:open+is:pr+base:master+created:2020-01-01..2020-11-05+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        count_old_pull_requests('https://github.com/fastlane/fastlane/',
                                datetime(2020, 1, 1),
                                datetime(2020, 12, 31),
                                'master')
    captured = capsys.readouterr()
    assert captured.out == 'Количество старых pull requests = 5\n'


def test_count_issues(capsys):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/search/issues?q=state:open+is:issue+created:2020-01-01..2020-12-31+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        m.get('https://api.github.com/search/issues?q=state:closed+is:issue+created:2020-01-01..2020-12-31+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        count_issues('https://github.com/fastlane/fastlane/',
                     datetime(2020, 1, 1),
                     datetime(2020, 12, 31))
    captured = capsys.readouterr()
    assert captured.out == 'Количество открытых issue = 5\nКоличество закрытых issue = 5\n'


def test_count_old_issues(capsys):
    with requests_mock.Mocker() as m:
        m.get('https://api.github.com/search/issues?q=state:open+is:issue+created:2020-01-01..2020-11-21+'
              'repo:fastlane/fastlane', status_code=200, json={'total_count': 5})
        count_old_issues('https://github.com/fastlane/fastlane/',
                         datetime(2020, 1, 1),
                         datetime(2020, 12, 31))
    captured = capsys.readouterr()
    assert captured.out == 'Количество старых issue = 5\n'
