#!/usr/bin/env python3
try:
    import sys
    import json
    import networkx as nx
    import contextlib
    with contextlib.redirect_stdout(None):
        import scipy
        import matplotlib.pyplot as plt
except:
    print("Ensure that the required modules are installed")
    exit(1)

#lines = [line.rstrip('\n') for line in file]
ANTS_ERR = 1
ROOM_ERR = 2
CONN_ERR = 3
MOVE_ERR = 4
READ_ERR = 5

class Lemon:

    def __init__(self):
        self.name = ""
        self.G = nx.Graph()
        self.num_ants = 0
        self.antmap = {}
        self.roommap = {}
        self.antmoves = []
        self.nodes_colors = []
        self.edges_colors = []

    def add_room(self, line, start_end):
        n = line.split(' ')
        if start_end == -1:
            self.G.add_node(n[0], color='red')
        elif start_end == 1:
            self.G.add_node(n[0], color='green')
        else:
            self.G.add_node(n[0], color='grey')

    def add_edge(self, line):
        n = line.split('-')
        self.G.add_edge(n[0], n[1], color='grey')

    def readinput(self):
        start_end = 0
        lines = [line.rstrip('\n') for line in sys.stdin]
        num_lines = len(lines)
        n = 0
        while n < num_lines and '-' not in lines[n]:
            if n == 0:
                self.num_ants = int(lines[0])
                n+=1
                continue
            if lines[n][0] == '#':
                if lines[n] == '##start':
                    start_end = 1
                elif lines[n] == '##end':
                    start_end = -1
                else:
                    start_end = 0
                n+=1
                continue
            else:
                self.add_room(lines[n], start_end)
        while n < num_lines and '-' in lines[n]:
            if lines[n][0] != 'L':
                self.add_edge(lines[n])
            else:
                self.antmoves.append(lines[n])

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

def lem_to_json(filename):
    f = open("gen_flow_one", 'r')
    lines = [line.rstrip('\n') for line in f]
    l = 1
    g = 0
    line_num = len(lines)
    nodes = []
    while l < line_num and '-' not in lines[l]:
        g = 2
        if lines[l][0] == '#':
            if lines[l] == "##start":
                g = 0
            elif lines[l] == "##end":
                g = 1
            l += 1
            continue
        else:
            nodes.append({"id": lines[l].split(' ')[0], "group": g})
        l += 1
    edges = []
    while l < line_num and '-' in lines[l]:
        if lines[l][0] == '#':
            pass
        else:
            tmp = lines[l].split('-')
            edges.append({"source": tmp[0], "target": tmp[1], "value": 2})
        l += 1
    out = open("flone_json", 'x')
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
            '#f08c00','#308bc0','#f9c030','grey']
