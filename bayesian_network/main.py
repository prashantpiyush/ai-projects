################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Nov 27, 2018

@author: prashant
'''

import os
import copy
import turtle
import tkinter as tk


graph = None
parents = None
probabilities = None
o = (-150, 100)
box_color = '#87d37c'
box_selected_color = '#fff68f'
box_disabled_color = '#dadfe1'
label_color = '#5c97bf'
box_width, box_height, box_pad = 70, 30, 5

query_box_co = (o[0]+150, o[1]-470)
query_box_width = 120
ans_box_co = (o[0]+150, o[1]-510)
ans_box_width = 120

submit_button_color = '#abb7b7'
submit_button_co = (o[0]+800, o[1]-470)
submit_button_width = 140
markov_button_co = (o[0]+800, o[1]-510)

markov_blanket_color = '#eeeeee'
markov_blanket_width = 330
markov_blanket_height= 20
markov_blanket_co = (o[0]+700, o[1]-10)

font = ("Arial", 10, "normal")

error_box_co = (o[0]+720, o[1]-110)
error_box_height = 200
error_box_width = 200
error_box_color = '#ff9478'
error_on = False

query_var_list = []
conditional_var_list = []

def init():
    global graph, parents, t, screen, query_var_pos, query_var_neg
    global conditional_var_pos, conditional_var_neg
    global query_var_selected, conditional_var_selected
    
    # parse input before creating buttons
    parse_input()
    
    t = ct.clone()
    ct.hideturtle()
    screen = t.getscreen()
    t.clear()
    screen.clear()
    screen.tracer(0)
    t.setpos(*o)
    t.penup()
    # 5 15 30
    def helper_show_buttons(offset, form='{}'):
        rectpos = {}
        for i, k in enumerate(sorted(graph.keys())):
            if i<=12:
                k = form.format(k)
                rectpos[k] = make_button(i, dk(k), offset, box_color)
            else:
                k = form.format(k)
                rectpos[k] = make_button(i-13, dk(k),
                                         offset+box_width+box_pad,
                                         box_color)
        return rectpos
    # query variable buttons
    offset = 10
    query_var_pos = helper_show_buttons(offset)
    offset += 2*box_width + 4*box_pad
    query_var_neg = helper_show_buttons(offset, form='{}_neg')
    
    # conditional variable buttons
    offset += 2*box_width + 60
    conditional_var_pos = helper_show_buttons(offset)
    offset += 2*box_width + 4*box_pad
    conditional_var_neg = helper_show_buttons(offset, form='{}_neg')
    
    query_var_selected = {k: 2 for k in query_var_pos}
    conditional_var_selected = {k: 2 for k in conditional_var_pos}
    
    make_button_xy(o[0]+100, o[1]+30, 'Query Variables', label_color, width=110)
    make_button_xy(o[0]+465, o[1]+30, 'Condition Variables', label_color, width=125)
    make_button_xy(o[0]+10, o[1]-470, 'Query Generated', label_color, width=120)
    make_button_xy(o[0]+150, o[1]-470, '', 'white', width=query_box_width)
    make_button_xy(o[0]+10, o[1]-510, 'Probability', label_color, width=120)
    make_button_xy(o[0]+150, o[1]-510, '', 'white', width=ans_box_width)
    
    make_button_xy(o[0]+800, o[1]-470, 'Click to compute', submit_button_color, width=submit_button_width)
    make_button_xy(o[0]+800, o[1]-510, 'Show markov blanket', submit_button_color, width=submit_button_width)
    
    make_button_xy(o[0]+750, o[1]+30, 'Markov Blanket', label_color, width=110)
    
    screen.update()
    screen.onclick(select_var)

# this function is equivalent to createBayesianNetwork(cause_effect_file)
def parse_input():
    global graph, parents, probabilities
    graph = {}
    parents = {}
    probabilities = {}
    with open(filepath, 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines[:-1:]:
            var = line.split(' >>')[0]
            children = line.split('[')[1].split(']')[0].split(', ')
            if '' in children:
                children.remove('')
            parents[var] = children
            probabilities[var] = list(map(float, line.split('>> ')[-1].split(' ')))
            
            graph[var] = graph.get(var, [])
            for k in children:
                clist = graph.get(k, None)
                if clist is None:
                    graph[k] = []
                graph[k].append(var)
    # end of parsing

# this function is equivalent to createExpression(query_variables Q, condition_variables C)
def update_query_box():
    global query_box_width
    make_button_xy(query_box_co[0], query_box_co[1], '', 'white', width=query_box_width, pencolor='white')
    query_box_width = (len(query_var_list) + len(conditional_var_list))*15 + 50
    query_box_width += sum([10 if k.endswith('neg') else 0 for k in query_var_list])
    query_box_width += sum([10 if k.endswith('neg') else 0 for k in conditional_var_list])
    def get_var(k):
        if k.endswith('neg'):
            return '~{}'.format(k.split('_')[0])
        else:
            return k
    form = 'P({} | {})' if len(conditional_var_list)>0 else 'P({})'
    query_string = form.format(', '.join(map(get_var, query_var_list)), ', '.join(map(get_var, conditional_var_list)))
    make_button_xy(query_box_co[0], query_box_co[1], query_string, 'white', width=query_box_width)
    
def display_probability():
    make_button_xy(ans_box_co[0], ans_box_co[1], '', 'white', width=ans_box_width)
    # p = str(compute_probability())
    p = "{:.4f}".format(compute_probability())
    make_button_xy(ans_box_co[0], ans_box_co[1], p, 'white', width=ans_box_width)

def gvn(k):
    if k.endswith('neg'):
        return k.split('_')[0]
    return k

def get_parents(v, l):
    rs = [k for k in l if gvn(k) in parents.get(v, [])]
    return rs

# this is computeProbability(MarkovBlanket M, expression E)
def compute_probability():
    q = copy.deepcopy(query_var_list)
    c = copy.deepcopy(conditional_var_list)
    v_list = q + c
    
    for k in q:
        if get_opk(k) in c:
            return 0.0
    if len(q)==0 or len(v_list)==0:
        return 'Invalid Query'
    
    prob = 1
    for v in v_list:
        prob *= p(v, get_parents(v, v_list))
    
    for v in c:
        prob /= p(v, get_parents(v, c))
    
    return prob

def btoi(s):
    if len(s)==0:
        return 0
    return 2*btoi(s[:-1]) + int(s[-1])

def p(q, c=[]):
    if len(parents.get(gvn(q), []))==0:
        if q.endswith('neg'):
            return 1 - probabilities[q.split('_')[0]][0]
        return probabilities[q][0]
    if len(c) == len(parents.get(gvn(q), [])):
        idx = ''
        for pv in parents.get(gvn(q), []):
            if pv in c:
                idx += '1'
            elif '{}_neg'.format(pv) in c:
                idx += '0'
        idx = btoi(idx)
        rs = probabilities[gvn(q)][idx]
        if q.endswith('neg'):
            return 1 - rs
        return rs
    parents_not_present = [k for k in parents.get(gvn(q), []) if k not in map(gvn, c)]
    pp = parents_not_present[0]
    pn = '{}_neg'.format(parents_not_present[0])
    rs = p(q, c+[pp])*p(pp) + p(q, c+[pn])*p(pn)
    return rs

def in_box(x, y, a, b, width=box_width, height=box_height):
    if a < x or a > x + width:
        return False
    if b > y or b < y - height:
        return False
    return True

def display_markov_blanket():
    global markov_blanket_height
    make_button_xy(markov_blanket_co[0], markov_blanket_co[1], '', 'white', width=markov_blanket_width, height=markov_blanket_height, pencolor='white')
    vs = copy.deepcopy(query_var_list) + copy.deepcopy(conditional_var_list)
    
    if len(vs)==0:
        return
    
    vs = set(map(gvn, vs))
    markov_blanket_height = len(vs) * 25
    make_button_xy(markov_blanket_co[0], markov_blanket_co[1], '', markov_blanket_color, width=markov_blanket_width, height=markov_blanket_height)
    
    for i, v in enumerate(vs):
        l = get_markov_blanket(v)
        t.penup()
        t.setpos(markov_blanket_co[0]+10, markov_blanket_co[1]-20-i*25)
        t.write('{} = {{ {} }}'.format(v,', '.join(l)), font=font)

# this function is equivalent to computeMarkovBlanket(BayesianNetwork B, node A)
def get_markov_blanket(v):
    mb = set()
    for k in graph[v]:
        mb.add(k)
        for p in parents[k]:
            mb.add(p)
    for k in parents[v]:
        mb.add(k)
    mb.add(v)
    return mb

def select_var(x, y):
    global error_on
    if error_on:
        make_button_xy(error_box_co[0], error_box_co[1], '', 'white', width=error_box_width, height=error_box_height, pencolor='white')
        error_on = False
    if in_box(submit_button_co[0], submit_button_co[1], x, y, width=submit_button_width):
        display_probability()
        return
    if in_box(markov_button_co[0], markov_button_co[1], x, y, width=submit_button_width):
        display_markov_blanket()
        return
    def helper_click_button(var_list, clicked, k, v, f):
        ok = k
        if ok.endswith('neg'):
            ok = k.split('_')[0]
        if clicked[ok]==2:
            var_list.append(k)
            clicked[ok] = f
            make_button_xy(v[0], v[1], dk(k), box_selected_color)
            make_button_xy(get_opc(v[0]), v[1], dk(get_opk(k)), box_disabled_color)
        elif clicked[ok]==f:
            var_list.remove(k)
            clicked[ok] = 2
            make_button_xy(v[0], v[1], dk(k), box_color)
            make_button_xy(get_opc(v[0]), v[1], dk(get_opk(k)), box_color)
        update_query_box()
    
    for k, v in query_var_pos.items():
        if in_box(v[0], v[1], x, y):
            if len(query_var_list)<10:
                helper_click_button(query_var_list, query_var_selected, k, v, 0)
            else: report()
            return
    for k, v in query_var_neg.items():
        if in_box(v[0], v[1], x, y):
            if len(query_var_list)<10:
                helper_click_button(query_var_list, query_var_selected, k, v, 1)
            else: report()
            return
    for k, v in conditional_var_pos.items():
        if in_box(v[0], v[1], x, y):
            if len(conditional_var_list)<10:
                helper_click_button(conditional_var_list, conditional_var_selected, k, v, 0)
            else: report()
            return
    for k, v in conditional_var_neg.items():
        if in_box(v[0], v[1], x, y):
            if len(conditional_var_list)<10:
                helper_click_button(conditional_var_list, conditional_var_selected, k, v, 1)
            else: report()
            return

def report():
    make_button_xy(markov_blanket_co[0], markov_blanket_co[1], '', 'white', width=markov_blanket_width, height=markov_blanket_height, pencolor='white')
    make_button_xy(error_box_co[0], error_box_co[1], '', 'white', width=error_box_width, height=error_box_height, pencolor='white')
    s = ['You can select a max of 10', 'variables in each of Q and C.']
    make_button_xy(error_box_co[0], error_box_co[1], '', error_box_color, width=error_box_width, height=error_box_height)
    t.penup()
    t.setpos(error_box_co[0]+10, error_box_co[1]-50)
    t.write(s[0], font=font)
    t.setpos(error_box_co[0]+10, error_box_co[1]-80)
    t.write(s[1], font=font)
    global error_on
    error_on = True
    
def get_opc(x):
    for k, v in query_var_pos.items():
        if in_box(v[0], v[1], x, v[1]):
            return x + 2*box_width + 4*box_pad
    for k, v in query_var_neg.items():
        if in_box(v[0], v[1], x, v[1]):
            return x - 2*box_width - 4*box_pad
    for k, v in conditional_var_pos.items():
        if in_box(v[0], v[1], x, v[1]):
            return x + 2*box_width + 4*box_pad
    for k, v in conditional_var_neg.items():
        if in_box(v[0], v[1], x, v[1]):
            return x - 2*box_width - 4*box_pad

def dk(k):
    if k.endswith('neg'):
        return "~{}".format(k.split('_')[0])
    return k

def get_opk(k):
    if k.endswith('neg'):
        return k.split('_')[0]
    else:
        return '{}_neg'.format(k)

def make_button(index, key, offset, color):
    x, y = o[0]+offset, o[1]-10-index*(box_height+box_pad)
    return make_button_xy(x, y, key, color)

def make_button_xy(x, y, key, color, width=box_width, height=box_height, pencolor='black'):
    t.setpos(x, y)
    t.pendown()
    t.pencolor(pencolor)
    t.fillcolor(color)
    t.begin_fill()
    rectangle(x, y, width, height)
    t.end_fill()
    t.penup()
    t.setpos(x+10, y-20)
    t.write(key, font=font)
    return (x, y)

def rectangle(x, y, w, h):
    t.setpos(x, y)
    t.setpos(x+w, y)
    t.setpos(x+w, y-h)
    t.setpos(x, y-h)
    t.setpos(x, y)

if __name__ == '__main__':
    
    filename = 'input1.txt'
    
    print("Choose an input file:")
    print("1. input1.txt")
    print("2. input2.txt")
    io = int(input("Enter [1/2]: "))
    while io!=1 and io!=2:
        io = int(input("Please enter a valid choice [1/2]: "))
    filename = 'input{}.txt'.format(io)
    
    root = tk.Tk()
    root.title('Probabilistic Reasoning (Made by: Prashant Piyush)')
    
    app_width, app_height = (1100, 600)
    
    root.geometry('{}x{}'.format(app_width, app_height))
    root.resizable(0, 0)
    root.grid_columnconfigure(0, weight=1, uniform=1)
    root.grid_rowconfigure(0, weight=1, uniform=1)
    
    border_params = {'highlightbackground':'black', 'highlightcolor':'black', 'highlightthickness':1}
    
    frame = tk.Frame(root, width=10, height=10, **border_params)
    frame.pack_propagate(0)
    frame.grid(sticky='nsew')
    frame.grid_columnconfigure(0, weight=1, uniform=1)
    frame.grid_rowconfigure(0, weight=1, uniform=1)
    
    canvas = tk.Canvas(frame, **border_params)
    canvas.grid(sticky='nsew', padx=4, pady=4)
    ct = turtle.RawTurtle(canvas)
    
    base_folder = '.'
    filepath = os.path.join(base_folder, filename)
    
    init()
        
    root.mainloop()
    
    
    
    
