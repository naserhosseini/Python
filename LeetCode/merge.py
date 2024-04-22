class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort()
        output = [intervals[0]]
        for i in range(1, len(intervals)):
            if output[-1][1] >= intervals[i][0]:
                output[-1] = [output[-1][0], intervals[i][1]] if intervals[i][1]>output[-1][1] else [output[-1][0], output[-1][1]]
            else:
                output.append(intervals[i])
        return output

test = Solution()
print(test.merge([[1,4],[2,3]]))
print(test.merge([[2,6],[1,3],[8,10],[15,18]]))
print(test.merge([[1,4],[4,5]]))
