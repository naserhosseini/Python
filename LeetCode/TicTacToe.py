class Solution:
    def tictactoe(self, moves: list[list[int]]) -> str:
        row, col = [[0] * 3 for _ in range(2)], [[0] * 3 for _ in range(2)]
        diag, anti_diag = [0] * 2, [0] * 2
        p = 0
        for r, c in moves:
            row[p][r] += 1
            col[p][c] += 1
            diag[p] += r == c
            anti_diag[p] += r + c == 2
            if 3 in (row[p][r], col[p][c], diag[p], anti_diag[p]):
                return "AB"[p]
            p ^= 1
        return "Draw" if len(moves) == 9 else "Pending"

test = Solution()
print(test.tictactoe([[0,0],[2,0],[1,1],[2,1],[2,2]]))
