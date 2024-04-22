def shell_sort(a_list):
    sublistcount=len(a_list)//2
    while sublistcount>0:
        for i in range(sublistcount):
            sublist(a_list,i,sublistcount)
        print(a_list)
        sublistcount=sublistcount//2
    return(a_list)

def sublist(a_list,start, gap):
    for i in range(start+gap,len(a_list),gap):
        cur_val=a_list[i]
        index=i
        while index>=gap and a_list[index-gap]>cur_val:
            a_list[index]=a_list[index-gap]
            index=index-gap

        a_list[index]=cur_val
    return a_list

print(shell_sort([10,31,9,41,7,1,18,23]))