'''
Created on Sep 26, 2018

@author: prashant
'''

def astarx():
    o = (-115, -110)
    global t
    t.clear()
    screen = t.getscreen()
    screen.clear()
    screen.tracer(0)
    t.hideturtle()
    t.pencolor('grey')
    size, w = 30, 30
    
    x = -30
    for i in range(0, 30):
        t.penup()
        t.setpos(o[0]+x, 300)
        t.pendown()
        t.setpos(o[0]+x, -300)
        t.penup()
        t.setpos(300, o[1]+x)
        t.pendown()
        t.setpos(-300, o[1]+x)
        x += size
    screen.update()
    
    # init pos
    pos = [(0, 0), (0, 1), (2, 0), (2, 1), (1, 0), (3, 0)]
    label = []
    
    box = []
    old = []
    for i in range(len(pos)):
        box.append((o[0]+pos[i][0]*(size+w), o[1]+pos[i][1]*size))
        old.append((o[0]+pos[i][0]*(size+w), o[1]+pos[i][1]*size))
        lt = t.clone()
        lt.hideturtle()
        lt.pencolor('red')
        lt.penup()
        label.append(lt)
    
    def draw_boxes():
        t.pencolor('red')
        for i in range(len(box)):
            x, y = box[i]
            t.penup()
#             print i, x != old[i][0] or y != old[i][1]
#             if x != old[i][0] or y != old[i][1]:
            label[i].clear()
            label[i].setpos(x+size/2, y+size/2)
            label[i].write(str(i+1))
            t.setpos(x, y)
            t.pendown()
            t.fillcolor('white')
            t.begin_fill()
            t.setpos(x, y+30)
            t.setpos(x+30, y+30)
            t.setpos(x+30, y)
            t.setpos(x, y)
            t.end_fill()
    def draw_crane():
        t.color('black')
        t.fillcolor('black')
        cw = 5
        t.penup()
        t.setpos(*crane)
        t.pendown()
        t.begin_fill()
#         t.setpos(crane[0]+size/2-1, crane[1])
#         t.setpos(crane[0]+size/2-1, crane[1]+500)
#         t.setpos(crane[0]+size/2+1, crane[1]+500)
#         t.setpos(crane[0]+size/2+1, crane[1])
#         t.setpos(crane[0],          crane[1])
        t.setpos(crane[0]+size,     crane[1])
        t.setpos(crane[0]+size,     crane[1]-size)
        t.setpos(crane[0]+size+cw,  crane[1]+cw)
        t.setpos(crane[0]-cw,       crane[1]+cw)
        t.setpos(crane[0],          crane[1]-size)
        t.setpos(crane[0],          crane[1])
        t.end_fill()
    def draw():
        t.clear()
        t.color('grey')
        x = -30
        for i in range(0, 30):
            t.penup()
            t.setpos(o[0]+x, 300)
            t.pendown()
            t.setpos(o[0]+x, -300)
            t.penup()
            t.setpos(300, o[1]+x)
            t.pendown()
            t.setpos(-300, o[1]+x)
            x += size
        draw_boxes()
        draw_crane()
        screen.update()
    # done
    
    moves = [(1, 3, 1), (1, 2, 2), (0, 2, 3), (5, 1, 1), (0, 1, 2)]
    mx = 5
    speed = 0.8
    crane = (o[0], o[1]+(mx+1)*size)
    for move in moves:
        idx, r, c = move
        # get crane to correct pos
        while crane[1] != o[1]+(mx+1)*size:
            x, y = crane
            mult = 1 if y <= o[1]+(mx+1)*size else -1
            crane = (x, round(y + mult*speed, 3))
            draw()
        
        while crane[0] != box[idx][0]:
            x, y = crane
            mult = 1 if x <= box[idx][0] else -1
            crane = (round(x + mult*speed, 3), y)
            draw()
            
        while crane[1] != box[idx][1]+size:
            x, y = crane
            mult = 1 if y <= box[idx][1]+size else -1
            crane = (x, round(y + mult*speed, 3))
            draw()
            
        while box[idx][1] != o[1]+mx*size:
            x, y = box[idx]
            old[idx] = box[idx]
            box[idx] = (x, round(y+speed, 3))
            crane = (crane[0], round(crane[1]+speed, 3))
            draw()
            
        while box[idx][0] != o[0]+r*(size+w):
            x, y = box[idx]
            old[idx] = box[idx]
            mult = 1 if x <= o[0]+r*(size+w) else -1
            box[idx] = (round(x + mult*speed, 3), y)
            crane = (round(crane[0] + mult*speed, 3), crane[1])
            draw()
            
        while box[idx][1] != o[1]+c*size:
            x, y = box[idx]
            old[idx] = box[idx]
            mult = 1 if y <= o[1]+c*size else -1
            box[idx] = (x, round(y + mult*speed, 3))
            crane = (crane[0], round(crane[1] + mult*speed, 3))
            draw()
    while crane[1] != o[1]+(mx+1)*size:
        x, y = crane
        mult = 1 if y <= o[1]+(mx+1)*size else -1
        crane = (x, round(y + mult*speed, 3))
        draw()
    # end of function

def astar():
    o = (-115, -110)
    t.clear()
