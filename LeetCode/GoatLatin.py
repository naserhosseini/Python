'''
You are given a string sentence that consist of words separated by spaces. Each word consists of lowercase and uppercase letters only.
We would like to convert the sentence to "Goat Latin" (a made-up language similar to Pig Latin.) The rules of Goat Latin are as follows:
If a word begins with a vowel ('a', 'e', 'i', 'o', or 'u'), append "ma" to the end of the word.
For example, the word "apple" becomes "applema".
If a word begins with a consonant (i.e., not a vowel), remove the first letter and append it to the end, then add "ma".
For example, the word "goat" becomes "oatgma".
Add one letter 'a' to the end of each word per its word index in the sentence, starting with 1.
For example, the first word gets "a" added to the end, the second word gets "aa" added to the end, and so on.
Return the final sentence representing the conversion from sentence to Goat Latin.

Example 1:

Input: sentence = "I speak Goat Latin"
Output: "Imaa peaksmaaa oatGmaaaa atinLmaaaaa"
'''
class Solution:
    def toGoatLatin(self, sentence: str) -> str:
        sent = sentence.split(' ')
        vowel = ['a', 'e', 'o', 'i', 'u']
        ind = list(range(1, len(sent) + 1))
        output = list(map(lambda x, y: x + 'ma' + 'a'*y if (x[0].lower() in vowel) else x[1:] + x[0] + 'ma' + 'a'*y, sent, ind))
        out = ' '.join(output)
        return out

#heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa
#heTmaa uickqmaaa rownbmaaaa oxfmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa
#heTmaa uickqmaaa rownbmaaaa heTmaaaaa umpedjmaaaaaa overmaaaaaaa hetmaaaaaaaa azylmaaaaaaaaa ogdmaaaaaaaaaa

test = Solution()
print(test.toGoatLatin("The quick brown fox jumped over the lazy dog"))