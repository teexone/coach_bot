import requests, json, pandas
from pandas import DataFrame

request_url_prefix = "https://codeforces.com/api/"
problems = pandas.DataFrame()


def __static_init__():
    global problems
    problems = pandas.DataFrame(pandas.read_json(json.dumps(requests.get(request_url_prefix + "problemset.problems").json()['result']['problems'])))


def get_all_problems() -> DataFrame:
    return problems


def get_user_submission(handle):
    return pandas.DataFrame(pandas.read_json(
        json.dumps(requests.get(request_url_prefix + "user.status?handle="+handle).json()['result'])))

