def insert_sort(a_list):
    index=range(1,len(a_list))
    for i in index:
        val_sort=a_list[i]
        while a_list[i-1]>val_sort and i>0:
            a_list[i],a_list[i-1]=a_list[i-1],a_list[i]
            i-=1
            print(a_list)
    return a_list

print(insert_sort([10,31,9,41,7,1,18,23]))