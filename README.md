# Overview

This Python code implements a Q-learning algorithm to generate and solve a maze. The user can specify the number of rows and columns in the maze, the number of mazes to generate, and whether to save or print the output. The Q-learning algorithm is implemented in the QLearner class, and the maze generation and visualization is implemented in the Maze class.

The Q-learning algorithm works by maintaining a Q-table, which is a table of values that represent the expected reward for taking a particular action in a particular state. The algorithm learns by exploring the maze and updating the Q-table based on the rewards received at each step. Once the Q-table has been learned, it can be used to navigate the maze by selecting the action with the highest expected reward at each step.

In this implementation, two Q-learners are used, one to learn a path from the start to the prize, and one to learn a path from the start to the finish. These two paths are then combined and used to generate a Maze by destroying walls while exploring both Q-tables, randomness is introduced by random exploration of said tables in some cases and dead-ends addition.

# Maze Generation

The Maze class is responsible for generating and visualizing the maze. The maze is represented as a grid of cells, with each cell having walls on its north, south, east, and west sides. The walls are initially set to all be present, and then removed to create a path through the maze.

In this implementation, the difficulty of the maze is controlled by the number of dead-ends in the maze. Dead-ends are created by having one of the Q-learners pave the path from the start to the prize, and the other Q-learner pave the path from the start to the finish, with the two paths being separated by adding negative reward for arriving on the opposite cell to ensure that the paths do not overlap. The Q-tables are also used by choosing also random cells as the target, this creates dead-ends in the maze, which can make it more challenging to solve.

# Feasibility of Modeling Inner Walls

Modeling the maze using the binary state of all inner walls is not feasible because the size of the Q-table would be exponential in the number of cells in the maze. For example, if the maze has n cells, there are (n-1) vertical walls and (n-1) horizontal walls, for a total of 2n-2 walls. Each wall can be either present or absent, so the total number of possible states is 2^(2n-2), combined with the number of possible actions in each state 2n-2, the size of the Q-table is 2^(2n-2)*(2n-2). This is an extremely large number (around 400M for n = 4),  and it would be impractical to learn a Q-table of this size.

# Difficulty of Generated Maze

One way to quantify the difficulty of the generated maze is to measure the length of the shortest path from the start to the finish. This can be done by using Dijkstra's algorithm to compute the shortest path through the maze, and then measuring the length of that path. Another way to quantify the difficulty of the maze is to count the number of dead-ends in the maze. Dead-ends introduction is implemented in this version as described before.

# Deployment Instructions

To reproduce the results of this code, follow these steps:

Clone the Git repository to your local machine.
Install the required dependencies by running pip install -r requirements.txt.
Run the code using the command python main.py --rows <num_rows> --cols <num_cols> --nsample <num_mazes> [--Save] [--Draw] [--seed <random_seed>].
where <num-rows> and <num-cols> specify the number of rows and columns in the maze, respectively, and <num-samples> specifies the number of mazes to be generated. The --Save flag tells the script to save the generated mazes in the specified directory. If you want to print the mazes in the console, add the --Draw flag as well.

The generated mazes will be saved in the Mazes/<num-rows>X<num-cols> directory, where <num-rows> and <num-cols> are the number of rows and columns in the maze, respectively.

To quantify the difficulty of the generated mazes, one possible approach is to compute various metrics such as the length of the shortest path from the start to the prize, the number of dead-ends, and the average length of dead-ends. These metrics can be computed using the functions provided in the maze.py file.

To reproduce the results in the Mazes folder, rerun the main.py script with default parameters except for rows and cols. You can modify the hyperparameters such as the random seed and the number of samples, and rerun the main.py script. Note that the results may vary depending on the random seed and other factors.