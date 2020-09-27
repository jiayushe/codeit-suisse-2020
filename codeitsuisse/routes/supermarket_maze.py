import logging
from flask import request, jsonify
from codeitsuisse import app
from queue import Queue

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluateSupermarketMaze():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    result = {}
    for key, val in data['tests'].items():
        result[key] = solve(val['maze'], val['start'], val['end'])
    logging.info('my result: {}'.format(result))
    ret = {'answers': result}
    return jsonify(ret)

def solve(maze, start, end):
    rows = len(maze)
    cols = len(maze[0])
    ans = -1
    q = Queue(maxsize = 1000000)
    q.put((start[1], start[0], 1))
    while(not q.empty() and ans == -1):
        curr = q.get()
        x, y, cnt = curr
        maze[x][y] = '*'
        for dir in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            x2, y2, cnt2 = x + dir[0], y + dir[1], cnt + 1
            if x2 == end[1] and y2 == end[0]:
                ans = cnt2
                break
            if x2 < 0 or x2 >= rows or y2 < 0 or y2 >= cols:
                continue
            if maze[x2][y2] == 0:
                q.put((x2, y2, cnt + 1))
    return ans
