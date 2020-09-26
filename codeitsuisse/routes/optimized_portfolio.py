import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])
def evaluateOptimizedPortfolio():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    result = []
    for test in data['inputs']:
        result.append(solve(test))
    logging.info('my result: {}'.format(result))
    ret = {'outputs': result}
    return jsonify(ret)

def solve(test):
    portfolio = test['Portfolio']
    indexFutures = test['IndexFutures']
    res = []
    for indexFuture in indexFutures:
        optimalHedgeRatio = indexFuture['CoRelationCoefficient'] * portfolio['SpotPrcVol'] / indexFuture['FuturePrcVol']
        futuresContractSize = indexFuture['IndexFuturePrice'] * indexFuture['Notional']
        numFuturesContract = round(optimalHedgeRatio, 3) * portfolio['Value'] / futuresContractSize
        res.append({
            'FuturePrcVol': indexFuture['FuturePrcVol'],
            'HedgePositionName': indexFuture['Name'],
            'OptimalHedgeRatio': round(optimalHedgeRatio, 3),
            'NumFuturesContract': round(numFuturesContract)
        })
    res.sort(key=lambda x: x['NumFuturesContract'])
    res.sort(key=lambda x: x['FuturePrcVol'])
    res.sort(key=lambda x: x['OptimalHedgeRatio'])
    ans = res[0]
    ans.pop('FuturePrcVol', None)
    return ans
