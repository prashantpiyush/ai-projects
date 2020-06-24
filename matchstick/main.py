################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Sep 7, 2018

@author: prashant
'''

import copy
import time
import turtle
import tkinter as tk
from itertools import product

from util import Ai


app_width = 1600
app_height = 900

pen = None

def draw_stick(x, y, w, h):
    pen.pencolor('red')
    pen.penup()
    pen.setposition(x, y)
    pen.pendown()
    pen.setposition(x+w, y+h)


def erase_stick(x, y, w, h):
    pen.pencolor('white')
    pen.penup()
    pen.setposition(x, y)
    pen.pendown()
    pen.setposition(x+w, y+h)


def draw_grid(h, v, ph, pv, init=False):
    w = 20
    o = [-40, 50]
    if init:
        pen.clear()
        for i in range(len(h)):
            for j in range(len(h[0])):
                if h[i][j]==1:
                    draw_stick(o[0]+j*w, o[1]-i*w, w, 0)
        for i in range(len(v)):
            for j in range(len(v[0])):
                if v[i][j]==1:
                    draw_stick(o[0]+j*w, o[1]-i*w, 0, -w)
    else:
        for i in range(len(h)):
            for j in range(len(h[0])):
                if h[i][j]!=ph[i][j]:
                    erase_stick(o[0]+j*w, o[1]-i*w, w, 0)
        for i in range(len(v)):
            for j in range(len(v[0])):
                if v[i][j]!=pv[i][j]:
                    erase_stick(o[0]+j*w, o[1]-i*w, 0, -w)
    time.sleep(1)

def start():
    h, v = ai.initial_state_generator()
    draw_grid(h, v, h, v, init=True)
    while True:
        ph, pv = copy.deepcopy(h), copy.deepcopy(v)
        h, v = ai.get_next_state()
        if h==None and v==None:
            break
        draw_grid(h, v, ph, pv)
    # function ends here

def compute_bfs_path():
    global bfs_path
    meta = ai.bfs(bfs_turtle)
    bfs_path = meta['path']
    set_label_text(bfs_node_count_label, meta['total_node_count'])
    set_label_text(bfs_node_mem_label, meta['node_mem'])
    set_label_text(bfs_max_size_label, meta['queue_max_len'])
    set_label_text(bfs_path_cost_label, meta['cost'])
    set_label_text(bfs_time_label, meta['time'])
    toggle_button(bfs_path_button)

def show_bfs_path():
    show_path_graphically(bfs_path, bfs_turtle)

def compute_dfs_path():
    global dfs_path
    meta = ai.dfs(dfs_turtle)
    dfs_path = meta['path']
    set_label_text(dfs_node_count_label, meta['total_node_count'])
    set_label_text(dfs_node_mem_label, meta['node_mem'])
    set_label_text(dfs_max_size_label, meta['stack_max_len'])
    set_label_text(dfs_path_cost_label, meta['cost'])
    set_label_text(dfs_time_label, meta['time'])
    toggle_button(dfs_path_button)

def show_dfs_path():
    show_path_graphically(dfs_path, dfs_turtle)
        
def show_path_graphically(path, t):
    global pen
    pen = t
    init = True
    ph, pv = None, None
    for node in path:
        h, v = ai.decompress(node)
        draw_grid(h, v, ph, pv, init)
        init = False
        ph, pv = h, v
        
def print_path(path):
    ph, pv = ai.decompress(path[0])
    for node in path[1::]:
        h, v = ai.decompress(node)
        f = False
        for i, j in product(range(len(h)), range(len(h[0]))):
            if h[i][j] != ph[i][j]:
                print('->', (i, j), end='')
                f = True
                break
        if f: continue
        for i, j in product(range(len(v), range(len(v[0])))):
            if h[i][j] != pv[i][j]:
                print('->', (i, j), end='')
                break
    # function ends here
        
def show_results():
    set_label_text(status_bar, 'Showing comparision results(R11, R12 & G3)')
    compare()
    runtime_graph()
    
def compare(run=False):
    avg_bfs_cost, avg_dfs_cost = 3, 7
    max_bfs_mem, max_dfs_mem = 50400, 504
    if run:
        cost = []
        max_bfs_mem, max_dfs_mem = 0, 0
        for _ in range(10):
            ai.initial_state_generator()
            meta_bfs = ai.bfs(bfs_turtle, init_state=False)
            meta_dfs = ai.dfs(dfs_turtle, init_state=False)
            cost.append((meta_bfs['cost'], meta_dfs['cost']))
            max_bfs_mem = max(max_bfs_mem, meta_bfs['node_mem']*meta_bfs['queue_max_len'])
            max_dfs_mem = max(max_dfs_mem, meta_dfs['node_mem']*meta_dfs['stack_max_len'])
        avg_bfs_cost = sum([val[0] for val in cost])/len(cost)
        avg_dfs_cost = sum([val[1] for val in cost])/len(cost)
    set_label_text(bfs_cmp_cost_label, avg_bfs_cost)
    set_label_text(dfs_cmp_cost_label, avg_dfs_cost)
    set_label_text(bfs_cmp_mem_label, max_bfs_mem)
    set_label_text(dfs_cmp_mem_label, max_dfs_mem)

def runtime_graph(run=False):
    global ai
    # These are the results from previous runs
    time = [(0.8058971352609088, 0.7959112525268416), (5.767188457820188, 1.7839178601334078),\
            (7.0034266835409795, 2.983069520901978), (8.636212998031588, 4.616296621770378),\
            (10.97483654365763, 6.617920596080964), (19.500726808795065, 8.78038179454515)]
    time = [(0.8034134646042023, 0.8229737673923273), (1.5956936986166195, 1.5917969050000629),\
            (2.846747373550863, 2.8401113741969146), (4.300874637468331, 4.2552083309090865),\
            (6.25773836093562, 6.005873583211578), (14.017652400610118, 8.400256838356142)]
    if run:
        time = []
        for size in range(2, 8):
            del ai
            ai = Ai(size, 80, int(size*size*0.7), status_bar)
            ai.initial_state_generator()
            meta_bfs = ai.bfs(bfs_turtle, init_state=True)
            meta_dfs = ai.dfs(dfs_turtle, init_state=True)
            print("on size: ", size , (meta_bfs['time'], meta_dfs['time']))
            time.append((meta_bfs['time'], meta_dfs['time']))
    t = cmp_turtle
    t.clear()
    o = (-110, -110)
    t.pencolor('black')
    t.penup()
    t.setposition(o[0], o[1])
    t.pendown()
    t.setposition(o[0]+280, o[1])
    t.penup()
    t.setposition(o[0]+230, o[1]+2)
    t.pendown()
    t.write('Grid size')
    t.penup()
    t.setposition(o[0], o[1])
    t.pendown()
    t.setposition(o[0], o[1]+220)
    t.write('Time')
    t.pencolor('red')
    time = [(0, 0)] + time
    stepx, stepy = 40, 8
    for i in range(1, len(time)):
        j = time[i][0]
        t.penup()
        t.setposition(o[0]+(i-1)*stepx, o[1]+time[i-1][0]*stepy)
        t.pendown()
        t.setposition(o[0]+i*stepx, o[1]+j*stepy)
    t.write('bfs')
    t.pencolor('blue')
    for i in range(1, len(time)):
        j = time[i][1]
        t.penup()
        t.setposition(o[0]+(i-1)*stepx, o[1]+time[i-1][1]*stepy)
        t.pendown()
        t.setposition(o[0]+i*stepx, o[1]+j*stepy)
    t.write('dfs')

def set_label_text(label, text):
    label.config(text=text)

def toggle_button(button, state=True):
    if state == True:
        button.config(state=tk.NORMAL)
    else:
        button.config(state=tk.DISABLED)

def set_parameters():
    try:
        int(n_var.get())
        int(p_var.get())
        int(m_var.get())
    except:
        set_label_text(warning_label, "Please enter valid integers only.")
        return
    nn = int(n_var.get())
    np = int(p_var.get())
    mm = int(m_var.get())
    t = int((nn*nn*np)/100)
    if mm > t:
        set_label_text(warning_label, "Target should be less/eq to num of sq in percentage cover.")
        return
    global ai
    del ai
    n, p, m = nn, np, mm
    ai = Ai(n, p, m, status_bar)
    
    global pen
    h, v = ai.initial_state_generator()
    pen = bfs_turtle
    draw_grid(h, v, None, None, init=True)
    pen = dfs_turtle
    draw_grid(h, v, None, None, init=True)
    
    set_label_text(warning_label, "")
    set_label_text(status_bar, "Grid parameters changed.")
    toggle_button(dfs_path_button, False)
    toggle_button(bfs_path_button, False)

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Matchstick Ai (Made by: Prashant Piyush)')
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
    
    bottom = tk.Frame(root, width=app_width, height=20)
    bottom.pack_propagate(0)
    bottom.grid(row=1, columnspan=2)
    
    status_bar = tk.Label(bottom, text='Preparing...', bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(fill=tk.BOTH)
    
    tk.Label(left, text='Size of grid').grid(row=0, pady=4, sticky=tk.W)
    tk.Label(left, text='Percentage cover').grid(row=1, pady=4, sticky=tk.W)
    tk.Label(left, text='Goal').grid(row=2, pady=4, sticky=tk.W)
    
    n_var = tk.StringVar()
    n_entry_field = tk.Entry(left, textvariable=n_var, width=25)
    n_entry_field.grid(row=0, column=1, stick=tk.W)
    
    p_var = tk.StringVar()
    p_entry_field = tk.Entry(left, textvariable=p_var, width=25)
    p_entry_field.grid(row=1, column=1, stick=tk.W)
    
    m_var = tk.StringVar()
    m_entry_field = tk.Entry(left, textvariable=m_var, width=25)
    m_entry_field.grid(row=2, column=1, stick=tk.W)
    
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
#     button_frame.columnconfigure(0, weight=1, uniform=1)
#     button_frame.columnconfigure(1, weight=1, uniform=1)
#     button_frame.columnconfigure(2, weight=1, uniform=1)
    
    tk.Label(button_frame, text='BFS (T1)', anchor=tk.W).grid(row=6, sticky=tk.W)
    start_bfs_button = tk.Button(button_frame, text='Start(Option 2)', width=15, command=compute_bfs_path)
    start_bfs_button.grid(row=7, sticky=tk.W, padx=4, pady=4)
    bfs_path_button = tk.Button(button_frame, text='Show path(Option 3)', width=15, state=tk.DISABLED, command=show_bfs_path)
    bfs_path_button.grid(row=8, stick=tk.W, padx=4, pady=4)
     
    tk.Label(button_frame, text='DFS (T2)', anchor=tk.W).grid(row=6, column=1, sticky=tk.W)
    start_dfs_button = tk.Button(button_frame, text='Start(Option 2)', width=15, command=compute_dfs_path)
    start_dfs_button.grid(row=7, column=1, sticky=tk.W, padx=4, pady=4)
    dfs_path_button = tk.Button(button_frame, text='Show path(Option 3)', width=15, state=tk.DISABLED, command=show_dfs_path)
    dfs_path_button.grid(row=8, column=1, stick=tk.W, padx=4, pady=4)
    
    tk.Label(button_frame, text='Show results (Option 4)', anchor=tk.W, wraplength=100)\
    .grid(row=6, column=2, sticky=tk.W, rowspan=2)
    cmp_button = tk.Button(button_frame, text='Show', width=10, command=show_results)
    cmp_button.grid(row=8, column=2, sticky=tk.W, padx=4, pady=4)
    
#     graph_button = tk.Button(button_frame, text='graph', width=10, command=runtime_graph)
#     graph_button.grid(row=8, column=2, sticky=tk.W, padx=4, pady=4)
    
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
#     compare_frame.columnconfigure(0, weight=1, uniform=1)
#     compare_frame.columnconfigure(1, weight=1, uniform=1)
#     compare_frame.columnconfigure(2, weight=1, uniform=1)
    
    tk.Label(compare_frame, text='Compare', anchor=tk.W, width=20).grid(row=0, sticky=tk.W)
    tk.Label(compare_frame, text='BFS', anchor=tk.W, width=10).grid(row=0, column=1, sticky=tk.W)
    tk.Label(compare_frame, text='DFS', anchor=tk.W).grid(row=0, column=2, sticky=tk.W)
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
    
    bfs_frame = tk.Frame(right, width=10, height=10)
    bfs_frame.pack_propagate(0)
    bfs_frame.grid(row=0, column=0, sticky='nsew')
    bfs_frame.grid_columnconfigure(0, weight=1)
    bfs_frame.grid_rowconfigure(1, weight=1)
    
    dfs_frame = tk.Frame(right, width=10, height=10)
    dfs_frame.pack_propagate(0)
    dfs_frame.grid(row=0, column=1, sticky='nsew')
    dfs_frame.grid_columnconfigure(0, weight=1)
    dfs_frame.grid_rowconfigure(1, weight=1)
    
    cmp_frame = tk.Frame(right, width=10, height=10)
    cmp_frame.pack_propagate(0)
    cmp_frame.grid(row=1, column=0, sticky='nsew')
    cmp_frame.grid_columnconfigure(0, weight=1)
    cmp_frame.grid_rowconfigure(1, weight=1)
    
    info_frame = tk.Frame(right, width=10, height=10)
    info_frame.pack_propagate(0)
    info_frame.grid(row=1, column=1, stick='nsew', padx=4, pady=4)
    info_frame.grid_columnconfigure(0, weight=1)
    
    tk.Label(bfs_frame, text='BFS', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    tk.Label(dfs_frame, text='DFS', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    tk.Label(cmp_frame, text='Compare graph', anchor=tk.CENTER).grid(row=0, padx=4, pady=2)
    
    # Create canvases and turtles
    bfs_canvas = tk.Canvas(bfs_frame, **border_params)
    bfs_canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    bfs_turtle = turtle.RawTurtle(bfs_canvas)
    
    dfs_canvas = tk.Canvas(dfs_frame, **border_params)
    dfs_canvas.grid(row=1, sticky='nsew', padx=4, pady=4)
    dfs_turtle = turtle.RawTurtle(dfs_canvas)
    
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
    desc = 'MATCHSTICK AI\n\nSome specifications:'\
    +'\n1. This program is gui based, there is no command line interaction with the user.'\
    +'\n2. The gui is fully capable of handling all user inputs.'\
    +'\n3. For all the options specified in the project description a button is implemented, please use them.'\
    +'\n\n\n'
    print(desc)
    
    
    # Set default values in entry fields
    n, p, m = (3, 100, 6)
    n_var.set(n)
    p_var.set(p)
    m_var.set(m)
    
        
    ai = Ai(n, p, m, status_bar)
    
    
    root.mainloop()
    
    
    