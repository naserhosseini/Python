def solution(A, Y):
    # write your code in Python 3.6
    if Y < 0:
        print('k could not be negative')
        return 0
    if Y >= len(A)-1:
        print('k must be less than {}, length of the list {} minus - 1'.format(len(A)-1, A))
        return 0
    datatype = list(map(lambda x: isinstance(x, int), A))
    if False in datatype:
        print('The list must have non negative values')
        return 0
    if min(A) < 0:
        print('The list must have non negative values')
        return 0
    collect = []
    for i in range(len(A)-1):
        collect.append(A[i]+A[i+1])
    collect.sort()
    return sum(collect[-Y:])


print(solution([1, 4, 3, 5, 2, 9], 1))

