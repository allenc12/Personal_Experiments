#!/usr/bin/env python3
try:
    import sys
    import json
    import networkx as nx
    import contextlib
    with contextlib.redirect_stdout(None):
        import matplotlib.pyplot as plt
except:
    print("Ensure that the required modules are installed")
    exit(1)
"""
#lines = [line.rstrip('\n') for line in file]
ANTS_ERR = 1
ROOM_ERR = 2
CONN_ERR = 3
MOVE_ERR = 4
READ_ERR = 5

class Lemon:

    def __init__(self):
        self.name = ""
        self.graph = None
        self.num_ants = 0
        self.antmap = {}
        self.roommap = {}
        self.antmoves = []
        self.start = None
        self.end = None

    def add_room(self, line, start_end):
        n = line.split(' ')
        new = Room(n[0], (int(n[1]), int(n[2])), self.roomsize, start_end)
        if start_end == -1:
            self.start = new
        elif start_end == 1:
            self.end = new
        try:
            if self.roommap[new.name]:
                print_err(ROOM_ERR)
        except:
            self.roommap[new.name] = new

    def readinput(self):
        lines = [line.rstrip('\n') for line in sys.stdin]
        #todo

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
    pygame.quit()
    sys.exit(1)
"""
# f = open("gen_flow_one", 'r')
# lines = [line.rstrip('\n') for line in f]
# l = 1
# g = 0
# line_num = len(lines)
# nodes = []
# while l < line_num and '-' not in lines[l]:
#     g = 2
#     if lines[l][0] == '#':
#         if lines[l] == "##start":
#             g = 0
#         elif lines[l] == "##end":
#             g = 1
#         l += 1
#         continue
#     else:
#         nodes.append({"id": lines[l].split(' ')[0], "group": g})
#     l += 1
# edges = []
# while l < line_num and '-' in lines[l]:
#     if lines[l][0] == '#':
#         pass
#     else:
#         tmp = lines[l].split('-')
#         edges.append({"source": tmp[0], "target": tmp[1], "value": 2})
#     l += 1
# out = open("flone_json", 'x')
# out.write(json.JSONEncoder().encode({"nodes": nodes, "links": edges})+'\n')
# out.close()
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
"""
# h = ['Xgj7','I_w2']
h = ['Pqz1','Ox_7']
paths = [
    [
        'Ouc9', 'Mgt4', 'Grq1', 'Xdu6', 'X_j2', 'Jdz3', 'Pmf9', 'Ohf5', 'Ref9', 'Tfv0', 'Kux7', 'Xwa7',
        'Kky8', 'Rrc3', 'Epw2', 'Vak8', 'Yiq5', 'Ijy6', 'Rlj1', 'Opr4', 'Nxb0', 'Wfg5', 'J_v3', 'Xtm4',
        'Kwk2', 'D_o7', 'Nmq0', 'Hx_4', 'Cc_4', 'Wl_2', 'M_h5', 'Mjd8', 'Mue5', 'Fxr7', 'Yzm4', 'U_x9',
        'Atz1', 'Plm5', 'Pmd2', 'Chl2', 'Etu4', 'Ylh6', 'Zxi1', 'W_c1', 'Esz0', 'Wp_4', 'F_h2', 'Ghf3',
        'Sdc4', 'Npw3', 'Pji1', 'Nvx3', 'Pip8', 'Xsv2', 'Yjy8', 'Xry6', 'Eht1', 'Igg2', 'Rmf2', 'Ox_7'
    ],[
        'Usy7', 'X_o7', 'Jsc7', 'Eeb6', 'Rvp1', 'Oc_8', 'Pj_4', 'Dka8', 'Iqq7', 'Yxz6', 'Kcv8', 'Ziz9',
        'Kku5', 'Z_d3', 'Yfs6', 'Q_o6', 'Kzw7', 'Mgx0', 'Daf1', 'Fab8', 'Axl5', 'Crm2', 'Zop2', 'Yix5',
        'Iun5', 'K_p5', 'Ydl9', 'Eu_2', 'Wmr8', 'Tfv0', 'Hiz8', 'Yal9', 'Kux7', 'W_y5', 'Pfs2', 'Ycl1',
        'Xwa7', 'Epw2', 'Ijy6', 'J_v3', 'D_o7', 'Cc_4', 'Gkl7', 'Mvi4', 'Wl_2', 'Asu3', 'Wxx5', 'M_h5',
        'Hua0', 'F_k2', 'Yos4', 'Fq_4', 'Eux1', 'Bua1', 'G_o1', 'Ox_7'
    ],[
        'Mad0', 'Zyf5', 'R_j5', 'Afq9', 'Cmb5', 'Cxd2', 'Apb8', 'Fqh4', 'Ijv0', 'Ype9', 'Xcx3', 'Vo_7',
        'O_d5', 'Gwa6', 'Edp7', 'Qlb5', 'Bcd2', 'Gpw7', 'Sjv1', 'Ryb6', 'Zpu4', 'Qck8', 'Hrv3', 'Exj3',
        'Kin8', 'Kna4', 'Adz3', 'A__8', 'Ffq1', 'Qwd4', 'Rfe8', 'Ptk3', 'Bmn8', 'Z_o1', 'Ms_5', 'Dcp0',
        'Qo_3', 'Ekx1', 'X_e6', 'Qob3', 'Mgf1', 'Wcy2', 'Zit1', 'Wx_5', 'Vgz5', 'B_x2', 'Eyp8', 'Yzm4',
        'Z_m6', 'Cnf7', 'Rek7', 'Kdb7', 'Ezo6', 'U_x9', 'Etu4', 'Puz3', 'Ece6', 'Irk6', 'Rpn1', 'Flo4',
        'Ylh6', 'Qnk7', 'Dfr5', 'Qh_0', 'Nur3', 'Mtd2', 'Jin7', 'Dd_4', 'Spj0', 'Ztz6', 'A_f8', 'V_k9',
        'Uzg2', 'Svu9', 'Xjv3', 'Afs5', 'Ngk2', 'Eny8', 'Rkf4', 'H_w3', 'Rhi5', 'Ox_7'
    ]
]
G = nx.read_edgelist("big-edgelist", delimiter='-', nodetype=str)
i = 0
ncolor = []
for node in G.nodes:
    if node == h[0]:
        ncolor.append('green')
    elif node == h[1]:
        ncolor.append('red')
    elif node in paths[0]:
        ncolor.append('orange')
    elif node in paths[1]:
        ncolor.append('magenta')
    elif node in paths[2]:
        ncolor.append('cyan')
    else:
        ncolor.append('grey')
    i += 1
print("Total Nodes: " + str(i))
ecolor = []
for edge in G.edges:
    if (edge[0] in paths[0] and edge[1] in paths[0]) or (edge[0] in h and edge[1] in paths[0]) or (edge[0] in paths[0] and edge[1] in h):
        G[edge[0]][edge[1]]['weight'] = 10
        ecolor.append('orange')
    elif (edge[0] in paths[1] and edge[1] in paths[1]) or (edge[0] in h and edge[1] in paths[1]) or (edge[0] in paths[1] and edge[1] in h):
        ecolor.append('magenta')
        G[edge[0]][edge[1]]['weight'] = 10
    elif (edge[0] in paths[2] and edge[1] in paths[2]) or (edge[0] in h and edge[1] in paths[2]) or (edge[0] in paths[2] and edge[1] in h):
        ecolor.append('cyan')
        G[edge[0]][edge[1]]['weight'] = 10
    else:
        ecolor.append('grey')
        G[edge[0]][edge[1]]['weight'] = 1
num_edges = len(G.edges)
print("num_edges: " + str(num_edges) + " len(ecolor): " + str(len(ecolor)))
nx.draw_networkx(G, pos=nx.spectral_layout(G), node_size=100, font_size=6, node_color=ncolor, edge_color=ecolor, with_labels=False)
plt.show()
exit(0)
