class Solution:
    def shuffle(self, nums: list[int], n: int) -> list[int]:
        odd = nums[:n]
        even = nums[n:]
        lis = list(map(lambda x, y: [x, y],  odd, even))
        output = [element for innerList in lis for element in innerList]
        return output

test = Solution()
print(test.shuffle(nums = [2,5,1,3,4,7], n = 3))