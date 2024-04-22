'''
There are n soldiers standing in a line. Each soldier is assigned a unique rating value.

You have to form a team of 3 soldiers amongst them under the following rules:

Choose 3 soldiers with index (i, j, k) with rating (rating[i], rating[j], rating[k]).
A team is valid if: (rating[i] < rating[j] < rating[k]) or (rating[i] > rating[j] > rating[k]) where (0 <= i < j < k < n).
Return the number of teams you can form given the conditions. (soldiers can be part of multiple teams).

Input: rating = [2,5,3,4,1]
Output: 3
Explanation: We can form three teams given the conditions. (2,3,4), (5,4,1), (5,3,1).
'''

class Solution:
    def numTeams(self, rating: list[int]) -> int:
        total = 0
        for i in range(len(rating)-2):
            out1 = list(filter(lambda x: x > rating[i], rating[i+1:]))
            for j in range(len(out1)-1):
                out2 = list(filter(lambda x: x > out1[j], out1[j+1:]))
                total += len(out2)
        for i in range(len(rating)-2):
            out1 = list(filter(lambda x: x < rating[i], rating[i+1:]))
            for j in range(len(out1)-1):
                out2 = list(filter(lambda x: x < out1[j], out1[j+1:]))
                total += len(out2)
        return total

test = Solution()
print(test.numTeams([1,2,3,4]))
