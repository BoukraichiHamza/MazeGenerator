import random
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import numpy as np

class Cell:
    """
    Represents a cell in the maze grid.

    Attributes:
        x (int): The x coordinate of the cell.
        y (int): The y coordinate of the cell.
        walls (list): A list of booleans representing whether there is a wall to the north, south, east, or west of the cell.
        is_prize (bool): True if the cell is a prize cell, False otherwise.
        is_start (bool): True if the cell is the start cell, False otherwise.
        is_finish (bool): True if the cell is the finish cell, False otherwise.
    """
    def __init__(self, x, y):
        """
        Initializes a new Cell object.

        Args:
            x (int): The x coordinate of the cell.
            y (int): The y coordinate of the cell.
        """
        self.x = x
        self.y = y
        self.walls = {'north': True, 'south': True, 'east': True, 'west': True}
        self.prize = False
        self.start = False
        self.finish = False

    def __eq__(self,other_cell):
        """
        Compares the cell with another cell for equality.

        Args:
            other_cell (Cell): The other cell to compare with.

        Returns:
            bool: True if the cells are equal (i.e., have the same x and y coordinates), False otherwise.
        """
        return (self.x == other_cell.x) and (self.y == other_cell.y)
    
    def __ne__(self,other_cell):
        """
        Compares the cell with another cell for inequality.

        Args:
            other_cell (Cell): The other cell to compare with.

        Returns:
            bool: True if the cells are not equal (i.e., have different x or y coordinates), False otherwise.
        """
        return (self.x != other_cell.x) or (self.y != other_cell.y)
    
    def __str__(self):
        """
        Returns a string representation of the cell.

        Returns:
            str: A string representing the cell in the format "(x, y)".
        """
        #return f"({self.x}, {self.y})" + str(self.walls)
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        """
        Returns a string representation of the Cell object.
        """
        return self.__str__()

