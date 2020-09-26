import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluateCleanFloor():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    tests = data.get('tests')
    result = {}
    for key, val in tests.items():
        ans = solve(val['floor'])
        result[key] = ans
    logging.info('my result: {}'.format(result))
    ret = {'answers': result}
    return jsonify(ret)

def solve(arr):
    ans = 0
    left = sum(arr)
    l = len(arr)
    i = 0
    while i < l:
        if i == l - 1:
            # last floor
            # resolve by itself
            curr = arr[i]
            ans += 2 * curr
            arr[i] -= curr
            left -= curr
            if curr % 2 == 1:
                ans += 1
            break
        if arr[i] + 1 <= arr[i + 1]:
            curr = arr[i]
            ans += 2 * curr + 1
            arr[i] -= curr
            arr[i + 1] -= curr + 1
            left -= 2 * curr + 1
            # early exit
            if left == 0:
                break
            i += 1
        else:
            curr = arr[i + 1]
            ans += 2 * curr
            arr[i] -= curr
            arr[i + 1] -= curr
            left -= 2 * curr
            # early exit
            if left == 0:
                break
            # resolve by itself
            curr = arr[i]
            ans += 2 * curr
            arr[i] -= curr
            left -= curr
            if curr % 2 == 1:
                ans += 1
            # early exit
            if left == 0:
                break
            # if current floor is even, we need to take another step to next floor
            if curr % 2 == 0:
                ans += 1
                arr[i + 1] += 1
            i += 1
 
    return ans
