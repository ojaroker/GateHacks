from game_logic import Game
from ui import UserInterface
import json

def main():
    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)
    
    with open('data/success_probabilities.json', 'r') as file:
        success_probabilities = json.load(file)

    # Prompt user for the number of bot players
    num_bot_players = 0
    while True:
        try:
            num_bot_players = int(input("Enter the number of bots you want to play against: "))
            if num_bot_players < 0:
                raise ValueError("The number of bots cannot be negative.")
            break  # Exit loop if valid input is given
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a non-negative integer.")

    # Total players include the human player
    num_players = num_bot_players + 1  # Assuming 1 human player

    # Initialize game and UI
    game = Game(valuation_data, success_probabilities, num_players)
    ui = UserInterface(game)

    # Start the game loop
    ui.start()

if __name__ == "__main__":
    main()
