class Solution:
    def reverseWords(self, s: str) -> str:
        lst = s.split(' ')
        res = list(map(lambda x: x[::-1], lst))
        output = ' '.join(res)
        return output


test = Solution()
print(test.reverseWords(s = "Let's take LeetCode contest"))