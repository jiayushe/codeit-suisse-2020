import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/intelligent-farming', methods=['POST'])
def evaluateIntelligentFarming():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    runId = data.get('runId')
    tests = data.get('list')
    result = []
    for test in tests:
        id = test['id']
        s = test['geneSequence']
        ans = solve(s)
        result.append({'id': id, 'geneSequence': ans})
    logging.info('my result: {}'.format(result))
    ret = {'runId': runId, 'list': result}
    return jsonify(ret)

def solve(s):
    cnt = {}
    cnt['A'], cnt['C'], cnt['G'], cnt['T'] = 0, 0, 0, 0
    for c in s:
        cnt[c] += 1
    # get ACGT, CC, A, C, G, T
    acgt = min(cnt['A'], cnt['C'], cnt['G'], cnt['T'])
    if (cnt['C'] - acgt) % 2 == 1 and acgt > 0:
        acgt -= 1
    cc = (cnt['C'] - acgt) // 2
    c = (cnt['C'] - acgt) % 2
    a, g, t = cnt['A'] - acgt, cnt['G'] - acgt, cnt['T'] - acgt
    # get AACGT from A and ACGT
    aacgt = min(a, acgt)
    a -= aacgt
    acgt -= aacgt
    # store all other good strings
    others = []
    while cc > 0:
        others.append('CC')
        cc -= 1
    while c > 0:
        others.append('C')
        c -= 1
    while g > 0:
        others.append('G')
        g -= 1
    while t > 0:
        others.append('T')
        t -= 1
    # start with AACGT
    ans = 'AACGT' * aacgt
    # insert A together with good strings
    idx = 0
    while a > 0 and idx < len(others):
        nx = min(a, 2)
        a -= nx
        ans += 'A' * nx
        ans += others[idx]
        idx += 1
    # concat remaining good strings
    while idx < len(others):
        ans += others[idx]
        idx += 1
    # concat remaining ACGT
    ans += 'ACGT' * acgt
    # concat remaining A
    ans += 'A' * a

    return ans
