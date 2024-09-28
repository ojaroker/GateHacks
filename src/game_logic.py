import random

class Game:
    def __init__(self, valuation_data, success_probabilities, num_players):
        self.valuation_data = valuation_data
        self.success_probabilities = success_probabilities
        self.num_players = num_players
        self.current_round = 0
        self.project_status = [False] * len(success_probabilities)
        self.initialize_game()

    def initialize_game(self):
        print("Initializing game...")
        self.player_scores = [0] * self.num_players
        self.reset_projects()

    def reset_projects(self):
        self.project_status = [False] * len(self.success_probabilities)

    def allocate_tokens(self, player_id, allocations):
        total_allocated = sum(allocations)
        min_allocation = len(allocations)  # Each project must receive at least 1 token

        if total_allocated != sum(allocations) or total_allocated < min_allocation:
            print(f"Invalid allocation by Player {player_id}. Must allocate exactly {self.num_players} tokens, with at least 1 to each project.")
            return False  # Invalid allocation

        # Store the allocations for this player
        self.valuation_data['players'][player_id - 1]['allocations'] = allocations
        print(f"Player {player_id} allocated tokens: {allocations}")
        return True  # Successful allocation

    def evaluate_projects(self):
        for j in range(len(self.success_probabilities)):
            if random.random() < self.success_probabilities[j]:
                self.project_status[j] = True
                print(f"Project {j + 1} succeeded!")
                
                for player_id, player in enumerate(self.valuation_data['players']):
                    if 'allocations' in player and player['allocations'][j] > 0:
                        score = player['valuations'][j] * player['allocations'][j]
                        self.player_scores[player_id] += score
                        print(f"Player {player_id + 1} scored {score} points from Project {j + 1}.")

    def play_round(self):
        print(f"--- Round {self.current_round + 1} ---")
        human_player_id = 1
        human_allocations = self.get_human_allocations()
        self.allocate_tokens(human_player_id, human_allocations)

        for player_id in range(2, self.num_players + 1):
            bot_allocations = self.get_bot_allocations(player_id)
            self.allocate_tokens(player_id, bot_allocations)

        self.evaluate_projects()
        self.current_round += 1
        self.reset_projects()

    def run_game(self):
        while True:
            self.play_round()
            if self.current_round >= 5:  # Example: end after 5 rounds
                break

        print("Final Scores:")
        for player_id, score in enumerate(self.player_scores):
            print(f"Player {player_id + 1}: {score} points")

    def get_human_allocations(self):
        allocations = []
        for j in range(len(self.success_probabilities)):
            while True:
                try:
                    allocation = int(input(f"Allocate tokens to Project {j + 1} (1 token minimum): "))
                    if allocation < 1:
                        print("You must allocate at least 1 token to each project.")
                    allocations.append(allocation)
                    break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        
        return allocations

    def get_bot_allocations(self, player_id):
        num_projects = len(self.success_probabilities)
        uniform_allocation = 1  # Example: allocate 1 token to each project for simplicity
        return [uniform_allocation] * num_projects
