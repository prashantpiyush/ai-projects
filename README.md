# ai-projects
Projects done for Artificial Intelligence course at BITS Pilani


## How to run
Only requirement is `Tkinter` which can be installed on a ubuntu using the following command
```
sudo apt-get install python3-tk
```
1. Move to any project directory using `cd`
2. Run the main program using `python main.py`


## Project Descriptions
Projects:
1. Matchstick problem
2. Container stacking problem
3. Magic square genrator
4. Checkers bot
5. Solving First-Order logic using Bayesian Network


### Matchstick problem
A predefined arrangement of match sticks is given, where they only form square. The position of flameable object on the match stick is
irrelavant for the problem. Each square can have a side containing only 1 match stick, or 2 stick on each, or 3 and so on.

Given a starting arrangement of the matchsticks, containing some number of squares and an end goal defined by the number of square, program a bot such that it 
reaches the end goal using minimum number of moves. And, in one move the intelligent angent can remove only one square. After all the moves are completed, each 
each matchstick should be a part of a square and the final arrangement should contain exactly the number of squares as defined by the end goal.

```
# defining the number of squares
 _ _ _         _ _ _
|_|_|_|       |_|   |
|_|_|_|       |_|_ _|
|_|_|_|       |_|_|_|
contains      contains only
9 squares     6 squares
```

A `grid_size: int`, `percentage_cover: int` and `goal: int` values are provided to the program. The program generates a random arrangement of matchsticks with size of grid given in
input containing only `floor(grid_size * grid_size * percentage_cover * 0.01)` number of squares. Basically, only `percentage_cover` percent of squares of the 
full grid.

Then the bot tries to find the solution using seaching algorithms, namely BFS and DFS.

![](images/matchstick_1.png?raw=true)
![](images/matchstick_2.png?raw=true)
![](images/matchstick_3.png?raw=true)


### Container stacking problem
A yard scenario is given where containers are stacked temproarly in order to later load them on a ship or dispatch them to some external users.

Given a initial arrangement of containers and a final arrangement, program a bot which reaches the end goal in best min time it can. The solution doesn't have
to be optimal on number of moves, a good enough solution, which takes relatively less time to find, is accepted. In one move, the agent can move any top container
from any stack to any other stack.

The agent uses **A*** **(A-star)**, **Hill climbing** and **Greedy Breadth-First Search (GBFS)** techniques mixed with different heuristics.

Heuristics
- Out of place: +1 if the container is simply not at its final position
- How many moves will it take
  - +1 if the current container is at a different height compared to its height in the goal arrangement
  - +1 if the current container is in a different stack than the goal stack

![](images/container_1.png?raw=true)
![](images/container_2.png?raw=true)


### Magic Square generator
Cosider creating the magic square as **Constraint Satisfaction Problem**. Now create an agent, which generates a magic square of given size by modeling 
a magic square as a CSP.
```
# consider a 3 x 3 magic square
a1 a2 a3
a4 a5 a6
a7 a8 a9

These are the values of which make up the square. Then as a CSP the following should hold true
a1 + a2 + a3 = a4 + a5 + a6
             = a7 + a8 + a9
             = a7 + a5 + a3
             = a1 + a5 + a9
for each i, ai should belong to set {1, 2, 3, ..., n*n} where and n = size of grid
and
for each i and j, ai != aj if i != j
```

The program uses DFS + Back tracking with/whithout contraint propagation to find a magic square which satisfies all the contstraints.
**Degree heuristic** and **Minimum remaining value (MRV) heuristics** are used.

```
Enter grid size (Enter 0 to show analysis): 3
Choose executing algorithm:
1. DFS + BT
2. DFS + BT + Constraint Propagation
Enter [1/2]: 2
Choose heuristic of variable ordering: 
1. No heuristic (default order)
2. Minimum remaining value (MRV)
3. Degree heuristic
Enter [1/2/3]: 2
Magic square grid:
2  7  6  
9  5  1  
4  3  8  
Do you want to Continue?
Enter [y/n]: y

Enter grid size (Enter 0 to show analysis): 0


The following values are computed for grid size 3.


(a) DFS + BT
R1. Nodes generated: 187769
R2. Mem. allocated to one node: 2160 bytes
R3. Max stack size: 9
R4. Time to compute values: 2.744sec
R5. Node generated (MRV): 187769


(b) DFS + BT + Constraint Propagation
R6. Nodes generated: 11473
R7. Computer ratio: 0.938
R8. Time to compute values: 0.98sec


Do you want to Continue?
Enter [y/n]: n
```


### Chekers bot
Create an intelligent bot using DFS and backtracking which can play chekers.

Bot uses **Min-Max algorithm** enhanced with **Alpha-Beta pruning** to find a best possible solution at any given game state.

Note: To make a move, first select a green coin and then select the position where you want to move it. Blue is opponent (bot).

Note: Option1 - show empty board. Option2 - use Min-max for bot. Option3 - use Min-max with Alpha-beta for bot algorithm. Option4 - show statistics.

![](images/chekers_1.png?raw=true)
![](images/chekers_2.png?raw=true)


### Solving First-Order logic using Bayesian Network
Create a bot which can answer first-order query logic. Given the probabilities of some variables, find the probabiliy of a set of selected variables given 
another set of selected conditional variables.

Bot uses **Bayesian Network** to model first order logic and concept of **Markov blanket** and chain rule.

**Markov Blanket:** A node is conditionally independent of all other nodes in the network, given its parents, children, and children’s parents — that is,
given its Markov blanket.

Note: first select a set of query variables and then conditional variables. Click on show probabilty to view the calculated probability.

![](images/bayes_1.png?raw=true)
![](images/bayes_2.png?raw=true)
![](images/bayes_3.png?raw=true)