# h = ['Xgj7','I_w2']
def soup():
    h = ['Ixl3','Eoi4']
    paths = [[
        'Ruy5', 'Jtw5', 'Nya5', 'Vxb5', 'Amz7', 'A_p4', 'Jxj6', 'Gml4', 'Azz8',
        'Nrl0', 'Bbq5', 'Vyn4', 'Ar_2', 'Eja8', 'Fo_7', 'Nn_7', 'Oaf5', 'Ava9',
        'Bj_2', 'Oav6', 'Jck8', 'Hmb2', 'Buj3', 'Msr7', 'Wyc8', 'Ete4', 'Zj_2',
        'Wlw7', 'Mrn1', 'Cf_2', 'Yh_5', 'Yne8', 'Okv1', 'Tbm3', 'Zra5', 'Jll4',
        'Mxg2', 'Qko0', 'Fad2', 'Oud2', 'Czo6', 'Ten1', 'Arm4', 'Mpv3', 'Bvm2',
        'Fvz3', 'Uil0', 'Fmt3', 'Zre5', 'X__0', 'Vjp7', 'Mk_8', 'T_x5', 'Rcd1',
        'Zhs1', 'Ku_9', 'Kuy2', 'Qf_7', 'Sfp4', 'Qep3', 'Rii3', 'Cvt6', 'Djs2',
        'Qhw7', 'Wvq0', 'Zbg2', 'Wnq2', 'Abl1', 'Nd_8', 'Njv2', 'Yav6', 'Ib_3',
        'Yto9', 'Ks_5', 'Bwj9', 'Xcx2', 'Cqi5', 'Vpt1', 'Bbv2', 'Wjq2', 'Sen1',
        'P_z6', 'Eeq6', 'Ifa2', 'Vzr5', 'Gs_3', 'Ctc8', 'Vfw8', 'Ezr9', 'Vwf5',
        'Zzg2', 'Pww7', 'U_v2', 'Xau8', 'Qzz1', 'Aho2', 'Xsa7', 'Miv8', 'Nfh3',
        'Dx_8', 'Jhb4', 'Eoi4'
    ],[
        'Y_i2', 'J_v9', 'Dcy5', 'Xut9', 'Bnh3', 'Ned3', 'Sfu6', 'Aqk7', 'Eo_0',
        'Vio1', 'Sc_4', 'Ksw4', 'Gzm5', 'Qar1', 'Bjz6', 'Qzt8', 'Jrq2', 'Fab0',
        'Kvu6', 'Oye5', 'Jxk4', 'Ah_0', 'Wfx3', 'Ffq5', 'R_n9', 'Khc5', 'Jur2',
        'Xlj7', 'Xbl1', 'E__7', 'Ubo2', 'Qck1', 'Ttk3', 'Byk1', 'Cme6', 'Jnz8',
        'Vum6', 'Mzv3', 'Nke5', 'Ryg7', 'Ffe2', 'Gkc0', 'Qbx2', 'Qq_3', 'Csm3',
        'Clu7', 'Plf6', 'Yca1', 'Mby8', 'Qth4', 'D__7', 'Flh0', 'Sz_8', 'Amq3',
        'Zzh3', 'Vai0', 'Fgn0', 'Uuo2', 'Yfa1', 'Aum2', 'Uiz9', 'Mhe4', 'Xpa0',
        'Ims2', 'Vuw5', 'D_o7', 'Mfd6', 'Rzm9', 'Hbn9', 'Vu_6', 'Vtc8', 'Qpl6',
        'Eob9', 'Ffi8', 'Osc3', 'Peq6', 'Kgu2', 'Npc4', 'Tkw1', 'Pkn0', 'Jo_0',
        'W_y3', 'Tmd4', 'Zlf0', 'Qez7', 'G_j2', 'Wn_3', 'Mny0', 'Odm4', 'Ciy1',
        'Tv_3', 'Kkb1', 'Rtz8', 'Xqd6', 'Mir8', 'Qj_4', 'Tqj7', 'Ajn2', 'Aue6',
        'Kon8', 'Coc6', 'Isl0', 'Sld2', 'Zy_8', 'Pgn7', 'S_n2', 'Xtc8', 'Zlr0',
        'Een1', 'Ets2', 'Jmu1', 'Ynz4', 'Cvs1', 'Dd_2', 'Isf9', 'Vyd2', 'Yui6',
        'Yax7', 'Zlf6', 'Wli5', 'Dgy7', 'Fif8', 'Pdn0', 'Ywj7', 'Bea1', 'Fvb5',
        'Nak0', 'Wlc8', 'Gxq6', 'B_n8', 'Sar0', 'T_f8', 'Uiv5', 'Eqs0', 'Ovj2',
        'Iph2', 'Ujs0', 'Eip8', 'Npd3', 'Ifc3', 'Ihe7', 'Xk_1', 'D_q1', 'Hhd5',
        'Rtq0', 'Pul7', 'Hhh2', 'Mvf1', 'Wne4', 'Eoi4], [Jwt6', 'Jko3', 'Dex6',
        'Wnm5', 'Rnf0', 'Mdb8', 'Ktm1', 'Jw_6', 'V_h5', 'Wlx2', 'Gdk3', 'Ssl7',
        'Fru3', 'His2', 'Otq7', 'Wrb7', 'Kce8', 'Cmp9', 'Ikp7', 'Evh0', 'Dsr7',
        'Wsz2', 'Rsb9', 'Shf3', 'Gjf5', 'Toz0', 'Toi6', 'Ujn7', 'Hfr4', 'S__3',
        'Aec3', 'Ivn6', 'Mtf4', 'Eok6', 'Uem7', 'Kom3', 'Jil2', 'Pya4', 'Vnn8',
        'Nsz2', 'Bop1', 'Dkh5', 'Kgs4', 'Csv4', 'Zez5', 'Kzp6', 'Y_m2', 'Znn1',
        'Ees2', 'Vsc5', 'Ovz5', 'Ueh6', 'I_h3', 'Oka0', 'Nm_4', 'Ocq9', 'Vxi6',
        'Gm_7', 'Fqo7', 'Eqi4', 'Uis0', 'E_u9', 'Vra3', 'Quv4', 'Vuj0', 'Uy_1',
        'F_l2', 'Ylr5', 'Ev_1', 'Wkr3', 'Moh1', 'Rp_8', 'Vua6', 'Xsn4', 'Ghd7',
        'Y_o2', 'Teu2', 'Nis9', 'Ncg3', 'Ktb9', 'Qfy9', 'Mgr1', 'Jpa3', 'M_q1',
        'Izy0', 'Nmw5', 'Zsk6', 'Roy9', 'Azp4', 'Twc6', 'Bxh5', 'Fkn0', 'Tpj9',
        'Bbs1', 'Ksk5', 'Iwo5', 'Opt5', 'Pss0', 'Gpy9', 'Sx_6', 'Tlf9', 'Jtv1',
        'Owr2', 'Kln9', 'Kff6', 'Qhw9', 'Mlt1', 'Wpf6', 'Rzy8', 'Jty3', 'Sdk4',
        'Vdu6', 'Zjf9', 'Fzb4', 'Z_y0', 'Fmz2', 'Wut9', 'G_u9', 'Ynz0', 'Ew_6',
        'Uee8', 'Ejl1', 'Scv1', 'Hye3', 'Hbl8', 'Brs9', 'Mqz5', 'Q__2', 'Nlo8',
        'Wze3', 'J__8', 'Hdi9', 'Ffr8', 'Ap_9', 'Rmd2', 'Pkz5', 'Oqk4', 'Fbk4',
        'Zyo9', 'Xty5', 'Eoi4'
    ],[
        'Azi6', 'War3', 'Zwi6', 'Efl7', 'Tbi0', 'Utj3', 'Ym_9', 'Nsf2', 'Bvo5',
        'J_w7', 'Mva6', 'Nec6', 'Wwr3', 'Wmv4', 'Pak4', 'Mzj0', 'Mux2', 'Swq2',
        'Tww4', 'Uto4', 'Wec7', 'Uhz5', 'Jin6', 'Zpq9', 'Dv_5', 'Nuu9', 'Cct5',
        'Hna5', 'Bre2', 'Otd4', 'Um_0', 'Sen9', 'Ar_1', 'Eeb5', 'Vck3', 'Tzo9',
        'Smq4', 'Gee3', 'Hlu8', 'Zuu9', 'Q_d4', 'Jmg2', 'E_e4', 'Gve8', 'Vwm1',
        'Sv_7', 'Kfw8', 'Vxi1', 'Vlp3', 'B_o4', 'Nik0', 'Dsx4', 'Gcx2', 'Sk_1',
        'Thd4', 'Qyy2', 'Yvb7', 'Ciq0', 'Upm9', 'Wut0', 'Agp5', 'Rbv9', 'U__8',
        'Oey5', 'Baq6', 'Off3', 'Fjh0', 'Mnb4', 'Cgm3', 'Fnl5', 'Whu6', 'Osz4',
        'Vpi0', 'Due9', 'Axh2', 'Vkp2', 'Rgw9', 'Js_3', 'K_h5', 'G_f9', 'Hsw4',
        'Dsc8', 'Doa0', 'Stj3', 'Idg4', 'Wng7', 'Vny3', 'Xe_1', 'X__3', 'Bnw6',
        'Eoi4'
    ],[
        'Ytx3', 'Drm1', 'Kob5', 'Fgw7', 'Esf0', 'Ukc9', 'Sms9', 'Vgd3', 'Vcc8',
        'J_x6', 'Jiv5', 'Kk_1', 'Alo4', 'Ihm8', 'Pzk8', 'Ecc5', 'Kci2', 'Ari2',
        'Ezc4', 'Tpg8', 'Wsu5', 'H_w7', 'Pch2', 'Q__0', 'Oa_2', 'O_j8', 'Uy_8',
        'Raj8', 'Eoi4'
    ],[
        'Vgd2', 'Cjq7', 'Efy5', 'Msn0', 'Uws3', 'Crt3', 'Fmw1', 'Zhg8', 'Izp9',
        'Zzz2', 'Irr5', 'W__1', 'V_x1', 'Tbh8', 'Qfj5', 'Owg5', 'Wst5', 'Poy3',
        'Mb_4', 'Pth6', 'Aqa8', 'Me_7', 'Hl_2', 'Xxq6', 'Rnb0', 'Ycp9', 'Ye_2',
        'P_o8', 'Zcu0', 'Fvl4', 'Pxe0', 'Wmb9', 'Xby1', 'Imc7', 'Rns2', 'Oje6',
        'B_d7', 'Feb1', 'Goj9', 'Ufz5', 'Prl6', 'Vb_5', 'Uii3', 'R_p1', 'Xxi6',
        'Ht_2', 'Juf7', 'A_g7', 'Cbm5', 'Ssh6', 'Wt_2', 'Eoi4'
    ],[
        'Hff8', 'Yry7', 'Ogs7', 'Kka3', 'Rgq2', 'Pa_2', 'Hmr2', 'Bkc1', 'Ye_0',
        'Fpu3', 'Vsv2', 'Cjy8', 'Zpf3', 'Dlz2', 'Xw_9', 'Tbl1', 'M_j4', 'Zjl1',
        'Mlu6', 'Yqq3', 'Uzj9', 'E_r0', 'Pfz4', 'J_d6', 'Nxn3', 'Wua9', 'M_j7',
        'Hon6', 'Mih9', 'Rzw1', 'Jak6', 'Idl5', 'Vdu0', 'Knn5', 'Cts3', 'Zzz9',
        'Amg2', 'Nsl1', 'Ypd9', 'Qbz2', 'Qak1', 'Shr4', 'Ffw3', 'Ddp9', 'Rl_0',
        'Kfp4', 'Ukt2', 'Dqo9', 'T_d8', 'Vzh9', 'Cqg1', 'Ule9', 'Ykq3', 'W__9',
        'Xfc4', 'Fhq9', 'Eho0', 'Fyl9', 'Pg_8', 'Upy0', 'A_p6', 'Fkd9', 'Dvm7',
        'Tgi1', 'Wsx2', 'Bzu7', 'Xiu8', 'Oil0', 'Pnq1', 'Xcw6', 'T_r6', 'Sps1',
        'Fot4', 'Eon0', 'Isw8', 'Wvt6', 'Tcl3', 'H_l8', 'Wkn5', 'Eoi4'
    ],[
        'Qyw4', 'M_s8', 'Pmh0', 'Prw9', 'Klu0', 'Myy5', 'Jqm6', 'Ume1', 'Gfg8',
        'Tls4', 'Vo_3', 'Jqk5', 'Drx6', 'Czb8', 'Tvh4', 'Mab9', 'P_a4', 'Mek3',
        'B_a2', 'Zwj4', 'Wju5', 'Gek7', 'Vbo4', 'Rhd7', 'Uzr9', 'Eka9', 'Hxp6',
        'Bf_4', 'Kox0', 'Yei2', 'Fko6', 'O_j4', 'Ejm0', 'Jp_7', 'Ugs6', 'Z_x7',
        'Eak9', 'Aqa9', 'Ilh1', 'I_z8', 'Vte4', 'To_9', 'Dta7', 'Iws2', 'O_w7',
        'Csd9', 'Bff2', 'Yv_4', 'Rug8', 'Xtp2', 'Kcc1', 'Jbz0', 'Yrv0', 'Kqc4',
        'Siy4', 'Ruk6', 'S_p6', 'Eap9', 'Jpt9', 'Neh2', 'Ngs1', 'Wmv0', 'Omc0',
        'Ul_0', 'Cqn3', 'Osn7', 'Bxa4', 'Cjj6', 'Nrb6', 'Vat8', 'Eel8', 'Vsb4',
        'Fzm9', 'Vzn9', 'Jsv6', 'R_r3', 'Gvf3', 'Jmh3', 'S_n4', 'Usy0', 'Nsj7',
        'Gbr3', 'Iwy6', 'Tin0', 'Mbv1', 'Owg0', 'Kod3', 'V__5', 'Tg_1', 'Koz9',
        'Paa3', 'Omy4', 'Pc_6', 'F_m6', 'Jg_7', 'Xkq2', 'Kn_1', 'Uqu7', 'Qui1',
        'Rmb8', 'Tzl4', 'Ooa0', 'Pay3', 'Ejo5', 'G_f1', 'Fym3', 'Ul_8', 'Nez8',
        'Ggb5', 'Eoi4'
    ],[
        'Kne2', 'Xpj5', 'Xlt1', 'Bne5', 'Wes5', 'Sib8', 'Mx_0', 'Xkw6', 'Bka9',
        'Bt_0', 'Tzu2', 'M_v1', 'Hyd6', 'Ylm1', 'Uyu6', 'Ob_2', 'Cmc5', 'Fxb2',
        'Ken5', 'Y_l5', 'Uks2', 'M__4', 'Rbh9', 'Thw2', 'Jxd0', 'Kde4', 'Jo_6',
        'Cn_4', 'Kgr9', 'Iqm0', 'N_x6', 'Qtr1', 'Rcp3', 'Bes1', 'Noz2', 'Kru8',
        'Tcc8', 'Woe5', 'Uam8', 'Tvs3', 'Itd8', 'Mvb2', 'Zhs9', 'Fei8', 'Qmy9',
        'A_c2', 'Hic2', 'Rxg4', 'Rio5', 'Qcb9', 'Srs9', 'Qyn4', 'Fly9', 'Ukh8',
        'Uri2', 'Ejl3', 'Tnk1', 'Zpb0', 'Amx5', 'Sq_7', 'Hbr0', 'J_j9', 'Yfg0',
        'Wcy9', 'Fvb8', 'Gn_0', 'Bq_8', 'Mzw5', 'Zeu0', 'Hxw6', 'Ojk4', 'Eje4',
        'K_n1', 'Iob8', 'Rgx0', 'Hgl0', 'Vcf2', 'Dyd2', 'Ov_0', 'Gey4', 'Aaw5',
        'Kvh1', 'Y_i5', 'Cne2', 'Hju9', 'Ewe1', 'Nnk8', 'Klh7', 'Ujm6', 'Sab7',
        'Kls6', 'Rbg7', 'Ysv3', 'Rnv7', 'Wq_4', 'Fkp8', 'Blc7', 'Gyr3', 'Cbn4',
        'Qdu1', 'K_n4', 'Gpx3', 'Ith8', 'Scc6', 'R_k5', 'Wpg3', 'Wyf2', 'Egy5',
        'Vjq4', 'Zcg6', 'Pyf6', 'Snm8', 'Oxw1', 'Xvg3', 'Tkv0', 'K_h8', 'Fvs9',
        'Scg3', 'Uzh8', 'Cvn4', 'Vre9', 'Tm_0', 'Rmh7', 'Wec5', 'Q_p7', 'A_b9',
        'Cbi5', 'Dlu1', 'Uya7', 'Hbo4', 'Sdn4', 'Pp_9', 'Zsz7', 'N_q2', 'Zkb9',
        'Vph4', 'Chr9', 'Xfl4', 'Yfj5', 'Bch9', 'Iks4', 'Udd3', 'Dpc3', 'Cfa2',
        'Zus0', 'Mje2', 'Jd_2', 'J_p7', 'Ndu3', 'Szk9', 'Aqc6', 'Qqg3', 'Cft6',
        'Euo6', 'Nla2', 'Olq4', 'Jsz8', 'Rnn6', 'Kkz6', 'Rjp3', 'Ass9', 'Vjf9',
        'Opk7', 'Rcv3', 'Dxr0', 'Ybh2', 'Dfg1', 'Eoi4'
    ],[
        'Wu_6', 'Zqn7', 'Qhs4', 'Rkx1', 'K_w4', 'Zpy1', 'Ioj0', 'Erl0', 'Rvz9',
        'Yee5', 'Vyu1', 'Fwp8', 'Yw_7', 'Jcx9', 'Vgx2', 'Xkt1', 'D_w1', 'Qac3',
        'W_d1', 'Y_u9', 'Srq2', 'Ivh0', 'Yng9', 'B_v1', 'Tsz8', 'Tn_6', 'Iot0',
        'Pkw4', 'Zun2', 'Bfh5', 'Fyq5', 'Atk4', 'Xai3', 'Tlq5', 'X_z2', 'Mga5',
        'Qli6', 'Fgo6', 'Ycd7', 'Gsr4', 'Jkh0', 'Krg5', 'Svj7', 'Eoi4'
    ]]
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
            G[edge[0]][edge[1]]['weight'] = 10
            ecolor.append(col_path[2])
        elif (edge[0] in paths[1] and edge[1] in paths[1]) or (edge[0] in h and edge[1] in paths[1]) or (edge[0] in paths[1] and edge[1] in h):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[2] and edge[1] in paths[2]) or (edge[0] in h and edge[1] in paths[2]) or (edge[0] in paths[2] and edge[1] in h):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[3] and edge[1] in paths[3]) or (edge[0] in h and edge[1] in paths[3]) or (edge[0] in paths[3] and edge[1] in h):
            ecolor.append(col_path[5])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[4] and edge[1] in paths[4]) or (edge[0] in h and edge[1] in paths[4]) or (edge[0] in paths[4] and edge[1] in h):
            ecolor.append(col_path[6])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[5] and edge[1] in paths[5]) or (edge[0] in h and edge[1] in paths[5]) or (edge[0] in paths[5] and edge[1] in h):
            ecolor.append(col_path[7])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[6] and edge[1] in paths[6]) or (edge[0] in h and edge[1] in paths[6]) or (edge[0] in paths[6] and edge[1] in h):
            ecolor.append(col_path[8])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[7] and edge[1] in paths[7]) or (edge[0] in h and edge[1] in paths[7]) or (edge[0] in paths[7] and edge[1] in h):
            ecolor.append(col_path[9])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in paths[8] and edge[1] in paths[8]) or (edge[0] in h and edge[1] in paths[8]) or (edge[0] in paths[8] and edge[1] in h):
            ecolor.append(col_path[10])
            G[edge[0]][edge[1]]['weight'] = 10
        else:
            edges_remove.append(edge)
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    # G.remove_edges_from(edges_remove)
    # G.remove_nodes_from(nodes_remove)
    # edges_remove = set(edges_remove)
    # k = 0
    # for i in range(len(edges_remove)):
    #     for j in range(len(edges_remove)):
    #         if i != j and edges_remove[i] == edges_remove[j]:
    #             G.remove_edge(edges_remove[j])
    #             G.remove_edge(edges_remove[i])
    #             k += 1
    # newcolors = []
    # for ec in ecolor:
    #     if ec != "grey":
    #         newcolors.append(ec)
    #     else:
    #         G.remove_node(edge[0])
    #         G.remove_node(edge[1])
    #         G.remove_nodes_from(edge)
    num_edges = len(G.edges)
    num_nodes = len(G.nodes)
    print("num_nodes: " + str(num_nodes))
    print("num_edges: " + str(num_edges) + " len(ecolor): " + str(len(ecolor)))
    nx.draw_networkx(G, pos=nx.spectral_layout(G), node_size=10, node_color=ncolor, edge_color=ecolor, with_labels=False)
    plt.show()

