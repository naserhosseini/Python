def selection_sort(a_list):
    index=range(len(a_list)-1)

    for i in index:
        min_index=i
        for j in range(i+1,len(a_list)):
            if a_list[j]<a_list[min_index]:
                min_index=j
        if min_index!=i:
            a_list[i],a_list[min_index]=a_list[min_index],a_list[i]
            print(a_list)
    return a_list

print(selection_sort([10,31,9,41,7,1,18,23]))