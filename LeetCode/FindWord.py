'''
Given an m x n board of characters and a list of strings words, return all words on the board.
Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring.
The same letter cell may not be used more than once in a word.

Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
'''

class Solution:
    def findWords(self, board: list[list[str]], words: list[str]) -> list[str]:
        leng = list(range(len(board[0])))
        row = list(map(lambda x: ''.join(x), board))
        col = list(map(lambda i: ''.join([row[i] for row in board]), leng))
        row.extend(col)
        print(row)
        res = list(filter(lambda x: x in row, words))
        return res


test = Solution()
print(test.findWords(board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","aakl","eat","rain"]))