def big():
    bh = ['Pqz1','Ox_7']
    bpaths = [[
        'Ouc9', 'Mgt4', 'Grq1', 'Xdu6', 'X_j2', 'Jdz3', 'Pmf9', 'Ohf5', 'Ref9',
        'Tfv0', 'Kux7', 'Xwa7', 'Kky8', 'Rrc3', 'Epw2', 'Vak8', 'Yiq5', 'Ijy6',
        'Rlj1', 'Opr4', 'Nxb0', 'Wfg5', 'J_v3', 'Xtm4', 'Kwk2', 'D_o7', 'Nmq0',
        'Hx_4', 'Cc_4', 'Wl_2', 'M_h5', 'Mjd8', 'Mue5', 'Fxr7', 'Yzm4', 'U_x9',
        'Atz1', 'Plm5', 'Pmd2', 'Chl2', 'Etu4', 'Ylh6', 'Zxi1', 'W_c1', 'Esz0',
        'Wp_4', 'F_h2', 'Ghf3', 'Sdc4', 'Npw3', 'Pji1', 'Nvx3', 'Pip8', 'Xsv2',
        'Yjy8', 'Xry6', 'Eht1', 'Igg2', 'Rmf2', 'Ox_7'
    ],[
        'Usy7', 'X_o7', 'Jsc7', 'Eeb6', 'Rvp1', 'Oc_8', 'Pj_4', 'Dka8', 'Iqq7',
        'Yxz6', 'Kcv8', 'Ziz9', 'Kku5', 'Z_d3', 'Yfs6', 'Q_o6', 'Kzw7', 'Mgx0',
        'Daf1', 'Fab8', 'Axl5', 'Crm2', 'Zop2', 'Yix5', 'Iun5', 'K_p5', 'Ydl9',
        'Eu_2', 'Wmr8', 'Tfv0', 'Hiz8', 'Yal9', 'Kux7', 'W_y5', 'Pfs2', 'Ycl1',
        'Xwa7', 'Epw2', 'Ijy6', 'J_v3', 'D_o7', 'Cc_4', 'Gkl7', 'Mvi4', 'Wl_2',
        'Asu3', 'Wxx5', 'M_h5', 'Hua0', 'F_k2', 'Yos4', 'Fq_4', 'Eux1', 'Bua1',
        'G_o1', 'Ox_7'
    ],[
        'Mad0', 'Zyf5', 'R_j5', 'Afq9', 'Cmb5', 'Cxd2', 'Apb8', 'Fqh4', 'Ijv0',
        'Ype9', 'Xcx3', 'Vo_7', 'O_d5', 'Gwa6', 'Edp7', 'Qlb5', 'Bcd2', 'Gpw7',
        'Sjv1', 'Ryb6', 'Zpu4', 'Qck8', 'Hrv3', 'Exj3', 'Kin8', 'Kna4', 'Adz3',
        'A__8', 'Ffq1', 'Qwd4', 'Rfe8', 'Ptk3', 'Bmn8', 'Z_o1', 'Ms_5', 'Dcp0',
        'Qo_3', 'Ekx1', 'X_e6', 'Qob3', 'Mgf1', 'Wcy2', 'Zit1', 'Wx_5', 'Vgz5',
        'B_x2', 'Eyp8', 'Yzm4', 'Z_m6', 'Cnf7', 'Rek7', 'Kdb7', 'Ezo6', 'U_x9',
        'Etu4', 'Puz3', 'Ece6', 'Irk6', 'Rpn1', 'Flo4', 'Ylh6', 'Qnk7', 'Dfr5',
        'Qh_0', 'Nur3', 'Mtd2', 'Jin7', 'Dd_4', 'Spj0', 'Ztz6', 'A_f8', 'V_k9',
        'Uzg2', 'Svu9', 'Xjv3', 'Afs5', 'Ngk2', 'Eny8', 'Rkf4', 'H_w3', 'Rhi5',
        'Ox_7'
    ]]
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
            G[edge[0]][edge[1]]['weight'] = 10
            ecolor.append(col_path[2])
        elif (edge[0] in bpaths[1] and edge[1] in bpaths[1]) or (edge[0] in bh and edge[1] in bpaths[1]) or (edge[0] in bpaths[1] and edge[1] in bh):
            ecolor.append(col_path[3])
            G[edge[0]][edge[1]]['weight'] = 10
        elif (edge[0] in bpaths[2] and edge[1] in bpaths[2]) or (edge[0] in bh and edge[1] in bpaths[2]) or (edge[0] in bpaths[2] and edge[1] in bh):
            ecolor.append(col_path[4])
            G[edge[0]][edge[1]]['weight'] = 10
        else:
            edges_remove.append(edge)
            ecolor.append(col_path[11])
            G[edge[0]][edge[1]]['weight'] = 1
    # G.remove_edges_from(edges_remove)
    # G.remove_nodes_from(nodes_remove)
    # edges_remove = set(edges_remove)
    # k = 0
    # for i in range(len(edges_remove)):
    #     for j in range(len(edges_remove)):
    #         if i != j and edges_remove[i] == edges_remove[j]:
    #             G.remove_edge(edges_remove[j])
    #             G.remove_edge(edges_remove[i])
    #             k += 1
    # newcolors = []
    # for ec in ecolor:
    #     if ec != "grey":
    #         newcolors.append(ec)
    #     else:
    #         G.remove_node(edge[0])
    #         G.remove_node(edge[1])
    #         G.remove_nodes_from(edge)
    num_edges = len(G.edges)
    num_nodes = len(G.nodes)
    print("num_nodes: " + str(num_nodes))
    print("num_edges: " + str(num_edges) + " len(ecolor): " + str(len(ecolor)))
    nx.draw_networkx(G, pos=nx.spectral_layout(G), node_size=10, node_color=ncolor, edge_color=ecolor, with_labels=False)
    plt.show()

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'big':
            big()
        elif sys.argv[1] == 'soup':
            soup()
    else:
        loops = Lemon()
        try:
            loops.read_input()
        except FileNotFoundError:
            print_err(READ_ERR)
        #TODO: Lemon.draw_graph()

if __name__ == '__main__':
    main()
