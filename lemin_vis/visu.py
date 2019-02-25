#!/usr/bin/env python3

try:
    import sys
    import random
    import re
    import networkx as nx
    import pytweening
    import contextlib
    with contextlib.redirect_stdout(None):
        import pygame
        from pygame.locals import *
except:
    print("Import error")
    print("""Please make sure these libraries are correctly available:
* pygame
* pytweening
* networkx""")
    exit(1)

FPS = 30

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
BLACK    = (  0,   0,   0)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
VIOLET   = (110,  60, 135)
DGREEN   = (165, 105, 178)
MUSTARD  = (229, 137, 100)
ORANGE   = (206,  90,  57)
DPURPLE  = ( 41,  50,  65)

GREEN    = ( 79, 255, 151)
DGREEN   = ( 15,  91,  82)
PINK     = (220,  40,  90)
DPINK    = (111,  29,  74)

BGCOLOR = (245,222,179)
ANTCOLOR = BLACK
# ROOMCOLOR = PURPLE
ROOMCOLOR = (165, 27, 27)
# STARTCOLOR = (250, 30, 30)
STARTCOLOR = ROOMCOLOR
# ENDCOLOR = (255, 150, 79)
ENDCOLOR = MUSTARD
CONNCOLOR = MUSTARD

ANTS_ERR = 1
ROOM_ERR = 2
CONN_ERR = 4
MOVE_ERR = 8
READ_ERR = 16

WINDOWWIDTH = 1000
WINDOWHEIGHT = 1000

class Ant:

    def __init__(self, name, start):
        self.name = name
        self.x, self.y = start
        self.img = pygame.image.load("/dev/urandom")
        self.n = 0
        self.move_list = None
        self.step = 1

    def __str__(self):
        return ("Ant name %s x %f y %d" % (self.name, self.x, self.y))

    def start_move(self, end_coords):
        self.move_list = pytweening.getLine(self.x, self.y, end_coords[0], end_coords[1])
        self.move_list.append(end_coords)

    def move(self, step=1, instamove=0):
        if instamove:
            if self.move_list:
                self.x, self.y = self.move_list[-1]
                self.move_list = None
            return 0
        if self.move_list == None:
            self.n = 0
            return 0
        self.n = self.n + self.step
        if self.n >= len(self.move_list) - 1:
            self.x, self.y = self.move_list[-1]
            self.move_list = None
            self.n = 0
            return 0
        else:
            self.x, self.y = self.move_list[self.n]
            return 1

class Room:

    def __init__(self, name, coords, roomsize, start_end=0):
        self.name = name
        self.x, self.y = coords
        self.start_end = start_end  # start = -1; end = 1; other = 0
        self.conns = {}
        self.disp_x = self.x * 5
        self.disp_y = self.y * 5
        self.roomsize = roomsize
        self.center = (self.disp_x + self.roomsize/ 2, self.disp_y + self.roomsize / 2)

    def __str__(self):
        return ("Room %s start_end %d pos (%d, %d)" % (self.name, self.start_end, self.x, self.y))

    def add_conn(new):
        self.conns[new.name] = new

