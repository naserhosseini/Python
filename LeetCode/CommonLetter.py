def commonChars(words):
    output = []
    for i in range(len(words[0])):
        for j in range(1,len(words)):
            if words[0][i] in words[j]:
                bln = True
            else:
                bln = False
        if bln:
            output.append(words[0][i])
    return output


print(commonChars(["cool", "lock", "cook"]))
