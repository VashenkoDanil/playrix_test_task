import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(dotenv_path=find_dotenv(), verbose=False, override=True)


URL_GITHUB_API = os.getenv('URL_GITHUB_API')
DEFAULT_BRANCH = os.getenv('DEFAULT_BRANCH')

URL_PATH_SEARCH_ISSUES = os.getenv('URL_PATH_SEARCH_ISSUES')
URL_PATH_REPOSITORIES_COMMITS = os.getenv('URL_PATH_REPOSITORIES_COMMITS')
