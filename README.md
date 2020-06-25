# ai-projects
Projects done for Artificial Intelligence course at BITS Pilani


## How to run
The only requirement is `Tkinter` which can be installed on Ubuntu using the following command
```
sudo apt-get install python3-tk
```
1. Move to any project directory using `cd`
2. Run the main program using `python main.py`


## Project Descriptions
Projects:
1. Matchstick problem
2. Container stacking problem
3. Magic square generator
4. Checkers bot
5. Solving First-Order logic using Bayesian Network


### Matchstick problem
A random pattern of matchsticks is given, where each matchstick is part of a square. The squares
can be of any sizes, comprising of 1 matchstick each on all four sides, or 2 sticks on each side,
and so on. The position of the flammable object on the stick is irrelevant to the problem.

In one move, the intelligent agent can remove only one matchstick. Create a bot such that it can
reach from an initial arrangement to the end goal, using a minimum number of moves. The end goal is
defined by the desired number of squares in the final arrangement of sticks. Also, in the final
position, each stick must be part of a square.

```
# defining the number of squares
 _ _ _         _ _ _             _ _ _
|_|_|_|       |_|   |           | |_ _|
|_|_|_|       |_|_ _|           |_|_|_|
|_|_|_|       |_|_|_|           |_|_|_|
contains    contains only    invalid start/end
9 squares     6 squares         position
                            contains rectangles
```

A `grid_size: int`, `percentage_cover: int` and `goal: int` values are provided to the program. The
program generates a random arrangement of matchsticks with the size of the grid given in
input containing only `floor(grid_size * grid_size * percentage_cover * 0.01)` number of squares.
Only `percentage_cover` percent of squares of the full grid.

Then the bot tries to find the solution using searching algorithms, namely BFS and DFS.

![](images/matchstick_1.png?raw=true)
![](images/matchstick_2.png?raw=true)
![](images/matchstick_3.png?raw=true)


### Container stacking problem
Consider a yard situation, where containers are stacked temporarily to later load them on a ship,
or dispatch them to some external users.

Write a bot that can reach the end goal from a given initial arrangement of containers. In one move
the bot can relocate any of the top containers to the top of another stack. It is not necessary to
find the path which uses the minimum number of moves but, to create a good enough solution to
achieve the goal arrangement.

The agent uses **A*** **(A-star)**, **Hill climbing** and **Greedy Breadth-First Search (GBFS)**
techniques mixed with different heuristics.

**Heuristics used:**
- Out of place: +1 if the container is simply not at its final position
- How many moves will it take
  - +1 if the current container is at a different height compared to its height in the goal arrangement
  - +1 if the current container is in a different stack than the goal stack

![](images/container_1.png?raw=true)
![](images/container_2.png?raw=true)


### Magic Square generator
Consider creating the magic square as **Constraint Satisfaction Problem**. Now create an agent,
which generates a magic square of a given size by modeling
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

The program uses DFS + Backtracking with/without constraint propagation to find a magic square that
satisfies all the constraints.
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


### Checkers bot
Create an intelligent bot using DFS and backtracking which can play checkers.

The bot uses the **Min-Max algorithm** enhanced with **Alpha-Beta pruning** to find the best
possible solution at any given game state.

Note: To make a move, first select a green coin and then select the position where you want to move
it. Blue is an opponent (bot).

Note: Option1 - show empty board. Option2 - use Min-max for bot. Option3 - use Min-max with
Alpha-beta for bot algorithm. Option4 - show statistics.

![](images/checkers_1.png?raw=true)
![](images/checkers_2.png?raw=true)


### Solving First-Order logic using Bayesian Network
Create a bot that can answer first-order query logic. Given the probabilities of some variables,
find the probability of a set of selected variables given
another set of selected conditional variables.

The bot uses **Bayesian Network** to model first-order logic and concept of **Markov blanket** and
chain rule.

**Markov Blanket:** A node is conditionally independent of all other nodes in the network, given
its parents, children, and children’s parents — that is,
given its Markov blanket.

Note: first select a set of query variables and then conditional variables. Click on show
probability to view the calculated probability.

![](images/bayes_1.png?raw=true)
![](images/bayes_2.png?raw=true)
![](images/bayes_3.png?raw=true)

