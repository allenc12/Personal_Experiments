#!/usr/bin/env python3
try:
    import sys
    import json
    import networkx as nx
    import contextlib

    with contextlib.redirect_stdout(None):
        import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("Ensure that the required modules are installed")
    exit(1)

ANTS_ERR = 1
ROOM_ERR = 2
CONN_ERR = 3
MOVE_ERR = 4
READ_ERR = 5


class Lemon:
    def __init__(self, name=None, G=None, debug=None):
        if name is None:
            self.name = "Graph"
        else:
            self.name = name
        if G is None:
            self.G = nx.Graph()
        else:
            self.G = G
        if debug is None:
            self.debug = 0
        else:
            self.debug = debug
        self.connections = []
        self.nodes = []
        self.start = None
        self.end = None
        self.num_ants = 0
        self.max_moves = None
        self.max_flow = None
        self.ants = {}
        self.antmoves = []
        self.paths = []
        self.nodes_colors = []
        self.edges_colors = []

    def add_room(self, line, start_end):
        if self.debug == 2:
            print("add_room")
        self.nodes.append(line)
        n = line.split(' ')
        if start_end == -1 and 'red' not in self.nodes_colors:
            self.G.add_node(n[0])
            self.end = n[0]
            self.nodes_colors.append('red')
        elif start_end == 1 and 'green' not in self.nodes_colors:
            self.G.add_node(n[0])
            self.start = n[0]
            self.nodes_colors.append('green')
        else:
            self.G.add_node(n[0])
            self.nodes_colors.append('grey')

    def add_edge(self, line):
        if self.debug == 2:
            print("add_edge")
        self.connections.append(line)
        n = line.split('-')
        self.G.add_edge(n[0], n[1], capacity=1)
        self.edges_colors.append('grey')

    def add_ant(self, line):
        if self.debug == 2:
            print("add_ant")
        for move in line.split(" "):
            a = move.split("-")
            if a[0] not in self.ants:
                self.ants[a[0]] = [a[1]]
            else:
                self.ants[a[0]].append(a[1])

    def read_input(self, argfile):
        start_end = 0
        lines = [line.rstrip('\n') for line in argfile]
        num_lines = len(lines)
        if self.debug == 2:
            print("num_lines: " + str(num_lines))
        n = 0
        for line in lines:
            if line is "":
                if self.debug == 2:
                    print("pass")
                pass
            elif n == 0 and line.isdigit():
                self.num_ants = int(line)
                if self.debug == 2:
                    print("num_ants: " + str(self.num_ants))
            elif line[0] == '#':
                if line == "##start":
                    start_end = 1
                elif line == "##end":
                    start_end = -1
                else:
                    start_end = 0
            elif line.count(" ") == 2:
                self.add_room(line, start_end)
            elif "L" not in line and "-" in line:
                self.add_edge(line)
            elif "L" in line and "-" in line:
                self.antmoves.append(line)
                self.add_ant(line)
            n += 1
        if self.debug >= 1:
            print("num_edges: " + str(len(self.G.edges)) +
                  " ecolors: " + str(len(self.edges_colors)))
            print("num_nodes: " + str(len(self.G.nodes)) +
                  " ncolors: " + str(len(self.nodes_colors)))
            print("lines: " + str(len(lines)))
            print("antmoves: " + str(len(self.antmoves)))
            print("paths: " + str(len(self.paths)))
        if self.debug >= 2:
            print("ants: " + str(self.ants))

    def get_flow(self):
        try:
            R = nx.algorithms.flow.edmonds_karp(
                self.G,
                self.start,
                self.end,
            )
            flow_val = nx.maximum_flow_value(self.G, self.start, self.end)
            if self.debug >= 1:
                print("max_flow: " + str(flow_val))
                print(flow_val == R.graph['flow_value'])
        except nx.exception.NetworkXError:
            print("self.G.nodes() is None")

    def draw_graph(self):
        print(nx.info(self.G))
        pos = nx.spectral_layout(self.G)
        # shortpaths = nx.algorithms.all_shortest_paths(self.G, self.start, self.end)
        # nx.draw_networkx_nodes(self.G, pos, sp)
        # ncolors = ["blue" if n in sp else "orange" for n in self.G.nodes()]
        nx.draw_networkx(
            self.G,
            pos,
            node_size=10,
            node_color=self.nodes_colors,
            edge_color=self.edges_colors,
            with_labels=False
        )
        plt.show()


def print_err(code):
    if code == ANTS_ERR:
        print("Ant error")
    elif code == ROOM_ERR:
        print("Room error")
    elif code == CONN_ERR:
        print("Connection error")
    elif code == MOVE_ERR:
        print("Move error")
    elif code == READ_ERR:
        print("Read error")
    sys.exit(1)


