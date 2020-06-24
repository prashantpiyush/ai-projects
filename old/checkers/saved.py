'''
Created on Oct 15, 2018

@author: prashant
'''

def move(x, y):
    global t, screen, sel
    t = canvas_turtle.clone()
    canvas_turtle.hideturtle()
    screen = t.getscreen()
    t.clear()
    sel = t.clone()
    screen.clear()
    screen.tracer(0)
    
    o = (-150, -400)
    o = (o[0]+50, o[1]+450)
    
    global hor, ver, radius
    hor = 50
    ver = 100
    radius = 15
    t.setpos(*o)
    t.width(3)
    
    def line(x,y,a,b):
        t.penup()
        t.setpos(x, y+radius)
        t.pendown()
        t.setpos(a,b+radius)
    
    t.pencolor("#00b16a")
    for i in range(1, 6):
        x = o[0]+abs(i-3)*hor
        y = o[1]-(i-1)*ver
        n = 6 - abs(i-3)
        for j in range(n):
            cx = x+2*j*hor
            if j>0:
                line(cx, y, x+2*(j-1)*hor, y)
            if i<3:
                lx = o[0]+abs(i+1-3)*hor+2*j*hor
                ly = o[1]-i*ver
                line(cx, y, lx, ly)
                rx = o[0]+abs(i+1-3)*hor+2*(j+1)*hor
                line(cx, y, rx, ly)
            elif i<5:
                ly = o[1]-i*ver
                if j!=0:
                    lx = o[0]+abs(i+1-3)*hor+2*(j-1)*hor
                    line(cx, y, lx, ly)
                if j!=n-1:
                    rx = o[0]+abs(i+1-3)*hor+2*j*hor
                    line(cx, y, rx, ly)
    t.pencolor("#00b5cc")
    global centers, selected, pcol
    pcol = ['#049372', '#34495e', 'white']
    selected = None
    centers = {}
    pos = []
    for i in range(1, 6):
        x = o[0]+abs(i-3)*hor
        y = o[1]-(i-1)*ver
        n = 6 - abs(i-3)
        p = []
        for j in range(n):
            t.penup()
            t.setpos(x+2*j*hor, y)
            #print (x+2*j*hor, y)
            centers[(x+2*j*hor, y+radius)] = 0
            p.append((x+2*j*hor, y+radius))
            t.pendown()
            t.fillcolor('white')
            t.begin_fill()
            t.circle(radius)
            t.end_fill()
        pos.append(p)
    # Don't delete this line. why?
    # because its magic.
    t.penup()
     
    p1_pos = [(0, 0),
              (1, 0), (1, 1), (1, 2), (1, 4),
              (2, 0), (2, 3), (2, 5),
              (3, 2),
              (4, 0)]
    p2_pos = [(0, 2), (0, 3),
              (1, 3),
              (2, 1), (2, 2), (2, 4),
              (3, 4),
              (4, 1), (4, 2), (4, 3)]
    t.pencolor('#00b5cc')
    for x, y in p1_pos:
        centers[pos[x][y]] = 1
        color(pos[x][y], 0)
    for x, y in p2_pos:
        centers[pos[x][y]] = 2
        color(pos[x][y], 1)
        
        
        
        
        
    def successor_function(self, state, player):
        centers = state
        steps = [(-2*self.hor, 0), (2*self.hor, 0), (-self.hor, self.ver),
                 (-self.hor, -self.ver), (self.hor, self.ver), (self.hor, -self.ver)]
        random.shuffle(steps)
        for pos in centers.keys():
            if centers[pos] != player:
                continue
            for dx, dy in steps:
                try:
