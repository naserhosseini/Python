class Solution:
    def uniqueOccurrences(self, arr: list[int]) -> bool:

        num = {}
        for i in range(len(arr)):
            if arr[i] in num.keys():
                num[arr[i]] += 1
            else:
                num[arr[i]] = 1
        val = num.values()
        return True if len(val) == len(set(val)) else False


test = Solution()
print(test.uniqueOccurrences(arr=[-3,0,1,-3,1,1,1,-3,10,0]))

