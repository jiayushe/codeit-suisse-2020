import logging
from flask import request, jsonify
from codeitsuisse import app
from queue import Queue

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluateCluster():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    result = solve(data)
    logging.info('my result: {}'.format(result))
    ret = {'answer': result}
    return jsonify(ret)

def solve(grid):
    rows = len(grid)
    cols = len(grid[0])
    ans = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                ans += 1
                flood(grid, i, j, rows, cols)
    return ans

def flood(grid, r, c, rows, cols):
    q = Queue(maxsize = 1000000)
    q.put((r, c))

    while(not q.empty()):
        curr = q.get()
        x, y = curr
        grid[x][y] = '*'
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x2, y2 = x + i, y + j
                if x2 < 0 or x2 >= rows or y2 < 0 or y2 >= cols:
                    continue
                if grid[x2][y2] != '*':
                    q.put((x2, y2))
