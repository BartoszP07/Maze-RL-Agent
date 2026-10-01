# Import libraries
import pygame

# Use a class to construct the player
class Player:
    # Initialise the player class
    def __init__(self, start_x, start_y, tile_size):
        self.x = start_x
        self.y = start_y
        self.size = tile_size
        
        # Size offset so the player can easily be seen
        self.size_offset = self.size/2
        
        # Create the player rect
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        
        
    # Subroutine to move the player around the maze
    def Move(self, direction, grid):
        
        new_x = self.x
        new_y = self.y
        
        # Define the directions
        if direction == "up":
            new_y -= 1
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
            
        # Check if the move is valid -- so empty space (0) or target space (3)
        if (grid[new_y][new_x] == 0 or grid[new_y][new_x] == 3):
            self.x = new_x
            self.y = new_y
        
    # Draw the player
    def Draw(self, screen):
        # Calculate the x and y based on the grid coordinates
        x = (self.x * self.size) + self.size_offset/4
        y = (self.y * self.size) + self.size_offset/4

        
        # Draw the rect
        pygame.draw.rect(screen, (0, 200, 0), (
            x,
            y,
            self.size - self.size_offset/2,
            self.size - self.size_offset/2
        ))