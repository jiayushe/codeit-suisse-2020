import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    result = solve(data)
    logging.info('my result: {}'.format(result))
    return jsonify(str(result))

def solve(data):
    weight = {}
    weight['maApple'] = 50
    weight['maBanana'] = 50
    weight['maWatermelon'] = 50

    ans = 0
    for fruit in data:
        ans += weight[fruit] * data[fruit]

    return ans