def lem_to_json(filename):
    f = open(filename, 'r')
    lines = [line.rstrip('\n') for line in f]
    f.close()
    nodes = []
    edges = []
    for line in lines:
        g = 2
        if line is not "" and line[0] == '#':
            if line == "##start":
                g = 0
            elif line == "##end":
                g = 1
            continue
        elif line.count(' ') == 2:
            nodes.append({"id": line.split(' ')[0], "group": g})
        else:
            tmp = line.split('-')
            edges.append({"source": tmp[0], "target": tmp[1], "value": 2})
    out = open(filename + ".json", 'x')
    out.write(json.JSONEncoder().encode({"nodes": nodes, "links": edges})+'\n')
    out.close()


"""
---flone---
1
#Here is the number of lines required: 33
##start Xgj7 4 4
##end   I_w2 8 4
---big---
361
#Here is the number of lines required: 74
##start Pqz1 0 0
##end   Ox_7 3 3
---soup---
236
#Here is the number of lines required: 88
##start Ixl3 4 4
##end   Eoi4 9 9
"""
col_path = ['green','red','orange','magenta','cyan','brown','blue','black',
            '#f08c00','#308bc0','#f9c030','grey', '#23f012']
def soup():
    f = open("soup_paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    h = tmp[0].split(" ")
    paths = [line.split(" ") for line in tmp[1:]]
    G = nx.read_edgelist("soup-edgelist", delimiter='-', nodetype=str)
    i = 0
    ncolor = []
    for node in G.nodes:
        if node == h[0]:
            ncolor.append(col_path[0])
        elif node == h[1]:
            ncolor.append(col_path[1])
        elif node in paths[0]:
            ncolor.append(col_path[2])
        elif node in paths[1]:
            ncolor.append(col_path[3])
        elif node in paths[2]:
            ncolor.append(col_path[4])
        elif node in paths[3]:
            ncolor.append(col_path[5])
        elif node in paths[4]:
            ncolor.append(col_path[6])
        elif node in paths[5]:
            ncolor.append(col_path[7])
        elif node in paths[6]:
            ncolor.append(col_path[8])
        elif node in paths[7]:
            ncolor.append(col_path[9])
        elif node in paths[8]:
            ncolor.append(col_path[10])
        else:
            ncolor.append(col_path[11])
        i += 1
    ecolor = []
    edges_remove = []
    for edge in G.edges:
        if (edge[0] in paths[0] and edge[1] in paths[0]) or (edge[0] in h and edge[1] in paths[0]) or (edge[0] in paths[0] and edge[1] in h):
            G[edge[0]][edge[1]]['weight'] = 1
            ecolor.append(col_path[2])
        elif (edge[0] in paths[1] and edge[1] in paths[1]) or (edge[0] in h and edge[1] in paths[1]) or (edge[0] in paths[1] and edge[1] in h):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[2] and edge[1] in paths[2]) or (edge[0] in h and edge[1] in paths[2]) or (edge[0] in paths[2] and edge[1] in h):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[3] and edge[1] in paths[3]) or (edge[0] in h and edge[1] in paths[3]) or (edge[0] in paths[3] and edge[1] in h):
            ecolor.append(col_path[5])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[4] and edge[1] in paths[4]) or (edge[0] in h and edge[1] in paths[4]) or (edge[0] in paths[4] and edge[1] in h):
            ecolor.append(col_path[6])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[5] and edge[1] in paths[5]) or (edge[0] in h and edge[1] in paths[5]) or (edge[0] in paths[5] and edge[1] in h):
            ecolor.append(col_path[7])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[6] and edge[1] in paths[6]) or (edge[0] in h and edge[1] in paths[6]) or (edge[0] in paths[6] and edge[1] in h):
            ecolor.append(col_path[8])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[7] and edge[1] in paths[7]) or (edge[0] in h and edge[1] in paths[7]) or (edge[0] in paths[7] and edge[1] in h):
            ecolor.append(col_path[9])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[8] and edge[1] in paths[8]) or (edge[0] in h and edge[1] in paths[8]) or (edge[0] in paths[8] and edge[1] in h):
            ecolor.append(col_path[10])
            G[edge[0]][edge[1]]['weight'] = 1
        else:
            edges_remove.append(edge)
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    num_edges = len(G.edges)
    num_nodes = len(G.nodes)
    print("num_nodes: " + str(num_nodes))
    print("num_edges: " + str(num_edges) + " len(ecolor): " + str(len(ecolor)))
    pos = nx.spring_layout(G)
    nodes_colors = 10
    node_color = ncolor
    edge_color = ecolor
    with_labels = False
    nx.draw_networkx(
        G,
        pos,
        node_size,
        node_color,
        edge_color,
        with_labels
    )
    plt.show()


