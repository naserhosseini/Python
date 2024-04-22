class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        q = 1
        for i in range(len(digits)-1, -1, -1):
            r = (digits[i] + q) % 10
            q = (digits[i] + q) // 10
            digits[i] = r
            if q == 0:
                break
        else:
            digits.insert(0, 1)
        return digits


test = Solution()
print(test.plusOne(digits=[4,3,2,1]))
print(test.plusOne(digits=[9,9,9,9]))