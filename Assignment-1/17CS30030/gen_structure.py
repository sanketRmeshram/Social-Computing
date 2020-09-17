
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
    

if __name__ == "__main__":

    # file_name = sys.argv[1]
    file_name = "facebook.elist"
    subgraph_name=file_name.split('.')[0]
    graph = make_snap_graph( list_of_edge_from_file(file_name) )

    print("Number of nodes:",graph.GetNodes())
    print("Number of edges:",graph.GetEdges())
    print("Number of nodes with degree=7:", snap.CntDegNodes(graph,7) )  # ???????????
    print("Node id(s) with highest degree:", end=" " )
    print(*nodes_with_highest_degree(graph),sep=",")
    # snap.PlotInDegDistr(graph, "example ", subgraph_name+" degree Distribution")    
    

    
    pass