def flonetxt():
    f = open("bingus/flow-one-paths")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    sted = tmp[0].split(" ")
    paths = [line.split(" ") for line in tmp[1:]]
    G = nx.read_edgelist("bingus/flow-one-edges", delimiter='-', nodetype=str)
    ncolor = []
    for node in G.nodes:
        if node == sted[0]:
            ncolor.append(col_path[0])
        elif node == sted[1]:
            ncolor.append(col_path[1])
        elif node in paths[0]:
            ncolor.append(col_path[2])
        else:
            ncolor.append(col_path[11])
    ecolor = []
    for edge in G.edges:
        if (edge[0] in paths[0] and edge[1] in paths[0]) or (edge[0] in sted and edge[1] in paths[0]) or (edge[0] in paths[0] and edge[1] in sted):
            ecolor.append(col_path[2])
            G[edge[0]][edge[1]]['weight'] = 2
        else:
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    print("num_nodes: " + str(len(G.edges)) + " ncolor: " + str(len(ncolor)))
    print("num_edges: " + str(len(G.nodes)) + " ecolor: " + str(len(ecolor)))
    nx.draw_networkx(
        G,
        pos=nx.spring_layout(G),
        node_size=10,
        node_color=ncolor,
        edge_color=ecolor,
        with_labels=False
    )
    plt.show()


def fltentxt():
    f = open("bingus/flow-ten-paths")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    sted = tmp[0].split(" ")
    paths = [line.split(" ") for line in tmp[1:]]
    G = nx.read_edgelist("bingus/flow-ten-edges", delimiter='-', nodetype=str)
    ncolor = []
    for node in G.nodes:
        if node == sted[0]:
            ncolor.append(col_path[0])
        elif node == sted[1]:
            ncolor.append(col_path[1])
        elif node in paths[0]:
            ncolor.append(col_path[2])
        elif node in paths[1]:
            ncolor.append(col_path[3])
        elif node in paths[2]:
            ncolor.append(col_path[4])
        elif node in paths[3]:
            ncolor.append(col_path[5])
        else:
            ncolor.append(col_path[11])
    ecolor = []
    for edge in G.edges:
        if (edge[0] in paths[0] and edge[1] in paths[0]) or (edge[0] in sted and edge[1] in paths[0]) or (edge[0] in paths[0] and edge[1] in sted):
            ecolor.append(col_path[2])
            G[edge[0]][edge[1]]['weight'] = 2
        elif (edge[0] in paths[1] and edge[1] in paths[1]) or (edge[0] in sted and edge[1] in paths[1]) or (edge[0] in paths[1] and edge[1] in sted):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 2
        elif (edge[0] in paths[2] and edge[1] in paths[2]) or (edge[0] in sted and edge[1] in paths[2]) or (edge[0] in paths[2] and edge[1] in sted):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 2
        elif (edge[0] in paths[3] and edge[1] in paths[3]) or (edge[0] in sted and edge[1] in paths[3]) or (edge[0] in paths[3] and edge[1] in sted):
            ecolor.append(col_path[5])
            G[edge[0]][edge[1]]['weight'] = 2
        else:
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    print("num_nodes: " + str(len(G.edges)) + " ncolor: " + str(len(ncolor)))
    print("num_edges: " + str(len(G.nodes)) + " ecolor: " + str(len(ecolor)))
    nx.draw_networkx(
        G,
        pos=nx.spectral_layout(G),
        node_size=10,
        node_color=ncolor,
        edge_color=ecolor,
        with_labels=False
    )
    plt.show()