class Maze:
    """
    This class represents a maze with randomly generated walls and a start, finish, and prize cell. 
    
    Attributes:
    - lines (int): the number of lines in the maze
    - columns (int): the number of columns in the maze
    - cells (numpy.ndarray): a 2D numpy array of Cell objects representing the cells in the maze
    - start_cell (Cell): the cell where the maze begins
    - finish_cell (Cell): the cell where the maze ends
    - prize_cell (Cell): the cell that contains the prize
    """
    def __init__(self, lines, columns):
        """
        Initializes a new Maze object with the specified number of lines and columns.
        
        Parameters:
        - lines (int): the number of lines in the maze
        - columns (int): the number of columns in the maze
        """
        self.lin = lines
        self.col = columns
        self.cells = np.array([[Cell(x, y) for y in range(columns)] for x in range(lines)])
        self.start_cell = None
        self.finish_cell = None
        self.prize_cell = None
    
    def __str__(self):
        """
        Returns a string representation of the maze.
        
        Returns:
        - str: a string representation of the maze
        """
        return str(self.cells)    
    
    def destroy_wall(self,cell,direction):
        """
        Removes the wall between a given cell and one of its neighbors in a specified direction.
        
        Parameters:
        - cell (Cell): the cell whose wall to remove
        - direction (str): the direction in which to remove the wall (north, south, east, or west)
        """
        row = cell.x
        col = cell.y
        if direction == "north" and row > 0:
            self.cells[row][col].walls["north"] = False
            self.cells[row-1][col].walls["south"] = False
        elif direction == "south" and row < self.lin-1:
            self.cells[row][col].walls["south"] = False
            self.cells[row+1][col].walls["north"] = False
        elif direction == "east" and col < self.col-1:
            self.cells[row][col].walls["east"] = False
            self.cells[row][col+1].walls["west"] = False
        elif direction == "west" and col > 0:
            self.cells[row][col].walls["west"] = False
            self.cells[row][col-1].walls["east"] = False

    def init_maze(self):
        """
        Initializes the maze by randomly setting the start, finish, and prize cells.
        """
        self.set_start()
        self.set_finish()
        self.set_prize()
    
    def set_start(self):
        """
        Sets the start cell to a random cell in the maze.
        """
        found = False
        while not(found):
            x = random.randint(0, self.lin-1)
            y = random.randint(0, self.col-1)
            cell = self.cells[x][y]
            found = not (cell.prize or cell.finish)
        cell.start = True
        self.start_cell = cell
    
    def set_finish(self):
        """
        Sets the finish cell to a random cell in the maze.
        """
        found = False
        while not(found):
            x = random.randint(0, self.lin-1)
            y = random.randint(0, self.col-1)
            cell = self.cells[x][y]
            found = not (cell.prize or cell.start)
        cell.finish = True
        self.finish_cell = cell
    
    def set_prize(self):
        """
        Sets the prize cell to a random cell in the maze.
        """
        found = False
        while not(found):
            x = random.randint(0, self.lin-1)
            y = random.randint(0, self.col-1)
            cell = self.cells[x][y]
            found = not (cell.finish or cell.start)
        cell.prize = True
        self.prize_cell = cell


    def draw(self):
        """
        Draws the current state of the maze by printing a textual representation of the maze.
        This method iterates through each cell in the maze, drawing its north and west walls and any
        special cell markers (e.g., start, finish, or prize). The textual representation is printed
        to the console.
        """
        for x in range(self.lin):
            # draw north walls
            for y in range(self.col):
                print('+', end='')
                if self.cells[x][y].walls['north']:
                    print('---', end='')
                else:
                    print('   ', end='')
            print('+')

            # draw west walls and height
            for y in range(self.col):
                if self.cells[x][y].walls['west']:
                    print('|', end='')
                else:
                    print(' ', end='')
                if self.cells[x][y].start:
                    print(' S ', end='')
                elif self.cells[x][y].finish:
                    print(' F ', end='')
                elif self.cells[x][y].prize:
                    print(' P ', end='')
                else:
                    print('   ', end='')
            print('|')

        # draw south walls
        for y in range(self.col):
            print('+', end='')
            if self.cells[x][y].walls['south']:
                print('---', end='')
            else:
                print('   ', end='')
        print('+')


    def plot(self,directory):
        """
        Plots the maze and saves the image to a given directory.
        Parameters:
        -----------
        directory : str
            The directory where the image of the plotted maze will be saved.
        """
        img_folder = 'Image/'

        fig, ax = plt.subplots(figsize=(self.col, self.lin))
        ax.set_xlim(0,self.col)
        ax.set_ylim(0,self.lin)

        for y in range(self.lin):
            for x in range(self.col):
                cell = self.cells[y][x]
                if cell.walls['north']:
                    ax.plot([x, x+1], [self.lin-y, self.lin-y], 'k-')
                if cell.walls['south']:
                    ax.plot([x, x+1], [self.lin-y-1, self.lin-y-1], 'k-')
                if cell.walls['west']:
                    ax.plot([x, x], [self.lin-y-1, self.lin-y], 'k-')
                if cell.walls['east']:
                    ax.plot([x+1, x+1], [self.lin-y-1, self.lin-y], 'k-')

                if cell.start:
                    start_img = mpimg.imread(img_folder + 'start.png')
                    ax.imshow(start_img, extent=(x, x+1, self.lin-y-1, self.lin-y))
                elif cell.finish:
                    end_img = mpimg.imread(img_folder + 'exit.png')
                    ax.imshow(end_img, extent=(x, x+1, self.lin-y-1, self.lin-y))
                elif cell.prize:
                    prize_img = mpimg.imread(img_folder + 'prize.jpg')
                    ax.imshow(prize_img, extent=(x, x+1, self.lin-y-1, self.lin-y))

        plt.axis('off')
        plt.savefig(directory,bbox_inches = 'tight',pad_inches = 0.1)
        plt.close()

    def path_exists(self, start, goal):
        """Checks whether there is a path between the start cell and the goal cell in the maze using depth-first search (DFS).
    
        Args:
            start (tuple): A tuple representing the (row, column) coordinates of the start cell.
        g   oal (tuple): A tuple representing the (row, column) coordinates of the goal cell.
    
        Returns:
            bool: True if there is a path between the start cell and the goal cell, False otherwise.
        """
        stack = [start]
        visited = []
        while len(stack)!=0:
            current_cell = stack.pop()
            if current_cell == goal:
                return True
            visited.append(current_cell)
            for neighbor in self.get_visitable_neighbors(current_cell):
                if neighbor not in visited:
                    stack.append(neighbor)
        return False
    
    def is_valid(self):
        """Check if the maze is valid by verifying if there exists a path from start to finish cell, 
        and a path from start to prize cell.

        Returns:
        --------
        bool:
            True if the maze is valid, False otherwise.
        """
        return self.path_exists(self.start_cell,self.finish_cell) and self.path_exists(self.start_cell,self.prize_cell)

    def get_visitable_neighbors(self, cell):
        """Returns a list of neighboring cells that can be visited from the given cell.

        Parameters:
        -----------
        cell : Cell
            The cell for which we want to get the neighboring cells.

        Returns:
        --------
        list of Cell:
            A list of neighboring cells that can be visited from the given cell.
        """

        neighbors = []
        x, y = cell.x, cell.y
        if x > 0 and not self.cells[x][y].walls['north']:
            neighbors.append(self.get_cell(x-1, y))
        if x < self.lin-1 and not self.cells[x][y].walls['south']:
            neighbors.append(self.get_cell(x+1, y))
        if y > 0 and not self.cells[x][y].walls['west']:
            neighbors.append(self.get_cell(x, y-1))
        if y < self.col-1 and not self.cells[x][y].walls['east']:
            neighbors.append(self.get_cell(x, y+1))
        return neighbors

    def pave_random_maze(self):
        """Randomly destroys walls between cells until a valid maze is generated."""
        while not (self.is_valid()):
            # Randomly select a cell in the maze
            row = random.randint(0, self.lin-1)
            col = random.randint(0, self.col-1)
            cell = self.cells[row][col]
            # Randomly select a neighboring cell to destroy a wall between
            directions = ["north", "south", "east", "west"]
            direction = random.choice(directions)
            self.destroy_wall(cell,direction)


    def pave_qtable_aux(self,q,begin_cell,randomizer=0):
        """Destroys walls between cells based on the given Q-table values and the target cell.

        Parameters:
        -----------
        q : numpy.ndarray
            A Q-table representing the Q-values for each state-action pair in the maze.
        begin_cell : Cell
            The cell from which the paving begins.
        randomizer : float
            The probability of choosing a random action instead of the one with maximum Q-value.

        Returns:
        --------
        None
        """
        #Destroy walls following q values and cell target
        current_cell = begin_cell
        target = self.start_cell
        while current_cell != target:
            x = current_cell.x
            y = current_cell.y
            q_xy = q[x,y]
            #Process Values for choices with weighted probability
            if np.random.uniform() < randomizer:
                # q_xy = [np.max((0.0,e)) for e in q_xy]
                # action = random.choices(['north', 'south', 'east', 'west'],weights=q_xy,k=1)[0]
                action = random.choice(['north', 'south', 'east', 'west'])
            else:
                c = np.argmax(q_xy)
                action = ['north', 'south', 'east', 'west'][c]
            #Destroy the wall and observe the new cell
            if action == 'north':
                if x == 0:
                    # invalid move
                    continue
                self.destroy_wall(current_cell,action)
                current_cell = self.cells[x-1][y]
            elif action == 'south':
                if x == self.lin-1:
                    # invalid move
                    continue
                self.destroy_wall(current_cell,action)
                current_cell = self.cells[x+1][y]
            elif action == 'east':
                if y == self.col-1:
                    # invalid move
                    continue
                self.destroy_wall(current_cell,action)
                current_cell = self.cells[x][y+1]
            elif action == 'west':
                if y == 0:
                    # invalid move
                    continue
                self.destroy_wall(current_cell,action)
                current_cell = self.cells[x][y-1]
    
    def pave_qtable(self,q1,q2):
        """Paves the maze based on the given Q-table values for the finish and prize cells, respectively.

        Parameters:
        -----------
        q1 : numpy.ndarray
            A Q-table representing the Q-values for each state-action pair with respect to the finish cell.
        q2 : numpy.ndarray
            A Q-table representing the Q-values for each state-action pair with respect to the prize cell.

        Returns:
        --------
        None
        """
        #Q1 for finish, Q2 for prize
        self.pave_qtable_aux(q1,self.finish_cell,0.2)
        self.pave_qtable_aux(q2,self.prize_cell,0.2)
        #Get randoms cells and add their path for creating dead-ends
        n_de = int(np.sqrt(self.lin*self.col))
        for i in range(n_de):
            #The used Cell mustn't be a target cell
            found = False
            while not(found):
                cell = self.cells[ random.randint(0, self.lin-1)][random.randint(0, self.col-1)]
                found = not (cell.prize or cell.finish or cell.start) and (cell.walls['north'] or cell.walls['east'] or cell.walls['south'] or cell.walls['west'])
            if i % 2 ==0:
                self.pave_qtable_aux(q1,cell,0.5)
            else:
                self.pave_qtable_aux(q2,cell,0.5)