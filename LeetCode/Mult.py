'''
Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].

The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.

You must write an algorithm that runs in O(n) time and without using the division operation.
'''

class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        mult_list = []
        for i in range(len(nums)):
            a = 1
            for j in range(len(nums)):
                if i != j:
                    a *= nums[j]
            mult_list.append(a)
        return mult_list

test = Solution()
print(test.productExceptSelf([-1,1,0,-3,3]))
