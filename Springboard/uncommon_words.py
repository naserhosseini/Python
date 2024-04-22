def uncommon_words(str1, str2):
    list1 = str1.lower().split(' ')
    list2 = str2.lower().split(' ')
    list_total1 = list(map(lambda x: x if (x not in list2) else None, list1))
    list_total2 = list(map(lambda x: x if (x not in list1) else None, list2))
    list_total = list(set(list_total1 + list_total2))
    if None in list_total:
        list_total.remove(None)
    list_total.sort()
    uncommon_words_in_strings = list_total
    return uncommon_words_in_strings


print(uncommon_words('Apple is a fruit apple is a fruit of color green and red', 'I have basket of red apples') )#'I love working at facebook', 'I am data engineer at facebook'))#'abcdefghijklmnopqrstuvwxyz', 'ABCDEFghIJKLmnopQrSTUVwxyz')) #
assert uncommon_words('I love working at facebook', 'I am data engineer at facebook') == ['am', 'data', 'engineer', 'love', 'working']
assert uncommon_words('abcdefghijklmnopqrstuvwxyz', 'ABCDEFghIJKLmnopQrSTUVwxyz') == []
assert uncommon_words('', '') == []
assert uncommon_words('Apple is a fruit apple is a fruit of color green and red', 'I have basket of red apples') == ['a', 'and', 'apple', 'apples', 'basket', 'color', 'fruit', 'green', 'have', 'i', 'is']

