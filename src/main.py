import json
import random
from game_logic import Game
from ui import UserInterface

def main():
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

    # Prompt user for the number of projects
    num_projects = 0
    while True:
        try:
            num_projects = int(input("Enter the number of projects: "))
            if num_projects <= 0:
                raise ValueError("The number of projects must be positive.")
            break  # Exit loop if valid input is given
        except ValueError as e:
            print(f"Invalid input: {e}. Please enter a positive integer.")

    # Generate random success probabilities for each project
    success_probabilities = [random.uniform(0.1, 1.0) for _ in range(num_projects)]  # Random probabilities between 0.1 and 1.0

    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)

    # Update the valuation matrix based on the number of players
    valuation_data["players"] = valuation_data["players"][:num_bot_players + 1]  # Trim to the desired number of players

    # If there are not enough players in the existing data, add new players
    for player_id in range(len(valuation_data["players"]) + 1, num_bot_players + 2):  # +2 because we are including the human player
        new_player_valuations = [1 / num_projects for _ in range(num_projects)]  # Equal distribution
        valuation_data["players"].append({
            "id": player_id,
            "valuations": new_player_valuations
        })

    # Save the updated valuation matrix back to the JSON file
    with open('data/valuation_matrix.json', 'w') as file:
        json.dump(valuation_data, file, indent=4)

    # Save success probabilities to JSON
    success_data = {
        "success_probabilities": success_probabilities
    }
    with open('data/success_probabilities.json', 'w') as file:
        json.dump(success_data, file, indent=4)

    # Initialize the game and UI
    game = Game(valuation_data, success_probabilities, num_bot_players + 1)
    ui = UserInterface(game)

    # Start the game loop
    ui.start()

if __name__ == "__main__":
    main()
