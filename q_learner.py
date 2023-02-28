import random
import numpy as np
from maze import *

class QLearner:
    """
    A class for a Q-learning agent that learns to navigate a maze.

    Attributes:
    -----------
    maze : Maze
        The maze that the agent navigates.
    alpha : float
        The learning rate of the agent. Default is 0.1.
    gamma : float
        The discount factor of the agent. Default is 0.9.
    epsilon : float
        The exploration rate of the agent. Default is 0.3.

    q_table : numpy array
        A 3-dimensional numpy array that stores the Q-values for each state-action pair in the maze.
        The shape of the array is (maze.lin, maze.col, 4), where the last dimension represents the 4 possible
        actions: 'north', 'south', 'east', 'west'.
    """
    def __init__(self, maze, alpha=0.1, gamma=0.9, epsilon=0.3):
        """
        Initializes a QLearner instance.

        Parameters:
        -----------
        maze : Maze
            The maze that the agent navigates.
        alpha : float, optional
            The learning rate of the agent. Default is 0.1.
        gamma : float, optional
            The discount factor of the agent. Default is 0.9.
        epsilon : float, optional
            The exploration rate of the agent. Default is 0.3.
        """
        self.maze = maze
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((self.maze.lin, self.maze.col, 4))
    
    def get_action(self, cell):
        """
        Chooses an action for the agent based on the current state.

        Parameters:
        -----------
        cell : Cell
            The current state of the agent.

        Returns:
        --------
        str
            The action chosen by the agent. It can be one of the following strings: 'north', 'south', 'east', 'west'.
        """
        if np.random.uniform() < self.epsilon:
            # random action
            return random.choice(['north', 'south', 'east', 'west'])
        else:
            # greedy action
            x = cell.x
            y = cell.y
            q_values = self.q_table[x, y]
            max_q = np.max(q_values)
            actions = []
            for i in range(4):
                if q_values[i] == max_q:
                    actions.append(i)
            action_index = np.random.choice(actions)
            return ['north', 'south', 'east', 'west'][action_index]
    
    def learn(self, start_cell, goal_cell, avoid_cell):
        """
        Trains the agent using Q-learning algorithm to navigate from the starting cell to the goal cell
        while avoiding the avoid_cell.

        Parameters:
        -----------
        start_cell : Cell
            The starting cell of the agent.
        goal_cell : Cell
            The goal cell of the agent.
        avoid_cell : Cell
            The cell that the agent must avoid.

        Returns:
        --------
        None
        """
        #Start learning
        for episode in range(2000):
            current_cell = start_cell
            while current_cell != goal_cell:
                # choose an action
                action = self.get_action(current_cell)
                x = current_cell.x
                y = current_cell.y
                
                # take the action and observe the new state and reward
                if action == 'north':
                    if x == 0:
                        # invalid move
                        continue
                    next_cell = self.maze.cells[x-1][y]
                elif action == 'south':
                    if x == self.maze.lin-1:
                        # invalid move
                        continue
                    next_cell = self.maze.cells[x+1][y]
                elif action == 'east':
                    if y == self.maze.col-1:
                        # invalid move
                        continue
                    next_cell = self.maze.cells[x][y+1]
                elif action == 'west':
                    if y == 0:
                        # invalid move
                        continue
                    next_cell = self.maze.cells[x][y-1]
                    
                next_x = next_cell.x
                next_y = next_cell.y
                reward = 0
                if next_cell == goal_cell:
                    reward = 1
                if next_cell == avoid_cell:
                    reward = -1
                # update Q table
                old_q = self.q_table[x, y, ['north', 'south', 'east', 'west'].index(action)]
                next_q = np.max(self.q_table[next_x, next_y])
                new_q = (1 - self.alpha) * old_q + self.alpha * (reward + self.gamma * next_q)
                self.q_table[x, y, ['north', 'south', 'east', 'west'].index(action)] = new_q
                
                # move to the next cell
                current_cell = next_cell

    def learn_from_prize(self):
        """
        This method initiates the Q-learning algorithm to find the optimal path from the prize cell to the start cell, 
        avoiding the finish cell. It calls the `learn` method with the `start_cell`, `prize_cell`, and `finish_cell` 
        as arguments.
        """
        self.learn(self.maze.prize_cell,self.maze.start_cell,self.maze.finish_cell)

    def learn_from_finish(self):
        """
        This method initiates the Q-learning algorithm to find the optimal path from the finish cell to the start cell, 
        avoiding the prize cell. It calls the `learn` method with the `start_cell`, `finish_cell`, and `prize_cell` 
        as arguments.
        """
        self.learn( self.maze.finish_cell,self.maze.start_cell,self.maze.prize_cell)