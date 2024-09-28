import json
import random
import sys
from game_logic import Game
from ui import UserInterface
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    # Load initial data
    with open('data/valuation_matrix.json', 'r') as file:
        valuation_data = json.load(file)

    # Initialize the game
    success_probabilities = [round(random.uniform(0.1, 1.0), 2) for _ in range(3)]
    game = Game(valuation_data, success_probabilities, 3)

    # Initialize the UI
    ui = UserInterface(game)
    ui.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
