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
    success_probabilities = [round(random.uniform(0.1, 1.0), 2) for _ in range(num_projects)]  # Random probabilities rounded to 2 decimal places
    
    # Inform the user of the success probabilities
    print("Success probabilities for each project:")
    for i, p in enumerate(success_probabilities):
        print(f"Project {i + 1}: {p}")

    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)

    # Initialize the user's valuations
    user_valuations = []
    total_valuations = 0

    for i in range(num_projects):
        while True:
            try:
                user_valuation = float(input(f"Enter your valuation for Project {i + 1}: "))
                if user_valuation < 0:
                    raise ValueError("Valuation cannot be negative.")
                
                # Calculate new total valuations
                new_total_valuations = total_valuations + user_valuation
                
                if new_total_valuations > num_projects:
                    print(f"The total valuations ({new_total_valuations}) cannot exceed the number of projects ({num_projects}). Please adjust your input.")
                else:
                    user_valuations.append(user_valuation)
                    total_valuations = new_total_valuations  # Update the total
                    break  # Exit loop if valid input is given
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a numeric value.")

    # Set uniform valuations for bots
    bot_valuation = 1.0  # Example: uniform valuation for each bot (could be adjusted as needed)

    # Update the valuation matrix
    valuation_data["players"] = []  # Reset existing players

    # Add user's valuation
    valuation_data["players"].append({
        "id": 1,  # User player ID
        "valuations": user_valuations
    })

    # Add bot players with uniform valuations
    for player_id in range(2, num_bot_players + 2):
        valuation_data["players"].append({
            "id": player_id,
            "valuations": [bot_valuation for _ in range(num_projects)]  # Uniform valuation for each bot
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
