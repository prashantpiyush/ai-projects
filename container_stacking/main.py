################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
from operator import pos
'''
Created on Sep 24, 2018

@author: prashant
'''


import copy
import time
import turtle
import tkinter as tk
from turtle import Shape

# import logging
# logfile = 'log.txt'
# with open(logfile, 'w') as f:
#     pass
# logging.basicConfig(filename=logfile,level=logging.DEBUG)
LOG_ENABLED = False
def log(*args):
    if not LOG_ENABLED: return
    # for arg in args:
    #     logging.debug(arg)

from util import Ai


app_width = 1400
app_height = 800

pen = None
t = None

def dummy():
    toggle_button(astar_path_button, True)
    # logging.debug("in dummy")
        
def prepturtle(pen):
    global t
    t = pen.clone()
    pen.hideturtle()
    
def compute_astar_path():
    prepturtle(astar_turtle)
    ai.initial_state_generator()
    init_pos = ai.get_block_pos('init_pos')
    display(init_pos)
    
    prepturtle(hc_turtle)
    ai.goal_state_generator()
    goal_pos = ai.get_block_pos('goal_pos')
    display(goal_pos)
    
    dummy()
    
def show_astar_path():
    prepturtle(astar_turtle)
    
    init_pos = ai.get_block_pos('init_pos')
    goal_pos = ai.get_block_pos('goal_pos')
    
    astar_path = ai.gbfs(init_pos, goal_pos, ai.h3)
    log("len of path with h1", len(astar_path))
    print ("len:", len(astar_path))
    
#     astar_path = ai.astar(init_pos, goal_pos, ai.h2)
#     log("len of path with h2", len(astar_path))

    for pos in astar_path:
        display(pos)
        time.sleep(1)
    
def display(pos, moves=[]):
    global t
    o = (-115, -110)
    t.clear()
    screen = t.getscreen()
    screen.clear()
    screen.tracer(0)
    t.hideturtle()
    t.pencolor('#D3D3D3') # light grey
    size, w = 30, 30
    
    # init pos
    box = []
    for i in range(len(pos)):
        box.append((o[0]+pos[i][0]*(size+w), o[1]+pos[i][1]*size))
    
    def draw_boxes():
        t.pencolor('red')
        for i in range(len(box)):
            t.pencolor('red')
            x, y = box[i]
            t.penup()
            t.setpos(x, y)
            t.pendown()
            t.setpos(x, y+size)
            t.setpos(x+size, y+size)
            t.setpos(x+size, y)
            t.setpos(x, y)
            t.penup()
            t.setpos(x+size/2-4, y+size/2-4)
            t.write(str(i+1))
    def draw():
        t.clear()
        t.color('#D3D3D3') # light grey
        x = -size
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
        screen.update()
        for _ in range(10):
            pass
#         time.sleep(1)
    draw()
    for move in moves:
        idx, r, c = move
        box[idx] = (o[0]+r*(size+w), o[1]+c*size)
        draw()
    # end of function

def set_label_text(label, text):
    label.config(text=text)

def toggle_button(button, state=True):
    if state == True:
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)

def set_parameters():
    try:
        int(input1_var.get())
        int(input2_var.get())
    except:
        set_label_text(warning_label, "Please enter valid integers only.")
        return
    global ai
    del ai
    n, m = int(input1_var.get()), int(input2_var.get())
    ai = Ai(n, m)
    
    set_label_text(warning_label, "")
    toggle_button(astar_path_button, False)
    toggle_button(hc_path_button, False)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Container Stacking (Made by: Prashant Piyush)')
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
    right.grid_columnconfigure(1, weight=1, uniform=1)
    right.grid_rowconfigure(0, weight=1, uniform=1)
    right.grid_rowconfigure(1, weight=1, uniform=1)
    
    
    tk.Label(left, text='Number of stacks').grid(row=0, pady=4, sticky=tk.W)
    tk.Label(left, text='Maximum size of stack').grid(row=1, pady=4, sticky=tk.W)
    tk.Label(left, text='(Empty)').grid(row=2, pady=4, sticky=tk.W)
    
    input1_var = tk.StringVar()
    input1_entry_field = tk.Entry(left, textvariable=input1_var, width=25)
    input1_entry_field.grid(row=0, column=1, stick=tk.W)
    
    input2_var = tk.StringVar()
    input2_entry_field = tk.Entry(left, textvariable=input2_var, width=25)
    input2_entry_field.grid(row=1, column=1, stick=tk.W)
    
