class Solution:
    def hasGroupsSizeX(self, deck: list[int]) -> bool:
        cnt = {}
        for i in range(len(deck)):
            if deck[i] in cnt.keys():
                cnt[deck[i]] += 1
            else:
                cnt[deck[i]] = 1
        val = set(cnt.values())
        return True if len(val) == 1 else False

test = Solution()
print(test.hasGroupsSizeX(deck = [1,1,1,2,2,2,3,3,3]))