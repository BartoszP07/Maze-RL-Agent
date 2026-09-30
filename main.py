# Import modules
import pygame, sys
from scripts import *

# Set the recursion limit to be larger to allow for larger mazes
sys.setrecursionlimit(10_000)

# Use a class to structure the maze
class Maze:
    # Initialize the class
    def __init__(self):
        # Get the settings for the game
        self.settings = GLOBAL_SETTINGS
        # Create the screen and components
        self.screen = pygame.display.set_mode(self.settings["Window-Size"])
        # Check if the window should be fullscreen
        if (self.settings["Fullscreen"]): # Should be fullscreen
            if (not pygame.display.is_fullscreen()):
                pygame.display.toggle_fullscreen()
        else:
            if (pygame.display.is_fullscreen()): # Should be windowed
                pygame.display.toggle_fullscreen()
                
        # Create clock for the game to run with
        self.clock = pygame.time.Clock()
        # Create delta time variable to use for frame independency
        self.delta_time = 0
        
        # Get the maze object
        self.maze = CreateMaze(self.settings["Window-Size"][0], self.settings["Window-Size"][1], 25, 25, 40)
        
        # Change the screen size based on the amount of rows, columns and the tile size
        
        new_screen_w = self.maze.width * self.maze.tile_width
        new_screen_h = self.maze.height * self.maze.tile_height
        pygame.display.set_mode((new_screen_w, new_screen_h))
        
        # Create the maze
        self.maze.CreateMaze()
        
    # Subroutine to stop close the game
    def QuitGame(self):
        pygame.quit()
        sys.exit()
        
    # Subroutine to handle pygame events
    def Events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.QuitGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.maze.CreateMaze();
    
    # Subroutine to handle updating the game
    def Update(self):
        pass
    
    # Subroutine to render the game assets
    def Draw(self):
        # Draw a solid colour for background
        self.screen.fill((255, 255, 255))
        
        self.maze.Draw(self.screen)
        
    # Subroutine to run the game loop
    def Run(self):
        while True:
            # Set the fps and get the delta time value
            self.delta_time = self.clock.tick(self.settings["Fps"]) / 1000
            
            # Call the subroutines to run the game
            self.Events()
            self.Update()
            self.Draw()
            
            # Update the window
            pygame.display.flip()
            
if (__name__ == "__main__"):
    game = Maze()
    game.Run()