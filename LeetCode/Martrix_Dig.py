class Solution:
    def diagonalSum(self, mat: list[list[int]]) -> int:
        sum = 0
        for i in range(len(mat[0])):
            if i != len(mat[0]) // 2 or len(mat[0]) % 2 == 0:
                sum += mat[i][i]+mat[i][-(i+1)]
            else:
                sum += mat[i][i]
        return sum


a = Solution()
print(a.diagonalSum(mat=[[1,2,3],
                          [4,5,6],
                          [7,8,9]]))
