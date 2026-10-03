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
        # Create clock for the game to run with
        self.clock = pygame.time.Clock()
        # Create delta time variable to use for frame independency
        self.delta_time = 0
        
        # Set dimensions for the maze
        rows = 25
        cols = 25
        tile_size = 40
        
        # Get the maze object
        self.maze = CreateMaze(self.settings["Window-Size"][0], self.settings["Window-Size"][1], cols, rows, tile_size)
        
        # Change the screen size based on the amount of rows, columns and the tile size
        new_screen_w = self.maze.width * self.maze.tile_width
        new_screen_h = self.maze.height * self.maze.tile_height
        self.screen = pygame.display.set_mode((new_screen_w, new_screen_h))
        
        # Create the maze
        self.maze.CreateMaze()
        
        # Create the player
        self.player = Player(self.maze.start_x, self.maze.start_y, tile_size)
        
        # Create the agent object
        self.agent = RLAgent()
        
        # Add a tracker for the agent
        self.generation = 1
        self.max_steps = 500
        self.steps_taken = 0
        
    # Subroutine to run the AI simulation
    def RunSimulation(self):
        
        # Get the current position of the player
        current_state = (self.player.x, self.player.y)
        # Get the action from the agent
        action = self.agent.ChooseAction(current_state)
        # Get the next position from the player class
        next_x, next_y = self.player.GetNextPosition(action)
        
        # Update the steps taken by the ai
        self.steps_taken += 1
        
        # Update the ai with reward point and get it to learn
        # Check if the ai has found the end
        if (next_x == self.maze.end_x) and (next_y == self.maze.end_y):
            # Reward the ai massively
            reward = 1000
            # Get the next position
            next_state = (next_x, next_y)
            # Update the agents randomness
            self.agent.epsilon = max(self.agent.epsilon_min, self.agent.epsilon * self.agent.epsilon_decay)
            # Debug info
            print(f"Generation {self.generation} complete")
            print(f"New Epsilon: {self.agent.epsilon}")
            self.generation += 1
            
            # Move the player to the start for the next generation
            self.player.Move(self.maze.start_x, self.maze.start_y)
        
        # Check if hit a wall
        elif self.maze.grid[next_y][next_x] == 1:
            # Punish the ai
            reward = -100
            # Dont move the player
            next_state = current_state 
        
        # If just and empty space
        else:
            reward = -1
            next_state = (next_x, next_y)
            self.player.Move(next_x, next_y)

        # Get the ai to learn from this
        self.agent.Learn(current_state, action, reward, next_state)
        
        # Timeout this generation if taking too long
        if self.steps_taken >= self.max_steps:
            # Debug
            print(f"Generation: {self.generation} timeout!")
            
            # Restart the maze
            self.player.Move(self.maze.start_x, self.maze.start_y)
            
            # Update the epsilon for the agent to lower randomness
            self.agent.epsilon = max(self.agent.epsilon_min, self.agent.epsilon * self.agent.epsilon_decay)    
            
            # Increment the generation and reset steps
            self.generation += 1
            self.steps_taken = 0
        
    # Subroutine to regenerate the maze and reposition the player
    def RestartMaze(self):
        self.maze.CreateMaze()
        self.player.x = self.maze.start_x
        self.player.y = self.maze.start_y
        
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
                    self.RestartMaze()
                    
                if event.key == pygame.K_w:
                    self.player.Move("up", self.maze.grid)
                if event.key == pygame.K_s:
                    self.player.Move("down", self.maze.grid)
                if event.key == pygame.K_a:
                    self.player.Move("left", self.maze.grid)
                if event.key == pygame.K_d:
                    self.player.Move("right", self.maze.grid)
    
    # Subroutine to handle updating the game
    def Update(self):
        # Check if the current player position is the same as the end position
        # if (self.player.x == self.maze.end_x) and (self.player.y == self.maze.end_y):
        #     # Get a new maze
        #     self.RestartMaze()
            
        # Run the simulation
        self.RunSimulation()
    
    # Subroutine to render the game assets
    def Draw(self):
        # Draw a solid colour for background
        self.screen.fill((255, 255, 255))
        
        self.maze.Draw(self.screen)
        
        self.player.Draw(self.screen)
        
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