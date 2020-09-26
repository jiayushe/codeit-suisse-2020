import logging
from flask import request, jsonify
from codeitsuisse import app
import ast

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluateFruitBasket():
    data = ast.literal_eval((request.get_data()).decode('UTF-8'));
    logging.info('data sent for evaluation: {}'.format(data))
    result = solve(data)
    logging.info('my result: {}'.format(result))
    return jsonify(str(result))

def solve(data):
    weight = {}
    weight['maApple'] = 50
    weight['maAvocado'] = 40
    weight['maBanana'] = 20
    weight['maPineapple'] = 50
    weight['maPomegranate'] = 40
    weight['maRamubutan'] = 50
    weight['maWatermelon'] = 60

    ans = 0
    for fruit in data:
        try:
            ans += weight[fruit] * data[fruit]
        except KeyError:
            continue

    return 0