class Game:

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(150, 5)
        self.clock = pygame.time.Clock()
        self.surf = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
        pygame.display.set_caption("lem-in visualizer\n")
        self.fps = FPS
        self.roomsize = 16
        self.num_ants = None
        self.room_max_x = None
        self.room_max_y = None
        self.room_min_x = None
        self.room_min_y = None
        self.roommap = {}
        self.antmap = {}
        self.move_num = 0
        self.inc = 1
        self.ant_moves = []
        self.start = None
        self.end = None
        self.ants_moving = 0
        self.instamove = 0

    def __str__(self):
        try:
            return "Num_ants %d max_x %d max_y %d min_x %d min_y %d" % (self.num_ants, self.room_max_x, self.room_max_y, self.room_min_x, self.room_min_y)
        except TypeError:
            return "Type error"

    def events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                self.quit()
            if self.event.type == KEYDOWN:
                if self.event.key == K_ESCAPE or self.event.key == K_q:
                    self.quit()
                if self.event.key == K_RIGHT and not self.ants_moving:
                    self.move_num = min(self.move_num + self.inc, len(self.ant_moves) - 1)
                if self.event.key == K_UP:
                    for n in self.antmap:
                        self.antmap[n].step += 1
                if self.event.key == K_DOWN:
                    for n in self.antmap:
                        self.antmap[n].step = max(self.antmap[n].step - 1, 1)
                if (self.event.key == K_HOME or self.event.key == K_r) and not self.ants_moving:
                    for n in self.antmap:
                        self.antmap[n].x, self.antmap[n].y = self.start.center
                        self.antmap[n].n = 0
                        self.antmap[n].step = 1
                    self.move_num = 0
                if self.event.key == K_0 or self.event.key == K_KP0:
                    for n in self.antmap:
                        self.antmap[n].step = 1
                if self.event.key == K_i:
                    self.instamove = ~self.instamove

    def add_conn(self, line):
        n = line.split('-')
        try:
            self.roommap[n[0]].conns[n[1]] = self.roommap[n[1]]
            self.roommap[n[1]].conns[n[0]] = self.roommap[n[0]]
        except KeyError:
            print_err(CONN_ERR)

    def add_room(self, line, start_end):
        n = line.split(' ')
        new = Room(n[0], (int(n[1]), int(n[2])), self.roomsize, start_end)
        if start_end == -1:
            self.start = new
        elif start_end == 1:
            self.end = new
        if self.room_max_y == None or self.room_max_y < new.y:
            self.room_max_y = new.y
        if self.room_max_x == None or self.room_max_x < new.x:
            self.room_max_x = new.x
        if self.room_min_y == None or new.y < self.room_min_y:
            self.room_min_y = new.y
        if self.room_min_x == None or new.x < self.room_max_x:
            self.room_min_x = new.x
        try:
            if self.roommap[new.name]:
                print_err(ROOM_ERR)
        except:
            self.roommap[new.name] = new

    def draw_rooms(self):
        for rname in self.roommap:
            if self.roommap[rname].start_end == -1:
                room_color = STARTCOLOR
            elif self.roommap[rname].start_end == 1:
                room_color = ENDCOLOR
            else:
                room_color = ROOMCOLOR
            pygame.draw.rect(self.surf, room_color, (self.roommap[rname].disp_x, self.roommap[rname].disp_y, self.roommap[rname].roomsize, self.roommap[rname].roomsize))
            if self.roommap[rname].start_end == -1:
                rm = self.roommap[rname]
                pygame.draw.lines(self.surf, MUSTARD, True, ((rm.disp_x, rm.disp_y), (rm.disp_x + rm.roomsize, rm.disp_y), (rm.disp_x + rm.roomsize, rm.disp_y + rm.roomsize), (rm.disp_x, rm.disp_y + rm.roomsize)), 3)

    def draw_connections(self):
        for rname in self.roommap:
            room_a = self.roommap[rname]
            for cname in room_a.conns:
                room_b = self.roommap[cname]
                pygame.draw.line(self.surf, CONNCOLOR, room_a.center, room_b.center, 2)

    def read_input(self):
        lines = [n.rstrip() for n in sys.stdin]
        for n in lines:
            print(n)
        linum = len(lines)
        n = 0
        start_end = 0
        room_p = re.compile("(?:(?:[a-zA-Z0-9_]+ \d+ \d+$)|(?:^#))")
        try:
            self.num_ants = int(lines[n])
            n += 1
        except:
            print_err(ANTS_ERR)
        while n < linum and room_p.match(lines[n]):
            if lines[n][0] == '#':
                if lines[n] == '##start':
                    start_end = -1
                elif lines[n] == '##end':
                    start_end = 1
                n += 1
                continue
            else:
                self.add_room(lines[n], start_end)
            start_end = 0
            n += 1
        conn_p = re.compile("(?:(?:^[a-zA-Z0-9_]+-[a-zA-Z0-9_]+$)|(?:^#))")
        while n < linum and conn_p.match(lines[n]):
            if lines[n][0] == '#':
                pass
            else:
                self.add_conn(lines[n])
            n += 1
        move_p = re.compile("^(?:L[0-9]+-[a-zA-Z0-9_]+ ?)+$")
        if n == linum or lines[n] != '':
            print_err(ANTS_ERR)
        n += 1
        while n < linum and move_p.match(lines[n]):
            self.ant_moves.append(lines[n])
            n += 1
        if n != linum:
            print_err(ANTS_ERR)
        self.ant_moves = [[]] + self.ant_moves
        for n in range(self.num_ants):
            name = 'L' + str(n + 1)
            self.antmap[name] = Ant(name, self.start.center)

    def display_ant(self, ant):
        img_rect = ant.img.get_rect()
        img_rect.center = (ant.x, ant.y)
        self.surf.blit(ant.img, img_rect)

    def draw_ants(self):
        for n in self.antmap:
            self.display_ant(self.antmap[n])

    def move_ants(self):
        for n in self.antmap:
            self.ants_moving += self.antmap[n].move(self.antmap[n].step, self.instamove)

    def update_ants(self):
        line = self.ant_moves[self.move_num]
        if line == []:
            return
        split_line = [n.split('-') for n in line.split(' ')]
        for n in split_line:
            if len(n) != 2:
                print_err(ANTS_ERR)
            try:
                self.antmap[n[0]].start_move(self.roommap[n[1]].center)
            except:
                print_err(MOVE_ERR)

    def quit(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        self.ants_moving = 0
        self.surf.fill(BGCOLOR)
        self.draw_connections()
        self.draw_rooms()
        self.update_ants()
        self.move_ants()
        self.draw_ants()
        pygame.display.update()

    def run(self):
        while 1:
            self.clock.tick(self.fps)
            self.events()
            self.draw()

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

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print("""Navigation:
Esc, Q  : quit visualizer
Up      : increase ant speed
Down    : decrease ant speed
Right   : move ants
0       : reset ant speed
I       : toggle instant ant movement
Home, R : reset""")
            sys.exit()
        else:
            print("illegal option: %s" % (sys.argv[1]))
            print("usage: ./lem-in < test_file | ./visu [--help]")
            sys.exit(1)
    g = Game()
    try:
        g.read_input()
    except FileNotFoundError:
        print_err(READ_ERR)
    g.run()

if __name__ == "__main__":
    main()
