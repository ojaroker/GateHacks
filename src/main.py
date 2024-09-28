from game_logic import Game
from ui import UserInterface
import json

def main():
    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)
    
    with open('data/success_probabilities.json', 'r') as file:
        success_probabilities = json.load(file)
    
    # Initialize game and UI
    game = Game(valuation_data, success_probabilities)
    ui = UserInterface(game)
    
    # Start the game loop
    ui.start()

if __name__ == "__main__":
    main()
