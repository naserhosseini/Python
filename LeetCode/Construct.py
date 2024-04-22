class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        out = list(map(lambda x: x in magazine, ransomNote))
        if False in out:
            return False
        else:
            return True


test = Solution()
print(test.canConstruct(ransomNote = "aa", magazine = "ab"))
