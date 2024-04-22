class Solution:
    def invertTree(self, root: list[int]) -> list[int]:
        level = int(len(root) ** 0.5)+1
        output = []
        for i in range(1, level+1):
            print(i, 2**(i-1)-1, 2**i-1, root[2**(i-1)-1:2**i-1])
            out = root[2**(i-1)-1:2**i-1]
            out.reverse()
            output.extend(out)
        return output

test = Solution()
print(test.invertTree(root = [4,2,7,1,3,6,9]))
