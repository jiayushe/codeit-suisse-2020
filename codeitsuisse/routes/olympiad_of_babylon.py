import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluateOlympiadOfBabylon():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    books = data['books']
    days = data['days']
    result = solve(days, books)
    logging.info('my result: {}'.format(result))
    ret = {'optimalNumberOfBooks': result}
    return jsonify(ret)

def solve(days, books):
    ans = 0
    # start from the day with least remaining time
    days.sort()
    for remain in days:
        # init
        # table[idx][remain] = (cnt, data)
        table = {}
        for idx in range(len(books) + 1):
            table[idx] = {}
        table[0][remain] = (0, [])

        # dp
        for idx, needed in enumerate(books):
            idx += 1
            for prevIdx in range(idx):
                for prevRemain in table[prevIdx]:
                    prevCnt, prevData = table[prevIdx][prevRemain]
                    currRemain = prevRemain - needed
                    if currRemain < 0:
                        continue
                    if currRemain not in table[idx]:
                        table[idx][currRemain] = (prevCnt + 1, prevData + [idx - 1])
                    elif prevCnt + 1 > table[idx][currRemain][0]:
                        table[idx][currRemain] = (prevCnt + 1, prevData + [idx - 1])

        INF = 10000
        maxCnt = 0
        maxData = []
        minRemain = INF
        for idx in table:
            for remain in table[idx]:
                cnt = table[idx][remain][0]
                if cnt > maxCnt:
                    maxCnt = cnt
                    minRemain = remain
                    maxData = table[idx][remain][1]
                elif cnt == maxCnt and remain < minRemain:
                    minRemain = remain
                    maxData = table[idx][remain][1]
        ans += maxCnt

        newBooks = []
        iter = 0
        for idx, needed in enumerate(books):
            if iter < len(maxData) and idx == maxData[iter]:
                iter += 1
            else:
                newBooks.append(needed)
        books = newBooks

    return ans
