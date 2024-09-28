from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit
import random

class UserInterface(QWidget):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()
        self.state = 'get_num_bots'  # State to track the game setup flow
        self.num_bots = 0
        self.num_projects = 0
        self.success_probabilities = []
        self.user_valuations = []
        self.current_project_index = 0

    def init_ui(self):
        self.setWindowTitle("Resource Allocation Game")
        self.layout = QVBoxLayout()

        # Game status label
        self.status_label = QLabel("Welcome to the Resource Allocation Game!")
        self.layout.addWidget(self.status_label)

        # Game chat box to show instructions and results
        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        self.layout.addWidget(self.chat_box)

        # Input box for user input
        self.input_box = QLineEdit()
        self.input_box.returnPressed.connect(self.handle_input)
        self.layout.addWidget(self.input_box)

        # Play button for next round (initially disabled)
        self.play_button = QPushButton("Play Round")
        self.play_button.setEnabled(False)
        self.play_button.clicked.connect(self.play_round)
        self.layout.addWidget(self.play_button)

        self.setLayout(self.layout)
        self.chat_log = []

        # Initial message asking for number of bot players
        self.display_message("Welcome! How many bots do you want to play against?")

    def handle_input(self):
        user_input = self.input_box.text()
        self.input_box.clear()

        # Display the user's input in the chat
        self.display_message(f"User: {user_input}")

        if self.state == 'get_num_bots':
            self.get_num_bots(user_input)
        elif self.state == 'show_projects_and_probs':
            self.show_projects_and_probs()
        elif self.state == 'get_valuations':
            self.get_user_valuations(user_input)
        elif self.state == 'get_allocations':
            self.get_user_allocations(user_input)

    def get_num_bots(self, user_input):
        """
        Handle the input for the number of bot players.
        """
        try:
            self.num_bots = int(user_input)
            if self.num_bots < 0:
                raise ValueError("Number of bots must be a non-negative integer.")
        except ValueError:
            self.display_message("Invalid input! Please enter a non-negative integer.")
            return

        # Randomly select number of projects and generate success probabilities
        self.num_projects = random.randint(1, self.num_bots + 1)
        self.success_probabilities = [round(random.uniform(0.1, 1.0), 2) for _ in range(self.num_projects)]

        # Move to next step of the setup
        self.state = 'show_projects_and_probs'
        self.display_message(f"Randomly selected {self.num_projects} projects.")
        self.show_projects_and_probs()

    def show_projects_and_probs(self):
        """
        Show the number of projects and their probabilities.
        """
        self.display_message("Here are the projects and their success probabilities:")
        for i, prob in enumerate(self.success_probabilities):
            self.display_message(f"Project {i + 1}: {prob} probability of success")

        # Prompt for user valuations
        self.state = 'get_valuations'
        self.current_project_index = 0
        self.display_message(f"Enter your valuation for Project 1:")

    def get_user_valuations(self, user_input):
        """
        Handle the input for user valuations for each project.
        """
        try:
            user_valuation = float(user_input)
            if user_valuation < 0:
                raise ValueError("Valuation cannot be negative.")
        except ValueError:
            self.display_message("Invalid input! Please enter a non-negative number.")
            return

        self.user_valuations.append(user_valuation)
        self.current_project_index += 1

        # If we still have more projects to value, ask for the next one
        if self.current_project_index < self.num_projects:
            self.display_message(f"Enter your valuation for Project {self.current_project_index + 1}:")
        else:
            # When all valuations are entered, initialize the game with this data
            self.initialize_game()

    def initialize_game(self):
        """
        Initialize the game with the collected data and proceed to play rounds.
        """
        # Set uniform valuations for bot players
        bot_valuation = 1.0

        # Update the valuation matrix in the game
        self.game.valuation_data["players"] = [{"id": 1, "valuations": self.user_valuations}]
        for player_id in range(2, self.num_bots + 2):
            self.game.valuation_data["players"].append({
                "id": player_id,
                "valuations": [bot_valuation for _ in range(self.num_projects)]
            })

        # Set the success probabilities in the game
        self.game.success_probabilities = self.success_probabilities

        self.display_message("Game initialized! Press 'Play Round' to start.")
        self.play_button.setEnabled(True)

    def play_round(self):
        self.play_button.setEnabled(False)
        self.display_message(f"--- Round {self.game.current_round + 1} ---")

        # Ask for user allocations
        self.state = 'get_allocations'
        self.display_message("Please allocate tokens (enter in format: '1, 1, 1'):")

    def get_user_allocations(self, user_input):
        """
        Handle the input for user allocations.
        """
        try:
            # Split the user input by commas and convert to integers
            allocations = [int(x.strip()) for x in user_input.split(",")]
            
            # Validate the number of allocations
            if len(allocations) != self.num_projects:
                raise ValueError(f"You must allocate tokens for all {self.num_projects} projects.")
            
            # Validate that each project receives at least 1 token
            if any(a < 1 for a in allocations):
                raise ValueError("Each project must receive at least 1 token.")

            # Pass allocations to the game
            scores = self.game.play_round(allocations)
            
            if scores is not None:
                # Format the scores for better readability
                score_output = "\n".join(f"Player {player_id}: {score} points" for player_id, score, _ in scores)
                self.display_message(f"Round {self.game.current_round} completed. Scores:\n{score_output}")
            else:
                self.display_message("Round was not completed due to invalid allocation.")

            self.play_button.setEnabled(True)

        except ValueError as e:
            self.display_message(f"Invalid input! {e}")


    def display_message(self, message):
        """
        Append the message to the chat log and update the chat box.
        """
        self.chat_log.append(message)
        self.chat_box.setText("\n".join(self.chat_log))
