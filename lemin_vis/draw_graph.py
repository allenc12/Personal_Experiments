#!/usr/bin/env python3
try:
    import sys
    import json
    import cProfile, pstats, io
    from pstats import SortKey
    import argparse
    import contextlib

    with contextlib.redirect_stdout(None):
        import networkx as nx
        import matplotlib.pyplot as plt
except ModuleNotFoundError:
    print("Ensure that the required modules are installed:"
          "*networkx"
          "*matplotlib")
    exit(1)

ANTS_ERR = 1
ROOM_ERR = 2
CONN_ERR = 3
MOVE_ERR = 4
READ_ERR = 5
col_path = ['green', 'red', 'orange', 'magenta', 'cyan', 'brown', 'blue', 'black',
            '#f08c00', '#308bc0', '#f9c030', '#23f012', '#497663', '#ec5952', '#db8fb0',
            '#afc58c', '#08ea07', '#3e60f3', '#9d5d80', '#701488', '#a78923', '#d461f8',
            '#0628c4', '#2f8bdc', '#1abf73', '#04edc1', '#dffe5d', '#fbfbad', '#b26258',
            '#d2881e', '#95d6ae', 'grey']


def draw_graph_nodes(G, paths, pos, col_path, draw_grey):
    n = 0
    for node in G.nodes:
        if node == paths[0][0]:
            nx.draw_networkx_nodes(G, pos, nodelist=[node],
                                   node_color=col_path[0], node_size=20)
        elif node == paths[0][1]:
            nx.draw_networkx_nodes(G, pos, nodelist=[node],
                                   node_color=col_path[1], node_size=20)
        for i in range(1, len(paths)):
            if node in paths[i]:
                nx.draw_networkx_nodes(G, pos, nodelist=[node],
                                       node_color=col_path[i+1], node_size=20)
                flag = False
                break
            else:
                flag = True
        if flag and draw_grey:
            nx.draw_networkx_nodes(G, pos, nodelist=[node],
                                   node_color=col_path[-1],
                                   node_size=2, alpha=0.1)
        flag = False
        n += 1
        if n == len(G.nodes):
            break
    print("num_nodes: " + str(len(G.nodes)) + " n: " + str(n))


def draw_graph_edges(G, paths, pos, col_path, draw_grey):
    e = 0
    for edge in G.edges:
        for i in range(1, len(paths)):
            if (
                    (edge[0] in paths[i] and edge[1] in paths[i])
                    or (edge[0] in paths[0] and edge[1] in paths[i])
                    or (edge[0] in paths[i] and edge[1] in paths[0])
            ):
                nx.draw_networkx_edges(G, pos, edgelist=[edge],
                                       edge_color=col_path[i+1])
                flag = False
                break
            else:
                flag = True
        if flag and draw_grey:
            nx.draw_networkx_edges(G, pos, edgelist=[edge],
                                   edge_color=col_path[-1], alpha=0.1)
        flag = False
        e += 1
        if e == len(G.edges):
            break
    print("num_edges: " + str(len(G.edges)) + " e: " + str(e))


class Lemon:
    def __init__(self, name=None, G=None, draw_grey=None, debug=None, pos=None):
        if name is None:
            self.name = "Graph"
        else:
            self.name = name
        if G is None:
            self.G = nx.Graph(name=self.name)
        else:
            self.G = G
        if draw_grey is None:
            self.draw_grey = False
        else:
            self.draw_grey = draw_grey
        if debug is None:
            self.debug = 0
        else:
            self.debug = debug
        if pos is None:
            self.pos = "spectral"
        else:
            self.pos = pos
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
            self.G.add_node(n[0], weight=2)
            self.end = n[0]
            self.nodes_colors.append('red')
        elif start_end == 1 and 'green' not in self.nodes_colors:
            self.G.add_node(n[0], weight=2)
            self.start = n[0]
            self.nodes_colors.append('green')
        else:
            self.G.add_node(n[0], weight=1)
            self.nodes_colors.append('grey')

    def add_edge(self, line):
        if self.debug == 2:
            print("add_edge")
        self.connections.append(line)
        n = line.split('-')
        self.G.add_edge(n[0], n[1], capacity=1, weight=1)
        self.edges_colors.append("grey")

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
        lines = [line.rstrip("\n") for line in argfile]
        num_lines = len(lines)
        if self.debug == 2:
            print("num_lines: " + str(num_lines))
        n = 0
        for line in lines:
            if line == "":
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
        tmp = []
        for move in self.antmoves[0].split(" "):
            tmp.append(move.split("-")[0])
        self.paths.append([self.start, self.end])
        for ant in tmp:
            self.paths.append(self.ants[ant][:-1])
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
        if self.pos == "spring":
            pos = nx.spring_layout(self.G)
        elif self.pos == "circular":
            pos = nx.circular_layout(self.G)
        elif self.pos == "kamada":
            pos = nx.kamada_kawai_layout(self.G)
        elif self.pos == "random":
            pos = nx.random_layout(self.G)
        elif self.pos == "shell":
            pos = nx.shell_layout(self.G)
        elif self.pos == "spectral":
            pos = nx.spectral_layout(self.G)
        else:
            pos = nx.spring_layout(self.G)
        draw_graph_nodes(self.G, self.paths, pos, col_path, self.draw_grey)
        draw_graph_edges(self.G, self.paths, pos, col_path, self.draw_grey)
        # nx.draw_networkx_labels(self.G, pos)
        plt.axis('off')
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
        if line != "" and line[0] == '#':
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


