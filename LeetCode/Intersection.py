def intersection(nums1, nums2):
    num_set = list(set(nums1)) if (len(nums1) < len(nums2)) else list(set(nums2))
    source = nums1 if (len(nums1) > len(nums2)) else nums2
    output = list(set(list(map(lambda x: x if (x in source) else None, num_set))))
    if None in output:
        output.remove(None)
    return output


print(intersection([4,7,9,7,6,7], [5,0,0,6,1,6,2,2,4]))

