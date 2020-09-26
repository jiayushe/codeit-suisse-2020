import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluateSaladSpree():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    n = data.get('number_of_salads')
    arr_of_arr = data.get('salad_prices_street_map')
    INF = 100000000000
    result = INF
    for arr in arr_of_arr:
        int_arr = []
        for val in arr:
            if val == 'X':
                int_arr.append(INF)
            else:
                int_arr.append(int(val))
        result = min(result, getMinCost(int_arr, n))
    if result == INF:
        result = 0    
    logging.info('my result: {}'.format(result))
    ret = {'result': result}
    return jsonify(ret)

def getMinCost(arr, n):
    curr = sum(arr[:n])
    best = curr
    i = n
    while i < len(arr):
        curr = curr + arr[i] - arr[i - n]
        best = min(best, curr)
        i += 1
    return best
