# Import modules
import random, pygame, math

# Use a class to handle the maze environment logic
class CreateMaze():
    # Initialize the class
    def __init__(self, screen_width, screen_height, columns, rows, tile_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calculate the tilesize based on the window size and the maze size
        self.width = columns if columns % 2 != 0 else columns + 1
        self.height = rows if rows % 2 != 0 else rows + 1
        
        
        # Calculate the exact tile size to fill the screen
        self.tile_width = tile_size
        self.tile_height = tile_size
        
        # Fill the grid array with number 1's
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        
        # Keep the start coordinates
        self.start_x = 0
        self.start_y = 0
        
    # Function to return a random empty point on the maze grid
    def FindEmptyPoint(self, avoid_coords=[]):
        while True:
            x = random.randint(1, self.width - 1)
            y = random.randint(1, self.height - 1)

            if (x != y):
                if (self.grid[y][x] == 0 and [x, y] not in avoid_coords):
                    return (x, y)
        
    # Subroutine to create the maze
    def CreateMaze(self):
        # Fill the grid array with number 1's
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]
        self.GenerateMaze(1, 1)
        
        # Pick any 2 random points on the grid
        # Start pos
        self.start_x, self.start_y = self.FindEmptyPoint()
        # End pos
        end_x, end_y = self.FindEmptyPoint(avoid_coords=[[self.start_x, self.start_y]])
        # Add this point to the grid
        self.grid[end_y][end_x] = 3
        
    # Subroutine to generate the maze
    def GenerateMaze(self, start_x, start_y):
        # Set the start position of the maze grid to a 0 (empty)
        self.grid[start_y][start_x] = 0
        
        # Use a stack to generate the maze instead of recursion to exceed recursive limits
        stack = [(start_x, start_y)]
        
        # Runs until the stack is empty, meaning the maze is finished
        while len(stack) > 0:
            # Get the first position from the stack
            curr_x, curr_y = stack[-1]
        
            # Define the directions the generator can go
            # Make each direction take 2 steps to avoid walls as much as possible
            directions = [(0, -2), (0, 2), (2, 0), (-2, 0)]
            
            # Randomise the directions each recursive call to make the maze random
            random.shuffle(directions)
            
            # Create a flag to see if the worker has moved
            moved = False
            
            # Go through each direction
            for dir_x, dir_y in directions:
                # Calculate the next position for the maze
                next_x = dir_x + curr_x
                next_y = dir_y + curr_y
                
                # Make sure the next position is still inside the grid
                if ((next_x > 0 and next_x < self.width) and (next_y > 0 and next_y < self.height)):
                    # Check if this space is a wall
                    if (self.grid[next_y][next_x] == 1):
                        # Make an empty space
                        self.grid[curr_y + (dir_y // 2)][curr_x + (dir_x // 2)] = 0
                        
                        self.grid[next_y][next_x] = 0
                        
                        # Add the new position to the stack
                        stack.append((next_x, next_y))
                        
                        # Set the moved flag to true
                        moved = True
                        break
            
            # If there was no move, delete the last posiiton
            if not moved:
                stack.pop()
                    
    # Subroutine to draw the maze
    def Draw(self, screen):
        # Go through the maze coordinates
        for y, row in enumerate(self.grid):
            for x, item in enumerate(row):
                colour = (255, 255, 255)
                if item == 1: colour = (25, 25, 25)
                elif item == 2: colour = (0, 175, 0)
                elif item == 3: colour = (175, 0, 0)
                    
                if item != 0:
                    x_pos = x * self.tile_width
                    y_pos = y * self.tile_height
                    pygame.draw.rect(screen, colour, (x_pos, y_pos, self.tile_width, self.  tile_height))