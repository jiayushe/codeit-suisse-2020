import logging
from flask import request, jsonify
from codeitsuisse import app
import math

logger = logging.getLogger(__name__)

INF = 1000000000
EPS = 0.00000001

class point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __le__(self, other):
        return (self.x, self.y) <= (other.x, other.y)

    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)

    def __ge__(self, other):
        return (self.x, self.y) >= (other.x, other.y)

    def __eq__(self, other):
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

class line:
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.start = point()
        self.end = point()

def pointsToLine(p1, p2, l):
    l.start = min(p1, p2)
    l.end = max(p1, p2)
    if abs(p1.x - p2.x) < EPS:
        l.a, l.b, l.c = 1.0, 0.0, -p1.x
    else:
        a = -(p1.y - p2.y) / (p1.x - p2.x)
        l.a, l.b, l.c = a, 1.0, -(a * p1.x) - p1.y

def areParallel(l1, l2):
    return math.isclose(l1.a, l2.a) and math.isclose(l1.b, l2.b)

def areIntersect(l1, l2, p):
    if areParallel(l1, l2):
        return False
    p.x = (l2.b * l1.c - l1.b * l2.c) / (l2.a * l1.b - l1.a * l2.b)
    if not math.isclose(l1.b, 0.0):
        p.y = -(l1.a * p.x + l1.c)
    else:
        p.y = -(l2.a * p.x + l2.c)
    return True

@app.route('/revisitgeometry', methods=['POST'])
def evaluateRevisitGeometry():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    # get shape
    shapeCoordinates = data.get('shapeCoordinates')
    n = len(shapeCoordinates)
    shapePoints = []
    for c in shapeCoordinates:
        shapePoints.append(point(c['x'], c['y']))
    shapeLines = []
    for i in range(n):
        newLine = line()
        p1 = shapePoints[i]
        p2 = shapePoints[i + 1] if i < n - 1 else shapePoints[0]
        pointsToLine(p1, p2, newLine)
        shapeLines.append(newLine)
    # get line
    lineCoordinates = data.get('lineCoordinates')
    linePoints = []
    for c in lineCoordinates:
        linePoints.append(point(c['x'], c['y']))
    lineLine = line()
    pointsToLine(linePoints[0], linePoints[1], lineLine)
    # get intersects
    intersects = []
    for l in shapeLines:
        intersect = point()
        if areIntersect(l, lineLine, intersect) and intersect >= l.start and intersect <= l.end:
            # prevent duplicates
            gd = True
            for other in intersects:
                if other == intersect:
                    gd = False
                    break
            if gd:
                intersects.append(intersect)
    result = []
    for intersect in intersects:
        result.append({'x': intersect.x, 'y': intersect.y})
    logging.info('my result: {}'.format(result))
    return jsonify(result)
