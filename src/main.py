import json
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

    # Total players include the human player
    num_players = num_bot_players + 1  # Assuming 1 human player

    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)

    # Update the valuation matrix based on the number of players
    valuation_data["players"] = valuation_data["players"][:num_players]  # Trim to the desired number of players

    # If there are not enough players in the existing data, add new players
    for player_id in range(len(valuation_data["players"]) + 1, num_players + 1):
        # Create a new player with random valuations (you can customize this)
        new_player_valuations = [1 / len(valuation_data["projects"]) for _ in valuation_data["projects"]]  # Equal distribution
        valuation_data["players"].append({
            "id": player_id,
            "valuations": new_player_valuations
        })

    # Save the updated valuation matrix back to the JSON file
    with open('data/valuation_matrix.json', 'w') as file:
        json.dump(valuation_data, file, indent=4)

    # Initialize the game and UI
    game = Game(valuation_data, success_probabilities, num_players)
    ui = UserInterface(game)

    # Start the game loop
    ui.start()

if __name__ == "__main__":
    main()
