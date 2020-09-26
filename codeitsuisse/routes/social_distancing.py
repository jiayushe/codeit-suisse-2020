import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluateSocialDistancing():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    tests = data.get('tests')
    result = {}
    for key, val in tests.items():
        ans = solve(val['seats'], val['people'], val['spaces'])
        result[key] = ans
    logging.info('my result: {}'.format(result))
    ret = {'answers': result}
    return jsonify(ret)

def solve(seats, people, spaces):
    l = max(seats, people) + 1

    # init
    table = [[0 for j in range(l)] for i in range(l)]
    for i in range(seats + 1):
        table[i][1] = i

    # dp
    for i in range(spaces + 2, seats + 1):
        for j in range(2, people + 1):
            table[i][j] = table[i - 1][j] + table[i - 1 - spaces][j - 1]

    return table[seats][people]   
