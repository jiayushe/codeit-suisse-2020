import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluateInventoryManagement():
    data = request.get_json()
    logging.info('data sent for evaluation: {}'.format(data))
    result = []
    for test in data:
        target = test['searchItemName']
        items = test['items']
        ans = solve(target, items)
        result.append({'searchItemName': target, 'searchResult': ans})
    logging.info('my result: {}'.format(result))
    return jsonify(result)

def solve(target, items):
    ans = {}
    str_ans = {}
    for item in items:
        l1 = len(target)
        l2 = len(item)
        l = max(l1, l2) + 1
        
        # init
        table = [[0 for j in range(l)] for i in range(l)]
        for i in range(1, l1 + 1):
            table[i][0] = i * 1
        for j in range(1, l2 + 1):
            table[0][j] = j * 1
        str_table = [['' for j in range(l)] for i in range(l)]
        for i in range(1, l1 + 1):
            str_table[i][0] = str_table[i - 1][0] + '-' + target[i - 1]
        for j in range(1, l2 + 1):
            str_table[0][j] = str_table[j - 1][0] + '+' + item[j - 1]

        # dp
        for i in range(1, l1 + 1):
            for j in range(1, l2 + 1):
                # replace
                if target[i - 1].lower() == item[j - 1].lower():
                    table[i][j] = table[i - 1][j - 1]
                    str_table[i][j] = str_table[i - 1][j - 1] + target[i - 1]
                else:
                    table[i][j] = table[i - 1][j - 1] + 1
                    str_table[i][j] = str_table[i - 1][j - 1] + item[j - 1]
                # delete
                temp_del = table[i - 1][j] + 1;
                if temp_del < table[i][j]:
                    table[i][j] = temp_del
                    str_table[i][j] = str_table[i - 1][j] + '-' + target[i - 1]
                # insert
                temp_ins = table[i][j - 1] + 1;
                if temp_ins < table[i][j]:
                    table[i][j] = temp_ins
                    str_table[i][j] = str_table[i][j - 1] + '+' + item[j - 1]
        
        ans[item] = table[l1][l2]
        str_ans[item] = str_table[l1][l2]

    sorted_ans = sorted(ans.items(), key=lambda x: (x[1], x[0]))

    res = []
    for i in sorted_ans:
        print(i[0], i[1])
        res.append(str_ans[i[0]])

    if len(res) > 10:
        res = res[:10]

    return res
