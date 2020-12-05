import sys
from argparse import ArgumentParser
from datetime import datetime
from typing import Dict

from exceptions import InvalidDateFormatError
from settings import DEFAULT_BRANCH


def parser_date(date: str) -> datetime:
    try:
        return datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        raise InvalidDateFormatError(f'Неверный формат даты: {date} (Пример: 05.12.2020)')


def create_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument('-u', '--url', type=str, required=True, help='URL публичного репозитория на github.com.')
    parser.add_argument('-s', '--start_date', default=None, type=parser_date, help='Дата начала анализа.')
    parser.add_argument('-e', '--end_date', default=None, type=parser_date, help='Дата окончания анализа.')
    parser.add_argument('-b', '--branch', default=DEFAULT_BRANCH, type=str, help='Ветка репозитория.')
    return parser


def get_params() -> Dict[str, any]:
    parser = create_parser()
    arguments = parser.parse_args(sys.argv[1:])
    return {
        'url_public_repository': arguments.url,
        'start_date_analysis': arguments.start_date,
        'end_date_analysis': arguments.end_date,
        'branch_repository': arguments.branch,
    }
