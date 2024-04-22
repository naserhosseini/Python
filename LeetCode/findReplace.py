class Solution:
    def findReplaceString(self, s: str, indices: list[int], sources: list[str], targets: list[str]) -> str:
        output = s
        for i in range(len(indices)):
            lgt = len(sources[i])
            if sources[i] in s:
                if s[indices[i]:indices[i]+lgt] == sources[i]:
                    output = output.replace(sources[i], targets[i])
        return output


test = Solution()
print(test.findReplaceString( "vmokgggqzp", [3,5,1], ["kg","ggq","mo"], ["s","so","bfr"]))
print(test.findReplaceString( "wreorttvosuidhrxvmvo", [14,12,10,5,0,18], ["rxv", "dh", "ui", "ttv", "wreor", "vo"], ["frs", "c", "ql", "qpir", "gwbeve", "n"]))

'''
"wreorttvosuidhrxvmvo"
[14,12,10,5,0,18]
["rxv","dh","ui","ttv","wreor","vo"]
["frs","c","ql","qpir","gwbeve","n"]


"gwbeveqpirosqlcfrsmn"
"gwbeveqpirosqlcfrsmn
'''
