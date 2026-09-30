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