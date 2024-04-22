'''
Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0).
The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)2 + (y1 - y2)2).
You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
'''

def kClosest(points, k):
    X = [item[0] for item in points]
    Y = [item[1] for item in points]

    dist = list(map(lambda x, y: (x ** 2 + y ** 2) ** 0.5, X, Y))
    dist_dict = {i : dist[i] for i in range(len(dist))}
    dist_dict = dict(sorted(dist_dict.items(), key=lambda item: item[1]))
    my_keys = sorted(dist_dict, key=dist_dict.get)[:k]
    results = list(map(lambda x: points[x], my_keys))
    return results

print(kClosest(points = [[3,3],[5,-1],[-2,4]], k = 2))
