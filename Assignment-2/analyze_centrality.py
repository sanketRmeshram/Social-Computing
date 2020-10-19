'''

Name : Sanket Meshram
Roll No. : 17CS30030

'''
import snap

def make_graph():
    edge_file = open("datasets/facebook_combined.txt")
    edges = []
    nodes = []
    while True:
        line = edge_file.readline()
        if len(line) == 0:
            break
        a, b = [int(node) for node in line.split()]
        edges.append([a, b])
        nodes.append(a)
        nodes.append(b)
    nodes = list(set(nodes))
    graph = snap.TNGraph.New()
    assert(len(nodes)==max(nodes)+1)

    for i in nodes:
        graph.AddNode(i)
    for i in edges:
        graph.AddEdge(i[0], i[1])
        graph.AddEdge(i[1], i[0])
    return graph,len(nodes)

def get_same(a,b):
    # print(a)
    using_snap=[]
    normal = []
    assert(len(a)==100)
    for i in a:
        using_snap.append(i[1])
    for i in b:
        normal.append(i[0])
    using_snap = set(using_snap)
    normal = set(normal)
    return len(using_snap & normal)
    

if __name__ == "__main__":
    graph ,n = make_graph()



###################################################################################################
    closeness_centrality_snap=[]
    for i in range(n) :
        closeness_centrality_snap.append([snap.GetClosenessCentr(graph,i), i])
    closeness_centrality_snap = sorted(closeness_centrality_snap)
    closeness_centrality_snap.reverse()

    centrality = open("centralities/closeness.txt")
    closeness_centrality = []
    for _ in range(100):
        line = centrality.readline()
        closeness_centrality.append([i for i in line.split()])
        closeness_centrality[-1][0] = int(closeness_centrality[-1][0])
        closeness_centrality[-1][1] = float(closeness_centrality[-1][1])

    print("#overlaps for Closeness Centrality:", get_same(closeness_centrality_snap[:100],closeness_centrality))

###################################################################################################
    
    betweenness_centrality_snap = snap.TIntFltH()
    temp = snap.TIntPrFltH()
    snap.GetBetweennessCentr(graph, betweenness_centrality_snap, temp, .8)

    betweenness_centrality_snap = [[betweenness_centrality_snap[i],i] for i in range(n)]

    betweenness_centrality_snap = sorted(betweenness_centrality_snap)
    betweenness_centrality_snap.reverse()

    centrality = open("centralities/betweenness.txt")
    betweenness_centrality = []
    for _ in range(100):
        line = centrality.readline()
        betweenness_centrality.append([i for i in line.split()])
        betweenness_centrality[-1][0] = int(betweenness_centrality[-1][0])
        betweenness_centrality[-1][1] = float(betweenness_centrality[-1][1])

    print("#overlaps for Betweenness Centrality:",get_same(betweenness_centrality_snap[:100],betweenness_centrality))
###################################################################################################
    pagerank_centrality_snap = snap.TIntFltH()
    snap.GetPageRank(graph, pagerank_centrality_snap,.8,1e-9,1000)

    pagerank_centrality_snap = [[pagerank_centrality_snap[i], i] for i in range(n)]

    pagerank_centrality_snap = sorted(pagerank_centrality_snap)
    pagerank_centrality_snap.reverse()

    centrality = open("centralities/pagerank.txt")
    pagerank_centrality = []
    for _ in range(100):
        line = centrality.readline()
        pagerank_centrality.append([i for i in line.split()])
        pagerank_centrality[-1][0] = int(pagerank_centrality[-1][0])
        pagerank_centrality[-1][1] = float(pagerank_centrality[-1][1])
    print("#overlaps for PageRank Centrality:",get_same(pagerank_centrality_snap[:100],pagerank_centrality))

###################################################################################################

    pass