#                     nxt = (pos[0]+dx, pos[1]+dy)
#                     if centers[nxt] == 0:
#                         centers[pos], centers[nxt] = 0, player
#                         yield centers
#                         centers[pos], centers[nxt] = player, 0
#                     mid = nxt
#                     nxt = (mid[0]*2, mid[1]*2)
#                     if centers[nxt]==0 and centers[mid]!=player:
#                         centers[pos], centers[nxt] = 0, player
#                         yield centers
#                         centers[pos], centers[nxt] = player, 0
                    x = 3 #random.randint(0, 100)
                    if x%2==0:
                        nxt = (pos[0]+dx, pos[1]+dy)
                        if centers[nxt] == 0:
                            centers[pos], centers[nxt] = 0, player
                            yield centers
                            centers[pos], centers[nxt] = player, 0
                        mid = nxt
                        nxt = (mid[0]*2, mid[1]*2)
                        if centers[nxt]==0 and centers[mid]!=player:
                            centers[pos], centers[nxt] = 0, player
                            yield centers
                            centers[pos], centers[nxt] = player, 0
                    else:
                        mid = (pos[0]+dx, pos[1]+dy)
                        try:
                            nxt = (mid[0]*2, mid[1]*2)
                            if centers[nxt]==0 and centers[mid]!=player and centers[mid]!=0:
                                centers[pos], centers[nxt] = 0, player
                                yield centers
                                centers[pos], centers[nxt] = player, 0
                        except: pass
                        if centers[mid] == 0:
                            centers[pos], centers[mid] = 0, player
                            yield centers
                            centers[pos], centers[mid] = player, 0
                except:
                    pass
        # end of function
        
def minmax():
    global t, screen, sel
    t = canvas_turtle.clone()
    canvas_turtle.hideturtle()
    screen = t.getscreen()
    t.clear()
    sel = t.clone()
    screen.clear()
    screen.tracer(0)
     
    o = (-150, -400)
    o = (o[0]+50, o[1]+450)
     
    global hor, ver, radius
    hor = 50
    ver = 100
    radius = 15
    t.setpos(*o)
    t.width(3)
     
    def line(x,y,a,b):
        t.penup()
        t.setpos(x, y+radius)
        t.pendown()
        t.setpos(a,b+radius)
     
    t.pencolor("#00b16a")
    for i in range(1, 6):
        x = o[0]+abs(i-3)*hor
        y = o[1]-(i-1)*ver
        n = 6 - abs(i-3)
        for j in range(n):
            cx = x+2*j*hor
            if j>0:
                line(cx, y, x+2*(j-1)*hor, y)
            if i<3:
                lx = o[0]+abs(i+1-3)*hor+2*j*hor
                ly = o[1]-i*ver
                line(cx, y, lx, ly)
                rx = o[0]+abs(i+1-3)*hor+2*(j+1)*hor
                line(cx, y, rx, ly)
            elif i<5:
                ly = o[1]-i*ver
                if j!=0:
                    lx = o[0]+abs(i+1-3)*hor+2*(j-1)*hor
                    line(cx, y, lx, ly)
                if j!=n-1:
                    rx = o[0]+abs(i+1-3)*hor+2*j*hor
                    line(cx, y, rx, ly)
    t.pencolor("#00b5cc")
    
    
    
    
def minmax(self, state, color, screen):
        print "Calculating next move using minmax algo..."
        if self.terminal_test(state):
#             print "Game Over"
            return None, None
        minv = 0
        cs = None
        self.color = color
        self.screen = screen
        self.iter = 0
        self.vis = {self.compress(state):True}
        depth = 3
        for child in self.successor_function(copy.deepcopy(state), 2):
            if cs is None:
                minv = self.dfs(copy.deepcopy(child), True, depth)
                cs = copy.deepcopy(child)
            else:
                if self.compress(child) in self.vis:
                    continue
                value = self.dfs(copy.deepcopy(child), True, depth)
                if value < minv:
                    minv = value
                    cs = copy.deepcopy(child)
        p, n = None, None
        print minv
        for pos in state:
            if state[pos]==2 and cs[pos]==0:
                p = pos
            elif state[pos]==0 and cs[pos]==2:
                n = pos
#         m = ((p[0]+n[0])/2, (p[1]+n[1])/2)
#         if m in state:
#             if state[m]!=0:
#                 print "Capture @", m
        return p, n
    
    def dfs(self, state, max_player, depth):
        self.iter += 1
        if self.terminal_test(state) or depth<=0:
            return self.utility_value(state)
        self.vis[self.compress(state)] = True
        if max_player:
            value = -1000
            for child in self.successor_function(state, 1):
                if self.compress(child) in self.vis:
                    continue
                value = max(value, self.dfs(child, False, depth-1))
            return value
        else:
            value = 1000
            for child in self.successor_function(state, 2):
                if self.compress(child) in self.vis:
                    continue     
                value = min(value, self.dfs(child, True, depth-1))
            return value