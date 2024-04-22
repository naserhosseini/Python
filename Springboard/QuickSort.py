def quick_sort(a_list):
    length=len(a_list)
    if length<=1:
        return a_list
    else:
        pivot=a_list.pop()
    item_GT=[]
    item_LT=[]

    for item in a_list:
        if item>pivot:
            item_GT.append(item)
        else:
            item_LT.append(item)
    return quick_sort(item_LT)+[pivot]+quick_sort(item_GT)

print(quick_sort([10,31,9,41,7,1,18,23]))