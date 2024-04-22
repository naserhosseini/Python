def dijkstra(graph, start,goal):
    shrt_dist={}
    track_prd={}
    unSeen=graph
    infinity=9999

    path=[]
    for node in unSeen:
        shrt_dist[node]=infinity
    shrt_dist[start]=0

    while unSeen:
        min_dist=None
        for node in unSeen:
            if min_dist is None:
                min_dist=node
            elif shrt_dist[node]<shrt_dist[min_dist]:
                min_dist=node
        path_options=graph[min_dist].items()
        for child,weight in path_options:
            if weight+shrt_dist[min_dist]<shrt_dist[child]:
                shrt_dist[child]=weight+shrt_dist[min_dist]
                track_prd[child]=min_dist
        unSeen.pop(min_dist)
    cur_node=goal
    while cur_node!=start:
        try:
            path.insert(0,cur_node)
            cur_node=track_prd[cur_node]
        except  KeyError:
            print('no path')
            break

    path.insert(0,start)
    if shrt_dist[goal]!=infinity:
        print('shortdisc is'+str(shrt_dist[goal]))
        print('OPtimal path is'+str(path))
graph={
    'a':{'b':3,'c':4,'d':7},
    'b':{'c':1,'f':5},
    'c':{'f':6,'d':2},
    'd':{'e':3,'g':6},
    'e':{'g':3,'h':4},
    'f':{'e':1,'h':8},
    'g':{'h':2},
    'h':{'g':2}
}

dijkstra(graph,'------------------------------------------------------------------------------------------------------------------------a','e')