def soup(draw_grey):
    f = open("soup_paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("soup-edgelist", delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def flonetxt(draw_grey):
    f = open("bingus/flow-one-paths")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("bingus/flow-one-edges", delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def fltentxt(draw_grey):
    f = open("bingus/flow-ten-paths")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("bingus/flow-ten-edges", delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def flthousandtxt(draw_grey):
    f = open("bingus/flow-thousand-paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("bingus/flow-thousand-edges",
                         delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def bigtxt(draw_grey):
    f = open("bingus/big-paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("bingus/big-edges", delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def souptxt(draw_grey):
    f = open("bingus/soup-paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("bingus/soup-edges", delimiter='-', nodetype=str)
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.spectral_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    print(nx.info(G))
    plt.axis('off')
    plt.show()


def big(draw_grey):
    f = open("big_paths", "r")
    tmp = [line.rstrip("\n") for line in f]
    f.close()
    paths = [line.split(" ") for line in tmp]
    G = nx.read_edgelist("big-edgelist", delimiter='-', nodetype=str)
    pos = nx.kamada_kawai_layout(G)
    draw_graph_nodes(G, paths, pos, col_path, draw_grey)
    draw_graph_edges(G, paths, pos, col_path, draw_grey)
    plt.axis('off')
    plt.show()


def main():
    if len(sys.argv) > 1 and "--debug" in sys.argv:
        debug = True
    else:
        debug = False
    if debug:
        pr = cProfile.Profile()
        pr.enable()
    # p = argparse.ArgumentParser()
    # p.add_argument("layout", help="specify graph layout")
    # args
    dg = False
    layout = None
    if len(sys.argv) > 1:
        if "--draw-grey" in sys.argv:
            dg = True
        if "--layout=spectral" in sys.argv:
            layout = "spectral"
        if "--layout=kamada" in sys.argv:
            layout = "kamada"
        if "--layout=spring" in sys.argv:
            layout = "spring"
        if "--layout=circular" in sys.argv:
            layout = "circular"
        if "--layout=shell" in sys.argv:
            layout = "shell"
        if "--layout=random" in sys.argv:
            layout = "random"
        loops = Lemon(name=sys.argv[1], debug=0, draw_grey=dg, pos=layout)
        if sys.argv[1] == 'big':
            big(dg)
        elif sys.argv[1] == 'soup':
            soup(dg)
        elif sys.argv[1] == 'flonetxt':
            flonetxt(dg)
        elif sys.argv[1] == 'fltentxt':
            fltentxt(dg)
        elif sys.argv[1] == 'flthousandtxt':
            flthousandtxt(dg)
        elif sys.argv[1] == 'bigtxt':
            bigtxt(dg)
        elif sys.argv[1] == 'souptxt':
            souptxt(dg)
        else:
            try:
                f = open(sys.argv[1])
                loops.read_input(f)
                f.close()
                loops.get_flow()
                loops.draw_graph()
            except FileNotFoundError:
                print_err(READ_ERR)
    else:
        try:
            loops = Lemon(name="stdin-graph", debug=0, draw_grey=True, pos=layout)
            loops.read_input(sys.stdin)
            loops.draw_graph()
        except FileNotFoundError:
            print_err(READ_ERR)
    if debug:
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())


if __name__ == '__main__':
    main()
