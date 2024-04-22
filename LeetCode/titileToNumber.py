class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        ind = 0
        for i in range(len(columnTitle)):
            p = len(columnTitle) - i - 1
            ind += (alphabet.index(columnTitle[i].lower()) + 1) * (26 ** p)
        return ind


test = Solution()
print(test.titleToNumber(columnTitle = "ZY"))