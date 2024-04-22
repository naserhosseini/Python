def close2zero(A):
    min_l = A[0]
    min_r = A[1]
    min_sum = min_l + min_r
    for l in range(0, len(A) - 1):
        for r in range(l + 1, len(A)):
            sum = A[l] + A[r]
            if abs(min_sum) > abs(sum):
                min_sum = sum
                min_l = l
                min_r = r
    return (A[min_l], A[min_r])


print(close2zero([15, 1, 81, -17, 4]))