#     input3_var = tk.StringVar()
#     input3_entry_field = tk.Entry(left, textvariable=input3_var, width=25)
#     input3_entry_field.grid(row=2, column=1, stick=tk.W)
    
    parameters_submit = tk.Button(left, text='Submit (Option 1)', width=20, command=set_parameters)
    parameters_submit.grid(row=3, sticky='W', padx=4, pady=4)
    
    # Warning lable for submit button
    warning_label = tk.Label(left, text='', anchor=tk.W)
    warning_label.grid(row=4, columnspan=2, sticky=tk.W)
    
    # Frame used as visual separator
    tk.Frame(left, height=1, bd=2, bg='black').grid(row=5, columnspan=2, sticky='we', padx=4, pady=8)
    
    button_frame = tk.Frame(left)
    button_frame.grid(row=6, rowspan=3, columnspan=2, sticky='nsew')
    button_frame.propagate(0)
    
    tk.Label(button_frame, text='Astar (T1)', anchor=tk.W).grid(row=6, sticky=tk.W)
    start_astar_button = tk.Button(button_frame, text='Start(Option 2)', width=15, command=compute_astar_path)
    start_astar_button.grid(row=7, sticky=tk.W, padx=4, pady=4)
    astar_path_button = tk.Button(button_frame, text='Show path(Option 3)', width=15, state=tk.DISABLED, command=show_astar_path)
    astar_path_button.grid(row=8, stick=tk.W, padx=4, pady=4)
     
    tk.Label(button_frame, text='HC (T2)', anchor=tk.W).grid(row=6, column=1, sticky=tk.W)
    start_hc_button = tk.Button(button_frame, text='Start(Option 2)', width=15, command=dummy)
    start_hc_button.grid(row=7, column=1, sticky=tk.W, padx=4, pady=4)
    hc_path_button = tk.Button(button_frame, text='Show path(Option 3)', width=15, state=tk.DISABLED, command=dummy)
    hc_path_button.grid(row=8, column=1, stick=tk.W, padx=4, pady=4)
    
    tk.Label(button_frame, text='Show results (Option 4)', anchor=tk.W, wraplength=100)\
    .grid(row=6, column=2, sticky=tk.W, rowspan=2)
    cmp_button = tk.Button(button_frame, text='Show', width=10, command=dummy)
    cmp_button.grid(row=8, column=2, sticky=tk.W, padx=4, pady=4)
    
    # Frame used as visual separator
    tk.Frame(left, height=1, bd=2, bg='black').grid(columnspan=2, sticky='we', padx=4, pady=8)
    
    tk.Label(left, text='BFS (T1)', anchor='w').grid(sticky='w')
    tk.Label(left, text='R1 - Total search tree nodes:', anchor='w').grid(row=11, sticky='w')
    tk.Label(left, text='R2 - Mem. for one node(bytes): ', anchor='w').grid(row=12, sticky='w')
    tk.Label(left, text='R3 - Max size of aux. queue: ', anchor='w').grid(row=13, sticky='w')
    tk.Label(left, text='R4 - Cost to reach goal: ', anchor='w').grid(row=14, sticky='w')
    tk.Label(left, text='R5 - Time taken(sec): ', anchor='w').grid(row=15, sticky='w')
    
    bfs_node_count_label = tk.Label(left, text='', anchor='w')
    bfs_node_count_label.grid(row=11, column=1, sticky='w')
    bfs_node_mem_label = tk.Label(left, text='', anchor='w')
    bfs_node_mem_label.grid(row=12, column=1, sticky='w')
    bfs_max_size_label = tk.Label(left, text='', anchor='w')
    bfs_max_size_label.grid(row=13, column=1, sticky='w')
    bfs_path_cost_label = tk.Label(left, text='', anchor='w')
    bfs_path_cost_label.grid(row=14, column=1, sticky='w')
    bfs_time_label = tk.Label(left, text='', anchor='w')
    bfs_time_label.grid(row=15, column=1, sticky='w')
    
    tk.Frame(left, height=1, bd=2, bg='grey').grid(columnspan=2, sticky='we', padx=4, pady=2)
    
    tk.Label(left, text='DFS (T2)', anchor=tk.W).grid(sticky=tk.W)
    tk.Label(left, text='R6 - Total search tree nodes:', anchor='w').grid(row=18, sticky='w')
    tk.Label(left, text='R7 - Mem. for one node(bytes): ', anchor='w').grid(row=19, sticky='w')
    tk.Label(left, text='R8 - Max size of stack: ', anchor='w').grid(row=20, sticky='w')
    tk.Label(left, text='R9 - Cost to reach goal: ', anchor='w').grid(row=21, sticky='w')
    tk.Label(left, text='R10 - Time taken(sec): ', anchor='w').grid(row=22, sticky='w')
    
    dfs_node_count_label = tk.Label(left, text='', anchor='w')
    dfs_node_count_label.grid(row=18, column=1, sticky='w')
    dfs_node_mem_label = tk.Label(left, text='', anchor='w')
    dfs_node_mem_label.grid(row=19, column=1, sticky='w')
    dfs_max_size_label = tk.Label(left, text='', anchor='w')
    dfs_max_size_label.grid(row=20, column=1, sticky='w')
    dfs_path_cost_label = tk.Label(left, text='', anchor='w')
    dfs_path_cost_label.grid(row=21, column=1, sticky='w')
    dfs_time_label = tk.Label(left, text='', anchor='w')
    dfs_time_label.grid(row=22, column=1, sticky='w')
    
    tk.Frame(left, height=1, bd=2, bg='grey').grid(columnspan=2, sticky='we', padx=4, pady=2)
    
    compare_frame = tk.Frame(left)
    compare_frame.grid(row=24, rowspan=3, columnspan=2, sticky='nsew')
    compare_frame.propagate(0)
    
    tk.Label(compare_frame, text='Compare', anchor=tk.W, width=20).grid(row=0, sticky=tk.W)
    tk.Label(compare_frame, text='Astar', anchor=tk.W, width=10).grid(row=0, column=1, sticky=tk.W)
    tk.Label(compare_frame, text='HC', anchor=tk.W).grid(row=0, column=2, sticky=tk.W)
    tk.Label(compare_frame, text='R11 - Memory(bytes):', anchor='w').grid(row=1, sticky='w')
    tk.Label(compare_frame, text='R12 - Cost: ', anchor='w').grid(row=2, sticky='w')
    
    bfs_cmp_mem_label = tk.Label(compare_frame, text='', anchor='w')
    bfs_cmp_mem_label.grid(row=1, column=1, sticky='w')
    bfs_cmp_cost_label = tk.Label(compare_frame, text='', anchor='w')
    bfs_cmp_cost_label.grid(row=2, column=1, sticky='w')
    
    dfs_cmp_mem_label = tk.Label(compare_frame, text='', anchor='w')
    dfs_cmp_mem_label.grid(row=1, column=2, sticky='w')
    dfs_cmp_cost_label = tk.Label(compare_frame, text='', anchor='w')
    dfs_cmp_cost_label.grid(row=2, column=2, sticky='w')
    
    # Graph frames
    astar_frame = tk.Frame(right, width=10, height=10)
    astar_frame.pack_propagate(0)
    astar_frame.grid(row=0, column=0, sticky='nsew')
    astar_frame.grid_columnconfigure(0, weight=1)
    astar_frame.grid_rowconfigure(1, weight=1)
    
    hc_frame = tk.Frame(right, width=10, height=10)
    hc_frame.pack_propagate(0)
    hc_frame.grid(row=0, column=1, sticky='nsew')
    hc_frame.grid_columnconfigure(0, weight=1)
    hc_frame.grid_rowconfigure(1, weight=1)
    
    cmp_frame = tk.Frame(right, width=10, height=10)
    cmp_frame.pack_propagate(0)
    cmp_frame.grid(row=1, column=0, sticky='nsew')
    cmp_frame.grid_columnconfigure(0, weight=1)
    cmp_frame.grid_rowconfigure(1, weight=1)
    
    info_frame = tk.Frame(right, width=10, height=10)
    info_frame.pack_propagate(0)
    info_frame.grid(row=1, column=1, stick='nsew', padx=4, pady=4)
    info_frame.grid_columnconfigure(0, weight=1)
    
    tk.Label(astar_frame, text='Astar', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    tk.Label(hc_frame, text='Hill Climbing', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    tk.Label(cmp_frame, text='Compare graph', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    
    # Create canvases and turtles
    astar_canvas = tk.Canvas(astar_frame, **border_params)
    astar_canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    astar_turtle = turtle.RawTurtle(astar_canvas)
    
    hc_canvas = tk.Canvas(hc_frame, **border_params)
    hc_canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    hc_turtle = turtle.RawTurtle(hc_canvas)
    
    cmp_canvas = tk.Canvas(cmp_frame, **border_params)
    cmp_canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    cmp_turtle = turtle.RawTurtle(cmp_canvas)
    
    tk.Label(info_frame, text='Instructions', anchor=tk.CENTER).grid(row=0, padx=8, pady=4)
    def add_inst(text):
        tk.Label(info_frame, text=text, wraplength=300, anchor=tk.W, justify='left').grid(sticky='w')
    add_inst('1. Input grid parameters (size & percentage coverage) and target number of squares.')
    add_inst('2. Then compute bfs/dfs path using "start bfs/dfs" button.')
    add_inst('3. Now use "show path" button to show corresponding path computed.')
    add_inst('4. Option numbers are written on respective buttons, please use them.')
    add_inst('5. Whenever bfs/dfs is called initial state is shown in their respective canvas.')
    add_inst('6. Program might not respond while its computing bfs/dfs path, so please be patient.')
    add_inst('7. Clicking on buttons while something is under process may produce unexpected results, '\
             + 'please refrain from doing that.')
    
    # Print Some Guidelines
    desc = 'STACKING CONTAINERS PROBLEM\n\nSome specifications:'\
    +'\n1. This program is gui based, there is no command line interaction with the user.'\
    +'\n2. The gui is fully capable of handling all user inputs.'\
    +'\n3. For all the options specified in the project description a button is implemented, please use them.'\
    +'\n\n\n'
    print(desc)
    
    
    # Set default values in entry fields
    n, m = (6, 3)
    input1_var.set(n)
    input2_var.set(m)
    
    ai = Ai(n, m)
    
    log('I m in Main')
    
    root.mainloop()
    
    
    