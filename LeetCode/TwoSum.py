def twoSum(List, target: int):
    output = list(filter(lambda x: x <= target, List))
    diff = target
    for i in range(len(output)):
        for j in range(i + 1, len(output)):
            if output[i] + output[j] - target < diff:
                res_i = i
                res_j = j
    return res_i, res_j


print(twoSum([3,2,4], 6))
