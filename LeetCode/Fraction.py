'''
Given two integers representing the numerator and denominator of a fraction, return the fraction in string format.
If the fractional part is repeating, enclose the repeating part in parentheses.
If multiple answers are possible, return any of them.
It is guaranteed that the length of the answer string is less than 104 for all the given inputs.

Example 1:

Input: numerator = 1, denominator = 2
Output: "0.5"
Example 2:

Input: numerator = 2, denominator = 1
Output: "2"
Example 3:

Input: numerator = 4, denominator = 333
Output: "0.(012)"
'''

def fractionToDecimal(numerator, denominator):
    result = numerator / denominator
    r = numerator % denominator
    if r != 0:
        real = numerator//denominator
        result = real
    return str(result)



print(fractionToDecimal(10, 7))
