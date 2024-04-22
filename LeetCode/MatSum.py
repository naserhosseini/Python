def matrixBlockSum(mat, k):
    n = len(mat)
    m = len(mat[0])

    for i in range(n):
        l = 0
        for j in range(m):
            # Calculate Prefix Sum
            l += mat[i][j]
            mat[i][j] = (mat[i][j], l)

    ans = []
    for i in range(n):
        temp = []
        for j in range(m):
            mnr = max(0, i - k)
            mnc = max(0, j - k)
            mxr = min(n - 1, i + k)
            mxc = min(m - 1, j + k)
            ans1 = 0
            for l in range(mnr, mxr + 1):
                ans1 += (mat[l][mxc][1] - mat[l][mnc][1]) + mat[l][mnc][0]
            temp.append(ans1)
        ans.append(temp)
    return ans


print(matrixBlockSum(mat = [[1,2,3],[4,5,6],[7,8,9]], k = 1))