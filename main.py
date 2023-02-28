from maze import Maze
import os
from q_learner import QLearner
import argparse
import copy
import random

def create_dir(root):
    """Create a directory and its parent directories if they do not already exist.
    Args:
        root (str): The directory to create.

    Raises:
        OSError: If the directory could not be created.
    """
    try:
        os.makedirs(root)
    except FileExistsError:
    # directory already exists
        pass

parser = argparse.ArgumentParser()
parser.add_argument("--Save",help='Folder to save outputs',action='store_true')
parser.add_argument("--Draw",help='Print outputs',action='store_true')
parser.add_argument("--seed",help='Random seed for reproducibility',type=int,default=40)
parser.add_argument("--rows",help='Number of rows in the maze',type=int,default=4)
parser.add_argument("--cols",help='Number of columns in the maze',type=int,default=4)
parser.add_argument("--nsample",help='Number of mazes generated',type=int,default=10)
args = parser.parse_args()


random.seed(args.seed)

maze = Maze(args.rows, args.cols)
maze.init_maze()
# Learn a way from start to prize and from prize to start
learner1 = QLearner(maze)
learner2 = QLearner(maze)
learner1.learn_from_finish()
learner2.learn_from_prize()

if args.Save:
    create_dir("Mazes")
    create_dir("Mazes/"+str(args.rows)+"X"+str(args.cols))

for i in range(args.nsample):
    maze_i = copy.deepcopy(maze)
    maze_i.pave_qtable(learner1.q_table,learner2.q_table)
    if args.Draw:
        print("*"*100+"\n")
        print("Maze "+str(i)+" :")
        maze_i.draw()
    if args.Save:
        maze_i.plot("Mazes/"+str(args.rows)+"X"+str(args.cols)+"/"+str(i)+".jpg")