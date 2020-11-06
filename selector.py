import pandas
import cf
import random

cf.__static_init__()


class TagCompare:
    tags = []

    def isin(self, other: list):
        ret = True
        for tag in self.tags:
            ret = ret and tag in other
        return ret

    def __init__(self, tags):
        self.tags = tags


def get_problem_by_complexity(min_c, max_c) -> pandas.DataFrame:
    return cf.get_all_problems().query(str(min_c) + ' <= ' + 'rating <=' + str(max_c))


def get_solved_problems(handle):
    qframe = cf.get_user_submission(handle)
    qframe.query('verdict == "ACCEPTED"')
    return qframe


def fetch_problems(quant, difficulty, tags=None, unsolved_by=None):
    if tags is None:
        tags = []
    q_frame = get_problem_by_complexity(difficulty[0], difficulty[1])
    if unsolved_by is not None:
        qsolved = get_solved_problems(unsolved_by)
        contest_id, index = [], []
        for i in qsolved.to_dict('index').values():
            if 'contestId' in i['problem']:
                contest_id.append(i['problem']['contestId'])
                index.append(i['problem']['index'])

        q_frame = q_frame.query('contestId not in @contest_id | index not in @index')
    tag_sorted = []
    if len(tags) >= 1 and tags[0] != ['*']:
        for tag in tags:
            comparator = TagCompare(tag)
            tag_sorted.append(q_frame.loc[q_frame['tags'].apply(lambda el: comparator.isin(el))])
    if len(tag_sorted) != 0:
        q_frame = pandas.concat(tag_sorted)
    ln = len(q_frame)
    return q_frame.iloc[random.sample(range(ln), k=min(ln, int(quant)))].to_dict('index') if ln else None
