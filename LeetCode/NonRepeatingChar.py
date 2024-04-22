class Solution:
    def firstUniqChar(self, s: str) -> int:
        # char = dict(map(lambda x: if  , s))
        char = {}
        for i in range(len(s)):
            if s[i] in char.keys():
                char[s[i]] += 1
            else:
                char[s[i]] = 1
        if 1 in char.values():
            l = list(char.keys())[list(char.values()).index(1)]
            return s.index(l)
        else:
            return -1


test = Solution()
print(test.firstUniqChar('dddccdbba'))
