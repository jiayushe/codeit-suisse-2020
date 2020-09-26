import logging
from flask import request, jsonify
from codeitsuisse import app
import ast

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = ast.literal_eval((request.get_data()).decode('UTF-8'))
    logging.info('data sent for evaluation: {}'.format(data))
    result = solve(data)
    logging.info('my result: {}'.format(result))
    return jsonify(str(result))

def solve(data):
    weight = {}
    weight['maApple'] = 40
    weight['maAvocado'] = 41
    weight['maPineapple'] = 15
    weight['maPomegranate'] = 67
    weight['maRamubutan'] = 69
    weight['maWatermelon'] = 92

    ans = 0
    for fruit in data:
        try:
            ans += weight[fruit] * data[fruit]
        except KeyError:
            continue

    return ans
