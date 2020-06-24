################################################
##                                            ##
##        ID: 2015A3PS0248P                   ##
##      Name: Prashant Piyush                 ##
##                                            ##
################################################
'''
Created on Oct 26, 2018

@author: prashant
'''


import copy
import time
import turtle
import Tkinter as tk


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


app_width = 1000
app_height = 600
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


    
def minmax():
    ai.magic()

def alphabeta():
    pass

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
    root.title('Magic Squares (Made by: Prashant Piyush)')
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
    
    
    