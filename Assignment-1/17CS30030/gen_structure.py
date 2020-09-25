'''

Name : Sanket Meshram
Roll No. : 17CS30030

'''

import sys

import snap
Rnd = snap.TRnd(42)
Rnd.Randomize()

def list_of_edge_from_file(file_name):
    edge_file = open("subgraphs/" + file_name)
    edges=[]
    while True : 
        line = edge_file.readline()
        if len(line) == 0 :
            break
        a,b = [int(node) for node in line.split()]
        edges.append([a,b])
    return edges

def make_snap_graph(edges) :
    nodes=[]
    for i in edges:
        nodes.append(i[0])
        nodes.append(i[1])
    nodes = set(nodes)
    graph = snap.TUNGraph.New()
    for node in nodes :
        graph.AddNode(node)
    for i in edges : 
        graph.AddEdge(i[0],i[1])
    return graph 

def nodes_with_highest_degree(graph) :
    mx_deg=max([ node.GetDeg() for node in graph.Nodes()])
    return [node.GetId() for node in graph.Nodes() if node.GetDeg() == mx_deg]
    
def get_bridges(graph) : 
    bridges = snap.TIntPrV() 
    snap.GetEdgeBridges(graph,bridges)
    return bridges


def get_articulation_points(graph):
    articulation_points = snap.TIntV()   
    snap.GetArtPoints(graph, articulation_points)
    return articulation_points

def get_mean(data) : 
    return sum(data)/len(data)

def get_variance(data) : 
    mean=get_mean(data)
    return sum([(i-mean)**2 for i in data])/len(data)

def get_each_nodes_ClusteringCofficient(graph) :
    ClusteringCofficients = snap.TIntFltH()
    snap.GetNodeClustCf(graph,ClusteringCofficients)
    return ClusteringCofficients


def plot_distribution(data,name,x_label,y_label) : 
    x = []
    y = []
    for pair in data : 
        x.append(pair.GetVal1())
        y.append(pair.GetVal2())
    import matplotlib.pyplot as plt
    plt.scatter(x,y,s=6)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(name)
    plt.savefig("plots/"+name+".png")
    plt.close()


if __name__ == "__main__":
    '''
        # ask how to take input from file cause directory of terminal can vary ?
        # what is variance and mean in here ?
        how to plot ?
        # how to do last 3 parts ? 

    '''
    file_name = sys.argv[1]   
    # file_name = "facebook.elist"
    subgraph_name=file_name.split('.')[0]
    graph = make_snap_graph( list_of_edge_from_file(file_name) )

    print("Number of nodes:",graph.GetNodes())
    print("Number of edges:",graph.GetEdges())
    print("Number of nodes with degree=7:", snap.CntDegNodes(graph,7) )
    print("Node id(s) with highest degree:", end=" " )
    print(*nodes_with_highest_degree(graph),sep=",")

    snap.PlotInDegDistr(graph, "plots/shortest_path_"+subgraph_name,"Undirected graph - in-degree Distribution")

    full_diameter = []
    full_diameter.append(snap.GetBfsFullDiam(graph, 10))
    print("Approximate full diameter by sampling 10 nodes:",full_diameter[-1])
    full_diameter.append(snap.GetBfsFullDiam(graph, 100))
    print("Approximate full diameter by sampling 100 nodes:",full_diameter[-1])
    full_diameter.append(snap.GetBfsFullDiam(graph, 1000))
    print("Approximate full diameter by sampling 1000 nodes:",full_diameter[-1])

    print("Approximate full diameter (mean and variance): ",get_mean(full_diameter),',',get_variance(full_diameter),sep="")

    effective_diameter = []
    effective_diameter.append(snap.GetBfsEffDiam(graph, 10))
    print("Approximate effective diameter by sampling 10 nodes:", effective_diameter[-1])
    effective_diameter.append(snap.GetBfsEffDiam(graph, 100))
    print("Approximate effective diameter by sampling 100 nodes:",effective_diameter[-1])
    effective_diameter.append(snap.GetBfsEffDiam(graph, 1000))
    print("Approximate effective diameter by sampling 1000 nodes:",effective_diameter[-1])

    print("Approximate effective diameter (mean and variance):", get_mean(effective_diameter), ',', get_variance(effective_diameter), sep="")

    snap.PlotShortPathDistr( graph , "plots/shortest_path_"+subgraph_name , "Undirected graph - shortest path")

    print("Fraction of nodes in largest connected component:", snap.GetMxSccSz(graph))
    print("Number of edge bridges:",get_bridges(graph).Len())
    print("Number of articulation points:",get_articulation_points(graph).Len())

    distribution = snap.TFltPrV()
    snap.GetClustCf(graph, distribution)
    plot_distribution(distribution, "connected_comp_"+subgraph_name,
                      "number of nodes in the component", "number of such components")

    snap.PlotSccDistr(graph, "plots/connected_comp_"+subgraph_name,"Undirected graph - scc distribution")

    print("Average clustering coefficient:", snap.GetClustCf(graph))
    print("Number of triads:", snap.GetTriads(graph))
    random_node = graph.GetRndNId()
    print("Clustering coefficient of random node",random_node,":",get_each_nodes_ClusteringCofficient(graph)[random_node])
    random_node = graph.GetRndNId()
    print("Number of triads random node",random_node, "participates:", snap.GetNodeTriads(graph,random_node))
    print("Number of edges that participate in at least one triad:",snap.GetTriadEdges(graph))

    snap.PlotClustCf(graph, "plots/clustering_coeff_" + subgraph_name,"Undirected graph - clustering coefficient")

    

    
    pass
