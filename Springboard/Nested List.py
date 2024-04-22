from collections.abc import Iterable


def flatten(lis):
    result = []
    for item in lis:
        if isinstance(item, Iterable):
            for x in flatten(item):
                result.append(x)
        else:
            result.append(item)
    return result

# flatList = [ item for elem in listOfList for item in elem]
lis = [1, [2,3], 4, [5, [6, [7, 8]]]]
print(flatten(lis))