#     label_turtle = t.clone()
    screen = t.getscreen()
    screen.clear()
    screen.tracer(0)
    t.hideturtle()
    t.pencolor('grey')
    size, w = 30, 30
    
    x = -30
    for i in range(0, 30):
        t.penup()
        t.setpos(o[0]+x, 300)
        t.pendown()
        t.setpos(o[0]+x, -300)
#         t.penup()
#         t.setpos(o[0]-x, 300)
#         t.pendown()
#         t.setpos(o[0]-x, -300)
        x += size
    x = 0
    for i in range(0, 30):
        t.penup()
        t.setpos(300, o[1]+x)
        t.pendown()
        t.setpos(-300, o[1]+x)
#         t.penup()
#         t.setpos(300, o[1]-x)
#         t.pendown()
#         t.setpos(-300, o[1]-x)
        x += size
    screen.update()
    
    shape = Shape('compound')
      
    t.penup()
    t.setpos(0, 0)
    t.begin_poly()
    t.setpos(0, 0)
    t.setpos(size, 0)
    t.setpos(size, size)
    t.setpos(0, size)
    t.setpos(0, 0)
    t.end_poly()
    shape.addcomponent(t.get_poly(), 'white', 'red')
    screen.register_shape('box', shape)

    shape = Shape('compound')
    cw = 5
    t.penup()
    t.setpos(0, 0)
    t.begin_poly()
    t.setpos(size/2-1, 0)
    t.setpos(size/2-1, 500)
    t.setpos(size/2+1, 500)
    t.setpos(size/2+1, 0)
    t.setpos(0, 0)
    t.setpos(size, 0)
    t.setpos(size, -size)
    t.setpos(size+cw, cw)
    t.setpos(-cw, cw)
    t.setpos(0, -size)
    t.setpos(0, 0)
    t.right(-90)
    t.end_poly()
    shape.addcomponent(t.get_poly(), 'black')
    screen.register_shape('crane', shape)
    
    t.shape('crane')
    crane = t.clone()
    crane.showturtle()
    crane.penup()
    
    t.shape('box')
    
    # init pos
    pos = [(0, 0), (0, 1), (2, 0), (2, 1), (1, 0), (3, 0)]
#     pos = [(a, 0) for a in range(10)]
    
    box = []
    label = []
    for i in range(len(pos)):
        box.append(t.clone())
        label.append(str(i+1))
        
#     label_turtle.clear()
#     label_turtle.penup()
#     label_turtle.pencolor('red')
#     def show_label(idx=None):
#         if idx is not None:
#             boxid = idx
#             x, y = box[boxid].pos()
#             x += size/2
#             y += size/2
#             label_turtle.setpos(x, y)
#             label_turtle.pendown()
#             print label[boxid]
#             label_turtle.write(label[boxid])
#             label_turtle.penup()
#             return
#         for boxid in range(len(box)):
#             x, y = box[boxid].pos()
#             x += size/2
#             y += size/2
#             label_turtle.setpos(x, y)
#             label_turtle.pendown()
#             print label[boxid]
#             label_turtle.write(label[boxid])
#             label_turtle.penup()
#     # end of helper function
    
    for i in range(len(pos)):
        box[i].penup()
        box[i].setpos(o[0]+pos[i][0]*(size+w), o[1]+pos[i][1]*size)
        box[i].showturtle()
        screen.update()
        
    moves = [(1, 3, 1), (1, 2, 2), (0, 2, 3), (5, 1, 1), (0, 1, 2)]
    mx = 5
    speed = 0.2
    crane.setpos(o[0], o[1]+(mx+1)*size)
    for move in moves:
        idx, r, c = move
        # get crane to correct pos
        while crane.ycor() != o[1]+(mx+1)*size:
            x, y = crane.pos()
            mult = 1 if y <= o[1]+(mx+1)*size else -1
            crane.setpos(x, round(y + mult*speed, 3))
            screen.update()
        
        while crane.xcor() != box[idx].xcor():
            x, y = crane.pos()
            mult = 1 if x <= box[idx].xcor() else -1
            crane.setpos(round(x + mult*speed, 3), y)
            screen.update()
        
        while crane.ycor() != box[idx].ycor()+size:
            x, y = crane.pos()
            mult = 1 if y <= box[idx].ycor()+size else -1
            crane.setpos(x, round(y + mult*speed, 3))
            screen.update()
            
        while box[idx].ycor() != o[1]+mx*size:
            x, y = box[idx].pos()
            box[idx].setpos(x, round(y+speed, 3))
            crane.setpos(crane.xcor(), round(crane.ycor()+speed, 3))
            screen.update()
            
        while box[idx].xcor() != o[0]+r*(size+w):
            x, y = box[idx].pos()
            mult = 1 if x <= o[0]+r*(size+w) else -1
            box[idx].setpos(round(x + mult*speed, 3), y)
            crane.setpos(round(crane.xcor() + mult*speed, 3), crane.ycor())
            screen.update()
            
        while box[idx].ycor() != o[1]+c*size:
            x, y = box[idx].pos()
            mult = 1 if y <= o[1]+c*size else -1
            box[idx].setpos(x, round(y + mult*speed, 3))
            crane.setpos(crane.xcor(), round(crane.ycor() + mult*speed, 3))
            screen.update()
    while crane.ycor() != o[1]+(mx+1)*size:
        x, y = crane.pos()
        mult = 1 if y <= o[1]+(mx+1)*size else -1
        crane.setpos(x, round(y + mult*speed, 3))
        screen.update()
    # end of function



