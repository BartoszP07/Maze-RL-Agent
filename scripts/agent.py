# Import necessary libraries
import random, math


# Use a class to create the agent
class RLAgent():
    # Initialise the agent
    def __init__(self):
        # Define the action for the agent to use
        self.actions = ["up", "down", "left", "right"]
        
        # Create the "brain" dictionary
        self.q_table = {}
        
        # Epsilon variables for exploration and exploitation
        self.epsilon = 1 # -> used to determine randomness 0 - 1 (min - max)
        self.epsilon_decay = 0.995 # -> used to lower the randomness for each iteration
        self.epsilon_min = 0.01 # -> make the randomness for movement a minimum, not 0.
        
        # Parameters for the actual learning
        self.learning_rate = 0.1 # -> How aggressively the agent overrides new data with old data
        self.discound_factor = 0.9 # -> How much it values finding the exit vs taking an immediate safe step
        
    # Subroutine to get the q values
    def GetQValues(self, state):
        # The state is the current coordiante for the maze
        if state not in self.q_table:
            self.q_table[state] = {"up": 0, "down": 0, "left": 0, "right": 0}
        return self.q_table[state]
    
    # Subroutine for the agent to choose an action
    def ChooseAction(self, state):
        # Get a random number and compare it with the epsilon for randomness
        if (random.uniform(0, 1) < self.epsilon):
            return random.choice(self.actions)
        else:
            # Use the highest of the q values
            q_values = self.GetQValues(state)
            return max(q_values, key=q_values.get)
        
    # Get the agent to learn
    def Learn(self, state, action, reward, next_state):
        # Use Bellmans Equation
        
        # Get the current q values for the current state
        q_values = self.GetQValues(state)
        # Get the current q value for the given action
        current_q = q_values[action]
        # Get the next q values
        next_q_values = self.GetQValues(next_state)
        # Get the best score from these next q values
        max_next_q = max(next_q_values.values())
        
        # Bellmans equation
        temporal_difference = reward + (self.discound_factor * max_next_q) - current_q
        new_q = current_q + (self.learning_rate * temporal_difference)
        
        # Override the old score with the newly calculated one
        self.q_table[state][action] = new_q