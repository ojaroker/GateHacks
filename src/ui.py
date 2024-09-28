class UserInterface:
    def __init__(self, game):
        """
        Initialize the user interface with the game instance.

        Parameters:
        - game (Game): The Game instance to interact with.
        """
        self.game = game

    def start(self):
        """
        Start the game loop by calling the run_game method from the Game class.
        """
        print("Welcome to the Resource Allocation Game!")
        self.game.run_game()
        self.display_final_scores()

    def display_final_scores(self):
        """
        Display the final scores of all players after the game ends.
        """
        print("Final Scores:")
        for player_id, score in enumerate(self.game.player_scores):
            print(f"Player {player_id + 1}: {score} points")
