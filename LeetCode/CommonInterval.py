'''
You are given two lists of closed intervals, firstList and secondList, where firstList[i] = [starti, endi] and secondList[j] = [startj, endj].
Each list of intervals is pairwise disjoint and in sorted order.
Return the intersection of these two interval lists.
A closed interval [a, b] (with a <= b) denotes the set of real numbers x with a <= x <= b.
The intersection of two closed intervals is a set of real numbers that are either empty or represented as a closed interval. For example, the intersection of [1, 3] and [2, 4] is [2, 3].

Example 1:
Input: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]
Output: [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
'''

def intervalIntersection(firstList, secondList):
    list_dict = {'1o': [], '1c': [], '2o': [], '2c': []}
    for i in range(len(firstList)):
        list_dict['1o'].append(firstList[i][0])
        list_dict['1c'].append(firstList[i][1])
    for i in range(len(secondList)):
        list_dict['2o'].append(secondList[i][0])
        list_dict['2c'].append(secondList[i][1])
    return list_dict


def nested(a):
    result = iter(a)
    try:
        print(next(result))
        print(next(result))
        print(next(result))
        print(next(result))
        print(next(result))
        print(next(result))
    except:
        print(err)

print(nested([[0,2],[5,10],[13,23],[24,25]]))
#print(intervalIntersection(firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]]))