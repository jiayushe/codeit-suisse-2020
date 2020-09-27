import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

memoized = {}

@app.route('/yin-yang', methods=['POST'])
def evaluateYinYang():
    global memoized
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    numElem = data['number_of_elements']
    numOp = data['number_of_operations']
    elements = data['elements']
    memoized = {}
    result = solve(numElem, numOp, elements)
    logging.info('my result: {}'.format(result))
    ret = {'result': result}
    return jsonify(ret)

def solve(numElem, numOp, elements):
    global memoized
    if elements in memoized and numElem in memoized[elements]:
        return memoized[elements][numElem][numOp]
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
    if not elements in memoized:
        memoized[elements] = {}
    if not numElem in memoized[elements]:
        memoized[elements][numElem] = {}
    memoized[elements][numElem][numOp] = ans
    return ans   