def flthousandtxt():
    f = open("bingus/flow-thousand-paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    h = tmp[0].split(" ")
    paths = [line.split(" ") for line in tmp[1:]]
    G = nx.read_edgelist("bingus/flow-thousand-edges", delimiter='-', nodetype=str)
    ncolor = []
    for node in G.nodes:
        if node == h[0]:
            ncolor.append(col_path[0])
        elif node == h[1]:
            ncolor.append(col_path[1])
        elif node in paths[0]:
            ncolor.append(col_path[2])
        elif node in paths[1]:
            ncolor.append(col_path[3])
        elif node in paths[2]:
            ncolor.append(col_path[4])
        elif node in paths[3]:
            ncolor.append(col_path[5])
        elif node in paths[4]:
            ncolor.append(col_path[6])
        elif node in paths[5]:
            ncolor.append(col_path[7])
        elif node in paths[6]:
            ncolor.append(col_path[8])
        elif node in paths[7]:
            ncolor.append(col_path[9])
        elif node in paths[8]:
            ncolor.append(col_path[10])
        else:
            ncolor.append(col_path[11])
    ecolor = []
    for edge in G.edges:
        if (edge[0] in paths[0] and edge[1] in paths[0]) or (edge[0] in h and edge[1] in paths[0]) or (edge[0] in paths[0] and edge[1] in h):
            G[edge[0]][edge[1]]['weight'] = 1
            ecolor.append(col_path[2])
        elif (edge[0] in paths[1] and edge[1] in paths[1]) or (edge[0] in h and edge[1] in paths[1]) or (edge[0] in paths[1] and edge[1] in h):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[2] and edge[1] in paths[2]) or (edge[0] in h and edge[1] in paths[2]) or (edge[0] in paths[2] and edge[1] in h):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[3] and edge[1] in paths[3]) or (edge[0] in h and edge[1] in paths[3]) or (edge[0] in paths[3] and edge[1] in h):
            ecolor.append(col_path[5])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[4] and edge[1] in paths[4]) or (edge[0] in h and edge[1] in paths[4]) or (edge[0] in paths[4] and edge[1] in h):
            ecolor.append(col_path[6])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[5] and edge[1] in paths[5]) or (edge[0] in h and edge[1] in paths[5]) or (edge[0] in paths[5] and edge[1] in h):
            ecolor.append(col_path[7])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[6] and edge[1] in paths[6]) or (edge[0] in h and edge[1] in paths[6]) or (edge[0] in paths[6] and edge[1] in h):
            ecolor.append(col_path[8])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[7] and edge[1] in paths[7]) or (edge[0] in h and edge[1] in paths[7]) or (edge[0] in paths[7] and edge[1] in h):
            ecolor.append(col_path[9])
            G[edge[0]][edge[1]]['weight'] = 1
        elif (edge[0] in paths[8] and edge[1] in paths[8]) or (edge[0] in h and edge[1] in paths[8]) or (edge[0] in paths[8] and edge[1] in h):
            ecolor.append(col_path[10])
            G[edge[0]][edge[1]]['weight'] = 1
        else:
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    print("num_nodes: " + str(len(G.edges)) + " ncolor: " + str(len(ncolor)))
    print("num_edges: " + str(len(G.nodes)) + " ecolor: " + str(len(ecolor)))
    nx.draw_networkx(
        G,
        pos=nx.spring_layout(G),
        node_size=10,
        node_color=ncolor,
        edge_color=ecolor,
        with_labels=False
    )
    plt.show()


def big():
    f = open("big_paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    bh = tmp[0].split(" ")
    bpaths = [line.split(" ") for line in tmp[1:]]
    G = nx.read_edgelist("big-edgelist", delimiter='-', nodetype=str)
    i = 0
    ncolor = []
    for node in G.nodes:
        if node == bh[0]:
            ncolor.append(col_path[0])
        elif node == bh[1]:
            ncolor.append(col_path[1])
        elif node in bpaths[0]:
            ncolor.append(col_path[2])
        elif node in bpaths[1]:
            ncolor.append(col_path[3])
        elif node in bpaths[2]:
            ncolor.append(col_path[4])
        else:
            ncolor.append(col_path[11])
        i += 1
    ecolor = []
    edges_remove = []
    for edge in G.edges:
        if (edge[0] in bpaths[0] and edge[1] in bpaths[0]) or (edge[0] in bh and edge[1] in bpaths[0]) or (edge[0] in bpaths[0] and edge[1] in bh):
            ecolor.append(col_path[2])
            G[edge[0]][edge[1]]['weight'] = 2
        elif (edge[0] in bpaths[1] and edge[1] in bpaths[1]) or (edge[0] in bh and edge[1] in bpaths[1]) or (edge[0] in bpaths[1] and edge[1] in bh):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 2
        elif (edge[0] in bpaths[2] and edge[1] in bpaths[2]) or (edge[0] in bh and edge[1] in bpaths[2]) or (edge[0] in bpaths[2] and edge[1] in bh):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 2
        else:
            edges_remove.append(edge)
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    print("num_nodes: " + str(len(G.edges)) + " ncolor: " + str(len(ncolor)))
    print("num_edges: " + str(len(G.nodes)) + " ecolor: " + str(len(ecolor)))
    nx.draw_networkx(
        G,
        pos=nx.spectral_layout(G),
        node_size=10,
        node_color=ncolor,
        edge_color=ecolor,
        with_labels=False
    )
    plt.show()


def main():
    loops = Lemon(debug=0)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'big':
            big()
        elif sys.argv[1] == 'soup':
            soup()
        elif sys.argv[1] == 'flonetxt':
            flonetxt()
        elif sys.argv[1] == 'fltentxt':
            fltentxt()
        elif sys.argv[1] == 'flthousandtxt':
            flthousandtxt()
        else:
            try:
                f = open(sys.argv[1], 'r')
                loops.read_input(f)
                f.close()
                loops.get_flow()
                loops.draw_graph()
            except FileNotFoundError:
                print_err(READ_ERR)
    else:
        try:
            loops.read_input(sys.stdin)
            loops.draw_graph()
        except FileNotFoundError:
            print_err(READ_ERR)
        #TODO: Lemon.draw_graph()


if __name__ == '__main__':
    main()
