import math
import os
import random
import re
import sys

#
# Complete the 'equalStacks' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY h1
#  2. INTEGER_ARRAY h2
#  3. INTEGER_ARRAY h3
#

def equalStacks(h1, h2, h3):
    # Write your code here
    l1, l2, l3 = 0, 0, 0
    for each in h1:
        l1 = l1 + each
    for each in h2:
        l2 = l2 + each
    for each in h3:
        l3 = l3 + each
    while l1 !=0 and l2 != 0 and l3 != 0 and (l1!=l2 or l2!=l3):
        if max(l1, l2, l3) == l1:
            l1 = l1 - h1[0]
            h1.pop(0)
        elif max(l1, l2, l3) == l2:
            l2 = l2 - h2[0]
            h2.pop(0)
        else:
            l3 = l3 - h3[0]
            h3.pop(0)
    else:
        if l1==l2 and l2==l3:
            return l1
        else:
            return 0

h1,h2,h3=[3,2,1,1,1],[4,3,2],[1,1,4,1]

result = equalStacks(h1, h2, h3)
print(result)

