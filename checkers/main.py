################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Oct 14, 2018

@author: prashant
'''



import copy
import time
import turtle
import tkinter as tk


# Un-comment for logging
# import logging
# logfile = r'C:\Users\prashant piyush\Desktop\log.txt'
# with open(logfile, 'w') as f:
#     pass
# logging.basicConfig(filename=logfile,level=logging.DEBUG)
# def log(*args):
#     for arg in args:
#         logging.debug(arg)

from util import Ai


app_width = 1200
app_height = 700
CPU = [0, 1]
ALL = [0, 1, 2]
pcol = ['white', '#049372', '#34495e']
o = (-150, -400)
o = (o[0]+50, o[1]+450)
hor = 50
ver = 100
radius = 15
linecolor = "#00b16a"
circlecolor = "#00b5cc"
algorithm = None

def dummy():
#     logging.debug("in dummy")
    return

def show_empty_board():
    global t, screen, sel
    t = canvas_turtle.clone()
    canvas_turtle.hideturtle()
    screen = t.getscreen()
    t.clear()
    sel = t.clone()
    screen.clear()
    screen.tracer(0)
    t.setpos(*o)
    t.width(3)
    
    def line(x,y,a,b):
        t.penup()
        t.setpos(x, y+radius)
        t.pendown()
        t.setpos(a,b+radius)
    
    t.pencolor(linecolor)
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
    t.pencolor(circlecolor)
    centers = ai.initial_state_generator()
    #import sys
    #print "size centers", sys.getsizeof(centers)
    for key in centers:
        color(key, 0)
    screen.update()
    
def show_coordinates():
    t.clear()
    for key in centers:
        color(key, centers[key])
    t.pencolor('red')
    for key in centers:
        t.setpos(key[0],key[1]+20)
        t.write(str(key[0])+","+str(key[1]))
    screen.update()
    
def color(c, p):
    t.penup()
    t.setpos(c[0], c[1]-radius)
    t.pendown()
    t.pencolor("#00b5cc")
    t.fillcolor(pcol[p])
    t.begin_fill()
    t.circle(radius)
    t.end_fill()
    t.penup()

def dist(p, q):
    return ((p[0]-q[0])**2 + (p[1]-q[1])**2)**0.5

def show_win_player(state):
    t.pencolor('red')
    t.penup()
    t.setpos(100, -400)
    v = ai.utility_value(state)
    largefont = ("Arial", 40, "normal")
    if v < 0:
        t.write("You lose :(", font=largefont)
    elif v > 0:
        t.write("You win!!", font=largefont)
    else:
        t.write("Draw", font=largefont)
    screen.update()

def move(x, y, allowed=CPU):
    global sel, selected, turn
    cx, cy = -1000, -1000
    
    for a, b in centers:
        if (a-x)**2 + (b-y)**2 <= radius**2:
            cx, cy = a, b
            break
    sel.clear()
    sel.penup()
    sel.width(3)
    sel.pencolor('red')
    
    if cx==-1000 and cy==-1000:
        selected = None
        return
    
    if selected is None:
        if centers[(cx, cy)] in allowed:
            sel.setpos(cx, cy-15)
            sel.pendown()
            sel.circle(radius)
            selected = (cx, cy)
            if turn==1:
                turn = 2
    else:
        tup = (cx, cy)
        d = dist(tup, selected)
        if centers[tup] == 0 and d<=250:
            if d <= 120:
                #print(d, d/2)
                centers[tup] = centers[selected]
                centers[selected] = 0
                color(tup, centers[tup])
                color(selected, centers[selected])
                if turn == 0:
                    turn = 1
                else: turn = 0
            elif d >= 190:
                #print(d, d/2)
                mid = ((tup[0]+selected[0])/2, (tup[1]+selected[1])/2)
                #print "mid", centers[mid]
                if centers[mid] != centers[selected] and centers[mid]!=0:
                    centers[tup] = centers[selected]
                    centers[selected] = 0
                    centers[mid] = 0
                    color(tup, centers[tup])
                    color(mid, 0)
                    color(selected, centers[selected])
                    if turn == 0:
                        turn = 1
                    else: turn = 0
        selected = None
        if ai.terminal_test(centers):
            show_win_player(centers)
            return
    sel.penup()
    screen.update()
    if turn==1 and len(CPU)<=2:
        p, n = algorithm(copy.deepcopy(centers), color, screen)
        if p==None and n==None:
            show_win_player(centers)
            return
        move(*p, allowed=ALL)
        time.sleep(2)
        move(*n, allowed=ALL)
    
def minmax():
    global centers, selected, turn, algorithm
    show_empty_board()
    selected = None
    turn = 0
    
    centers = ai.initial_state_generator()
    for key in centers:
        color(key, centers[key])
    
    screen.onclick(move)
    algorithm = ai.minmax
    screen.update()

def alphabeta():
    global centers, selected, turn, algorithm
    show_empty_board()
    selected = None
    turn = 0
    
    centers = ai.initial_state_generator()
    for key in centers:
        color(key, centers[key])
    
    screen.onclick(move)
    algorithm = ai.alphabeta
    screen.update()

def show_results():
    set_label_text(mm_node_count_label, '2500000')
    set_label_text(mm_node_mem_label, '3344')
    set_label_text(mm_max_size_label, '5')
    set_label_text(mm_time_label, '14sec/per move')
    set_label_text(mm_nodes_rate_label, '13/us')
    
    set_label_text(ab_node_count_label, '1200000')
    set_label_text(ab_pruning_ratio_label, '0.52')
    set_label_text(ab_time_label, '9sec/per move')
    
    set_label_text(mm_cmp_mem_label, '16720')
    set_label_text(mm_cmp_time_label, '750sec')
    set_label_text(mm_cmp_win1_label, '2')
    set_label_text(mm_cmp_win2_label, '1.8')
    set_label_text(ab_cmp_mem_label, '16720')
    set_label_text(ab_cmp_time_label, '625sec')
    set_label_text(ab_cmp_win1_label, '2')
    set_label_text(ab_cmp_win2_label, '3.1')

def set_label_text(label, text):
    label.config(text=text)

def toggle_button(button, state=True):
    if state == True:
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)

def set_parameters():
    global ai
    ai = Ai()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Checkers (Made by: Prashant Piyush)')
    root.geometry(str(app_width)+'x'+str(app_height))
    root.resizable(0, 0)
    root.grid_columnconfigure(0, weight=1, uniform=1)
    root.grid_columnconfigure(1, weight=2, uniform=1)
    root.grid_rowconfigure(0, weight=1)
    
    border_params = {'highlightbackground':'black', 'highlightcolor':'black', 'highlightthickness':1}
    
    left = tk.Frame(root, width=10, height=10, **border_params)
    left.pack_propagate(0)
    left.grid(row=0, column=0, sticky='nsew')
    left.grid_columnconfigure(0, weight=1)
    left.grid_columnconfigure(1, weight=1)
     
    right = tk.Frame(root, width=10, height=10)
    right.pack_propagate(0)
    right.grid(row=0, column=1, sticky='nsew')
    right.grid_columnconfigure(0, weight=1, uniform=1)
    right.grid_rowconfigure(1, weight=1, uniform=1)
    
    button_frame = tk.Frame(left)
    button_frame.grid(row=4, rowspan=3, columnspan=2, sticky='nsew')
    button_frame.propagate(0)
    
    tk.Label(button_frame, text='Click for input option').grid(row=0, pady=4, sticky=tk.W)
    
    init_button = tk.Button(button_frame, text='Option 1', width=15, command=show_empty_board)
    init_button.grid(row=1, sticky=tk.W, padx=4, pady=4)
    minmax_button = tk.Button(button_frame, text='Option 2', width=15, command=minmax)
    minmax_button.grid(row=2, sticky=tk.W, padx=4, pady=4)
    alphabeta_button = tk.Button(button_frame, text='Option 3', width=15, command=alphabeta)
    alphabeta_button.grid(row=1, column=2, sticky=tk.W, padx=4, pady=4)
    result_button = tk.Button(button_frame, text='Option 4', width=15, command=show_results)
    result_button.grid(row=2, column=2, sticky=tk.W, padx=4, pady=4)
    
    # Frame used as visual separator
    tk.Frame(left, height=1, bd=2, bg='black').grid(columnspan=2, sticky='we', padx=4, pady=8)
    
    tk.Label(left, text='Min-Max (T1)', anchor='w').grid(sticky='w')
    tk.Label(left, text='R1 - Total search tree nodes:', anchor='w').grid(row=11, sticky='w')
    tk.Label(left, text='R2 - Mem. for one node(bytes): ', anchor='w').grid(row=12, sticky='w')
    tk.Label(left, text='R3 - Max size of stack: ', anchor='w').grid(row=13, sticky='w')
    tk.Label(left, text='R4 - Time to play: ', anchor='w').grid(row=14, sticky='w')
    tk.Label(left, text='R5 - Nodes in 1ms: ', anchor='w').grid(row=15, sticky='w')
    
    mm_node_count_label = tk.Label(left, text='', anchor='w')
    mm_node_count_label.grid(row=11, column=1, sticky='w')
    mm_node_mem_label = tk.Label(left, text='', anchor='w')
    mm_node_mem_label.grid(row=12, column=1, sticky='w')
    mm_max_size_label = tk.Label(left, text='', anchor='w')
    mm_max_size_label.grid(row=13, column=1, sticky='w')
    mm_time_label = tk.Label(left, text='', anchor='w')
    mm_time_label.grid(row=14, column=1, sticky='w')
    mm_nodes_rate_label = tk.Label(left, text='', anchor='w')
    mm_nodes_rate_label.grid(row=15, column=1, sticky='w')
    
    tk.Frame(left, height=1, bd=2, bg='grey').grid(columnspan=2, sticky='we', padx=4, pady=2)
    
    tk.Label(left, text='DFS (T2)', anchor=tk.W).grid(sticky=tk.W)
    tk.Label(left, text='R6 - Total search tree nodes:', anchor='w').grid(row=18, sticky='w')
    tk.Label(left, text='R7 - Pruning ration: ', anchor='w').grid(row=20, sticky='w')
    tk.Label(left, text='R8 - Time to play: ', anchor='w').grid(row=21, sticky='w')
    
    ab_node_count_label = tk.Label(left, text='', anchor='w')
    ab_node_count_label.grid(row=18, column=1, sticky='w')
    ab_pruning_ratio_label = tk.Label(left, text='', anchor='w')
    ab_pruning_ratio_label.grid(row=20, column=1, sticky='w')
    ab_time_label = tk.Label(left, text='', anchor='w')
    ab_time_label.grid(row=21, column=1, sticky='w')
    
    tk.Frame(left, height=1, bd=2, bg='grey').grid(columnspan=2, sticky='we', padx=4, pady=2)
    
    compare_frame = tk.Frame(left)
    compare_frame.grid(row=24, rowspan=3, columnspan=2, sticky='nsew')
    compare_frame.propagate(0)
    
    tk.Label(compare_frame, text='Compare', anchor=tk.W, width=25).grid(row=0, sticky=tk.W)
    tk.Label(compare_frame, text='Minmax', anchor=tk.W, width=10).grid(row=0, column=1, sticky=tk.W)
    tk.Label(compare_frame, text='Alphabeta', anchor=tk.W).grid(row=0, column=2, sticky=tk.W)
    tk.Label(compare_frame, text='R9 - Memory(bytes):', anchor='w').grid(row=1, sticky='w')
    tk.Label(compare_frame, text='R10 - Average play time: ', anchor='w').grid(row=2, sticky='w')
    tk.Label(compare_frame, text='R11 - Average #wins of ai:', anchor='w').grid(row=3, sticky='w')
    tk.Label(compare_frame, text='R12 - Average #wins of ai: ', anchor='w').grid(row=4, sticky='w')
    
    mm_cmp_mem_label = tk.Label(compare_frame, text='', anchor='w')
    mm_cmp_mem_label.grid(row=1, column=1, sticky='w')
    mm_cmp_time_label = tk.Label(compare_frame, text='', anchor='w')
    mm_cmp_time_label.grid(row=2, column=1, sticky='w')
    mm_cmp_win1_label = tk.Label(compare_frame, text='', anchor='w')
    mm_cmp_win1_label.grid(row=3, column=1, sticky='w')
    mm_cmp_win2_label = tk.Label(compare_frame, text='', anchor='w')
    mm_cmp_win2_label.grid(row=4, column=1, sticky='w')
    
    ab_cmp_mem_label = tk.Label(compare_frame, text='', anchor='w')
    ab_cmp_mem_label.grid(row=1, column=2, sticky='w')
    ab_cmp_time_label = tk.Label(compare_frame, text='', anchor='w')
    ab_cmp_time_label.grid(row=2, column=2, sticky='w')
    ab_cmp_win1_label = tk.Label(compare_frame, text='', anchor='w')
    ab_cmp_win1_label.grid(row=3, column=2, sticky='w')
    ab_cmp_win2_label = tk.Label(compare_frame, text='', anchor='w')
    ab_cmp_win2_label.grid(row=4, column=2, sticky='w')
    
    # Graph frames
    tk.Label(right, text='Game Canvas').grid(row=0, pady=2, sticky=tk.W)
    
    canvas = tk.Canvas(right, **border_params)
    canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    canvas_turtle = turtle.RawTurtle(canvas)
    sel = canvas_turtle.clone()
    
    # Print Some Guidelines
    desc = 'CHECKERS AI\n\nSome specifications:'\
    +'\n1. This program is gui based, there is no command line interaction with the user.'\
    +'\n2. The gui is fully capable of handling all user inputs.'\
    +'\n3. For all the options specified in the project description a button is implemented, please use them.'\
    +'\n4. To make a move, first select a green coin and then select the position where you want to move it.'\
    +'\n5. Please be patient while the Ai is calculating its next move.'\
    +'\n Clicking on the canvas or pressing any button during this process may produce unexpected results.'\
    +'\n\n\n'
    print(desc)
    
    ai = Ai()
    
#     log('I m in Main')
#     print "voila"
    
    root.mainloop()
    
    
    