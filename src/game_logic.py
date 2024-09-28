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

        # Ensure total allocation equals the number of players and each project has at least 1 token
        if total_allocated != self.num_players or total_allocated < min_allocation:
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

        # Prompt user until valid allocations are made
        while True:
            human_allocations = self.get_human_allocations()
            if self.allocate_tokens(human_player_id, human_allocations):
                break  # Exit loop if the allocation was successful
            else:
                print(f"Invalid allocations by Player {human_player_id}. Please try again.")

        # Allocate tokens for bot players
        for player_id in range(2, self.num_players + 1):
            bot_allocations = self.get_bot_allocations(player_id)
            self.allocate_tokens(player_id, bot_allocations)

        # Evaluate projects based on all allocations
        self.evaluate_projects()
        self.current_round += 1
        self.reset_projects()


    def run_game(self):
        max_rounds = 5
        round_count = 0
        
        while round_count < max_rounds:
            self.play_round()
            round_count += 1
            
            # Check if there is only one player left with tokens
            if self.check_single_player_left():
                print("Game over! Only one player left with tokens.")
                break

        # If max rounds reached without a single player left
        if round_count == max_rounds:
            print("Game over! Maximum rounds reached.")


    def check_single_player_left(self):
        active_players = 0
        for player in self.valuation_data['players']:
            if 'allocations' in player and sum(player['allocations']) > 0:
                active_players += 1

        return active_players <= 1  # Return True if only one or no active players left

    def get_human_allocations(self):
        allocations = []
        for j in range(len(self.success_probabilities)):
            while True:
                try:
                    allocation = int(input(f"Allocate tokens to Project {j + 1} (1 token minimum): "))
                    if allocation < 1:
                        print("You must allocate at least 1 token to each project.")
                    else:
                        allocations.append(allocation)
                        break
                except ValueError:
                    print("Invalid input. Please enter a numeric value.")
        
        return allocations

    
    def get_bot_allocations(self, player_id):
        num_projects = len(self.success_probabilities)
        total_tokens = self.num_players  # Total tokens to allocate is equal to the number of players

        # Normalize success probabilities to sum to 1
        normalized_probabilities = [p / sum(self.success_probabilities) for p in self.success_probabilities]

        # Allocate tokens based on normalized probabilities
        allocations = [int(total_tokens * prob) for prob in normalized_probabilities]

        # Adjust the allocations to ensure the total equals the number of tokens
        while sum(allocations) < total_tokens:
            # Randomly increment allocation for one of the projects until it matches total_tokens
            allocations[random.randint(0, num_projects - 1)] += 1

        while sum(allocations) > total_tokens:
            # Randomly decrement allocation for one of the projects until it matches total_tokens
            project_to_decrement = random.randint(0, num_projects - 1)
            if allocations[project_to_decrement] > 0:
                allocations[project_to_decrement] -= 1
        
        return allocations
