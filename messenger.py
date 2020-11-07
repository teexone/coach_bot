def get_emoji(complexity):
    complexity = int(complexity)
    if complexity < 1200:
        return u'\U0001F4D7'
    elif complexity < 1600:
        return u'\U0001F4D2'
    elif complexity < 2000:
        return u'\U0001F4D9'
    else:
        return u'\U0001F4D5'


def problem_info(problem):
    e = get_emoji(problem['rating']) + ' '
    text = e + str(problem['contestId']) + str(problem['index']) + '. ' + \
           str(problem['name']) + '\n' + e + \
           'Problem link: [%s%s](https://codeforces.com/problemset/problem/%s/%s)\n' \
           % (str(problem['contestId']), str(problem['index']), str(problem['contestId']),
              str(problem['index'])) + e + 'Complexity: %s' \
           % str(int(problem['rating'])) + '\n\n'
    return text
