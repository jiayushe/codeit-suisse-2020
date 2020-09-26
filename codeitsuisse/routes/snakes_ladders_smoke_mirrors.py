import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

board = []

@app.route('/slsm', methods=['POST'])
def evaluateSnakesLaddersSmokeMirrors():
    global board
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    boardSize = data["boardSize"]
    players = data["players"]
    jumps = data["jumps"]
    board = [('*', 0) for i in range(boardSize + 1)]
    for jump in jumps:
        arr = jump.split(':')
        first, second = int(arr[0]), int(arr[1])
        if first == 0:
            board[second] = ('mirror', 0)
        elif second == 0:
            board[first] = ('smoke', 0)
        elif first < second:
            board[first] = ('ladder', second)
        else:
            board[first] = ('snake', second)
    result = solve(boardSize, players)
    logging.info('my result: {}'.format(result))
    return jsonify(result)

def solve(boardSize, players):
    rolls = []
    currPos = 1
    while boardSize - currPos > 6:
        nextRolls, nextPos = getNext(currPos)
        for i in range(players):
            rolls += nextRolls
        currPos = nextPos
    if boardSize - currPos == 1:
        rolls += [2 for i in range(players - 1)]
    else:
        rolls += [1 for i in range(players - 1)]
    rolls.append(boardSize - currPos)
    return rolls

def getNext(currPos):
    rolls = []
    maxPos = 0
    for move in range(1, 7):
        nextPos = currPos + move
        cell = board[nextPos]
        if cell[0] == '*':
            if nextPos > maxPos:
                maxPos = nextPos
                rolls = [move]
        elif cell[0] == 'ladder' or cell[0] == 'snake':
            if cell[1] > maxPos:
                maxPos = cell[1]
                rolls = [move]
    return rolls, maxPos
