import random

class Game:
    def __init__(self, valuation_data, success_probabilities, num_players):
        self.valuation_data = valuation_data
        self.success_probabilities = success_probabilities
        self.num_players = num_players
        self.current_round = 0
        self.project_status = [False] * len(success_probabilities)
        self.player_scores = [0] * self.num_players
        self.reset_projects()

    def reset_projects(self):
        self.project_status = [False] * len(self.success_probabilities)

    def allocate_tokens(self, player_id, allocations):
        total_allocated = sum(allocations)
        min_allocation = len(allocations)  # Each project must receive at least 1 token

        if total_allocated != self.num_players or total_allocated < min_allocation:
            return False  # Invalid allocation

        self.valuation_data['players'][player_id - 1]['allocations'] = allocations
        return True  # Successful allocation

    def evaluate_projects(self):
        scores = []
        for j in range(len(self.success_probabilities)):
            if random.random() < self.success_probabilities[j]:
                self.project_status[j] = True
                for player_id, player in enumerate(self.valuation_data['players']):
                    if 'allocations' in player and player['allocations'][j] > 0:
                        score = player['valuations'][j] * player['allocations'][j]
                        self.player_scores[player_id] += score
                        scores.append((player_id + 1, score, j + 1))  # Store scores for the UI
        return scores

    def play_round(self, human_allocations):
        human_player_id = 1

        if self.allocate_tokens(human_player_id, human_allocations):
            bot_scores = []
            for player_id in range(2, self.num_players + 1):
                bot_allocations = self.get_bot_allocations(player_id)
                self.allocate_tokens(player_id, bot_allocations)

            scores = self.evaluate_projects()
            self.current_round += 1
            self.reset_projects()
            return scores  # Return scores to update UI

        return None  # Indicate invalid allocation

    def check_single_player_left(self):
        active_players = 0
        for player in self.valuation_data['players']:
            if 'allocations' in player and sum(player['allocations']) > 0:
                active_players += 1
        return active_players <= 1

    def get_bot_allocations(self, player_id):
        num_projects = len(self.success_probabilities)
        total_tokens = self.num_players

        normalized_probabilities = [p / sum(self.success_probabilities) for p in self.success_probabilities]
        allocations = [int(total_tokens * prob) for prob in normalized_probabilities]

        while sum(allocations) < total_tokens:
            allocations[random.randint(0, num_projects - 1)] += 1

        while sum(allocations) > total_tokens:
            project_to_decrement = random.randint(0, num_projects - 1)
            if allocations[project_to_decrement] > 0:
                allocations[project_to_decrement] -= 1

        return allocations
