# GateHacks

Resource Allocation Game:

Multiple players (user against AI bots) compete to allocate a fixed number of resources (e.g., tokens, items) among several distinct projects or tasks. Each player has a different valuation for each project, and they must decide how to allocate their resources to maximize their own payoff.

## Game Setup
### Players and Projects
There are n players and m distinct projects.

### Valuation Matrix V
There is a valuation matrix V where V_{ij}​ represents the value player i assigns to project j.

The rows in V must sum to m. This means the total value assigned to all projects by each player sums up to the number of projects m.

### Tokens
Each player starts with T tokens (for a total of n*T tokens in the game).
Each player must allocate a minimum of 1 token to each project in each round, and all tokens must be allocated.

### Project Success
Each project j has a distinct probability of success p_j​, where 0<p_j<1 for each project j. These probabilities can vary based on factors such as resource allocation or external conditions.

If project j succeeds, each player invested in it receives back the tokens they allocated, valued at the amount they assigned to the project.

### Game Dynamics

After each round, all projects are reset, and players allocate their tokens again based on their valuations.

The game ends after 5 rounds or when there is only one player left with tokens.