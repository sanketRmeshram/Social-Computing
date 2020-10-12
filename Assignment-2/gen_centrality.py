'''

Name : Sanket Meshram
Roll No. : 17CS30030

'''
"""
Closeness centrality : just do bfs from each node
Betweenness centrality : 

"""

import time
from queue import Queue


def distance_array_BFS(g,start) :
    dist = [-1 for _ in range(len(g))]
    q = Queue(maxsize=len(g))
    dist[start] = 0
    q.put(start)
    while q.empty() is False:
        node = q.get()
        for to  in g[node] :
            if dist[to] == -1 :
                dist[to] = dist[node] +1
                q.put(to)

    return dist 




def ClosenessCentrality(g) :
    ans = [-1 for _ in range(len(g))]
    n = len(g)
    for i in range(n) : 
        ans[i] = (n-1)/sum(distance_array_BFS(g,i))
    return ans

def Brands_BFS(start,g,CB) :

    stk = []
    P = [[] for _ in range(len(g))]
    sigma = [0 for _ in range(len(g))]
    sigma[start] = 1
    dist = [-1 for _ in range(len(g))]
    dist[start] = 0
    q = Queue(maxsize=len(g))
    q.put(start)
    while q.empty() is False:
        v = q.get()
        stk.append(v)
        for w in g[v]:
            if dist[w] == -1:
                dist[w] = dist[v] + 1
                q.put(w)
            if dist[w] == dist[v] + 1 :
                sigma[w] += sigma[v]
                P[w].append(v)
    delta = [0 for _ in range(len(g))]
    while  len(stk) :
        w = stk.pop()
        for v in P[w] :
            delta[v]+= sigma[v]/sigma[w] * (1+delta[w])
            if w!=start : 
                CB[w]+=delta[w]


def BetweennessCentrality_Brands(g):
    n = len(g)
    # CB array will store the BetweennessCentrality of each node
    CB = [0 for i in range(len(g))]
    for s in range(n) :
        Brands_BFS(s,g,CB)
    CB = [i*2/((n-1)*(n-2)) for i in CB]
    return CB
    
def PageRank(g,alpha) :
    n = len(g)
    d = [1/n for _ in range(n) ]
    Biased_Nodes = ((n-1)//4) +1
    for i in range(n) :
        if i%4 ==0 :
            d[i]=1/Biased_Nodes

    PR = [_ for _ in d]
    for _ in range(300) :  # cange afterward
        for u in range(n) :
            t=0
            for v in g[u] :
                t+=PR[v]/len(g[v])
            PR[u] = alpha*t + (1-alpha)*d[u]
    return PR
    

def make_graph():
    edge_file = open("datasets/facebook_combined.txt")
    edges = []
    nodes=[]
    while True:
        line = edge_file.readline()
        if len(line) == 0:
            break
        a, b = [int(node) for node in line.split()]
        edges.append([a, b])
        nodes.append(a)
        nodes.append(b)
    nodes= list(set(nodes))
    g = [[] for _ in range(max(nodes)+1)]
    for i in edges :
        g[i[0]].append(i[1])
        g[i[1]].append(i[0])
    return g


def SaveToFile(a,FileName):
    data = [(a[i],i) for i in range(len(a))]
    data = sorted(data)
    data = reversed(data)
    output = open("centralities/"+FileName,"w")
    for val,i in data :
        print(i,round(val,6),file = output)
    pass

if __name__ == "__main__":

    start_time = time.time()

    g= make_graph()
    
    SaveToFile(ClosenessCentrality(g), "closeness.txt")

    print("--- %s seconds ---" % (time.time() - start_time))

    SaveToFile(BetweennessCentrality_Brands(g), "betweenness.txt")

    print("--- %s seconds ---" % (time.time() - start_time))

    SaveToFile(PageRank(g,.8), "pagerank.txt")

    print("--- %s seconds ---" % (time.time() - start_time))
    
    pass
