class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(t) != len(s):
            return False
        char = []
        for i in range(len(t)):
            if s[i] not in char:
                char.append(s[i])
                if s[i] not in t:
                    return False
                if s.count(s[i]) != t.count(s[i]):
                    return False

        return True




test = Solution()
print(test.isAnagram(s = "anagram", t = "nagrram"))