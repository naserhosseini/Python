class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle not in haystack:
            return -1

        return haystack.index(needle)



test = Solution()
print(test.strStr(haystack = "leetcode", needle = "leeto"))
