import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

map1 = {}
result = []
infectedName = ''
originName = ''

@app.route('/contact_trace', methods=['POST'])
def evaluateContactTrace():
    global map1
    map1 = {}
    global result
    result = []
    global infectedName
    global originName
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    infected = data.get('infected')
    infectedName = infected['name']
    map1[infected['name']] = infected['genome']
    origin = data.get('origin')
    originName = origin['name']
    map1[origin['name']] = origin['genome']
    cluster = data.get('cluster')
    for c in cluster:
        map1[c['name']] = c['genome']
    trace(infectedName, [infectedName], [])
    logging.info('my result: {}'.format(result))
    return jsonify(result)

def trace(currName, traceArr, specArr):
    currGenome = map1[currName]

    if currName != infectedName and currGenome == map1[originName]:
        result.append(getStr(traceArr, specArr))
        return
    
    INF = 1000000000
    bestTotalDiff = INF
    bestHeadDiff = []
    bestName = []

    for name, genome in map1.items():
        if name in traceArr:
            continue
        currDiff = getDiff(genome, currGenome)
        if currDiff[0] < bestTotalDiff:
            bestTotalDiff = currDiff[0]
            bestHeadDiff = [currDiff[1]]
            bestName = [name]
        elif currDiff[0] == bestTotalDiff:
            bestHeadDiff.append(currDiff[1])
            bestName.append(name)
    
    for i in range(len(bestName)):
        nextName = bestName[i]
        nextTraceArr = traceArr + [nextName]
        nextSpec = 1 if bestHeadDiff[i] > 1 else 0
        nextSpecArr = specArr + [nextSpec]
        trace(nextName, nextTraceArr, nextSpecArr)

def getDiff(g1, g2):
    totalDiff = 0
    headDiff = 0
    i = 0
    while i < len(g1):
        if g1[i] != g2[i]:
            totalDiff += 1
            headDiff += 1
        if g1[i + 1] != g2[i + 1]:
            totalDiff += 1
        if g1[i + 2] != g2[i + 2]:
            totalDiff += 1
        i += 4
    return totalDiff, headDiff

def getStr(traceArr, specArr):
    ans = infectedName
    for i in range(len(specArr)):
        if specArr[i] == 1:
            ans += '*'
        ans += ' -> '
        ans += traceArr[i + 1]
    return ans
