import logging
from flask import request, jsonify
from codeitsuisse import app
import sys
from functools import lru_cache

sys.setrecursionlimit(100000)
logger = logging.getLogger(__name__)

@app.route('/yin-yang', methods=['POST'])
def evaluateYinYang():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    numElem = data['number_of_elements']
    numOp = data['number_of_operations']
    elements = data['elements']
    result = solve(numElem, numOp, elements)
    logging.info('my result: {}'.format(result))
    ret = {'result': result}
    return jsonify(ret)

@lru_cache(maxsize=None)
def solve(numElem, numOp, elements):
    if numOp == 0:
        return 0
    if numElem == 1:
        return 1 if elements[0] == 'Y' else 0
    ans = 0
    for i in range(numElem // 2):
        elementsLeft = elements[:i] + elements[i + 1:]
        solvedLeft = solve(numElem - 1, numOp - 1, elementsLeft)
        if elements[i] == 'Y':
            solvedLeft += 1
        elementsRight = elements[:numElem - i - 1] + elements[numElem - i:]
        solvedRight = solve(numElem - 1, numOp - 1, elementsRight)
        if elements[numElem - i - 1] == 'Y':
            solvedRight += 1
        ans += max(solvedLeft, solvedRight) * 2 / numElem
    if numElem % 2 == 1:
        idx = numElem // 2
        elementsMid = elements[:idx] + elements[idx + 1:]
        solvedMid = solve(numElem - 1, numOp - 1, elementsMid)
        if elements[idx] == 'Y':
            solvedMid += 1
        ans += solvedMid / numElem
    return ans   
