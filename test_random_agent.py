"""
Test script for RandomAgent - Two random agents play Connect Four
"""

from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent


def print_board(observation):
    """Print the current board state"""
    board = observation["observation"]
    print("\n  0 1 2 3 4 5 6")
    print("  -------------")
    for row in range(6):
        print(f"| ", end="")
        for col in range(7):
            if board[row, col, 0] == 1:
                print("X ", end="")  # Player 0
            elif board[row, col, 1] == 1:
                print("O ", end="")  # Player 1
            else:
                print(". ", end="")
        print("|")
    print("  -------------\n")


def play_single_game(env, agents, verbose=True):
    """
    Play a single game between two agents.

    Parameters:
        env: PettingZoo environment
        agents: dict mapping agent names to agent instances
        verbose: if True, print each move and board state

    Returns:
        tuple: (winner, num_moves)
            winner: "player_0", "player_1", or "draw"
            num_moves: int - total number of moves in the game
    """
    env.reset()
    winner = "draw"
    num_moves = 0

    for agent_name in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            action = None
            if reward == 1:
                winner = agent_name
                if verbose:
                    print(f"\n{agents[agent_name].player_name} ({agent_name}) wins!")
        else:
            # Get action from agent
            agent = agents[agent_name]
            mask = observation["action_mask"]
            action = agent.choose_action(
                observation=observation["observation"],
                action_mask=mask
            )
            num_moves += 1
            if verbose:
                print(f"{agent.player_name} ({agent_name}) plays column {action}")
                print_board(observation)

        env.step(action)

    return winner, num_moves


def play_multiple_games(num_games, verbose=False):
    """
    Play multiple games between two RandomAgents and return statistics.

    Parameters:
        num_games: int - number of games to play
        verbose: if True, print details of each game

    Returns:
        dict with results: wins for each player, draws, win rates, and game length stats
    """
    # Create environment (no rendering for faster execution)
    env = connect_four_v3.env(render_mode=None)

    # Create two RandomAgent instances
    agents = {
        "player_0": RandomAgent(env, player_name="RandomAgent_1"),
        "player_1": RandomAgent(env, player_name="RandomAgent_2"),
    }

    # Track results
    results = {
        "player_0_wins": 0,
        "player_1_wins": 0,
        "draws": 0
    }

    # Track game lengths
    game_lengths = []

    print(f"=== Playing {num_games} games: RandomAgent vs RandomAgent ===\n")

    for game_num in range(1, num_games + 1):
        if verbose:
            print(f"\n--- Game {game_num} ---")

        winner, num_moves = play_single_game(env, agents, verbose=verbose)
        game_lengths.append(num_moves)

        if winner == "player_0":
            results["player_0_wins"] += 1
        elif winner == "player_1":
            results["player_1_wins"] += 1
        else:
            results["draws"] += 1

        # Print progress every 100 games (if not verbose)
        if not verbose and game_num % 100 == 0:
            print(f"Completed {game_num}/{num_games} games...")

    env.close()

    # Calculate win rates
    results["player_0_win_rate"] = results["player_0_wins"] / num_games * 100
    results["player_1_win_rate"] = results["player_1_wins"] / num_games * 100
    results["draw_rate"] = results["draws"] / num_games * 100

    # Calculate game length statistics
    results["game_lengths"] = game_lengths
    results["avg_moves"] = sum(game_lengths) / len(game_lengths)
    results["min_moves"] = min(game_lengths)
    results["max_moves"] = max(game_lengths)

    # Print summary
    print("\n" + "=" * 50)
    print("=== Final Results ===")
    print("=" * 50)
    print(f"Total games played: {num_games}")
    print(f"\n{agents['player_0'].player_name} (player_0 - First player):")
    print(f"  Wins: {results['player_0_wins']} ({results['player_0_win_rate']:.2f}%)")
    print(f"\n{agents['player_1'].player_name} (player_1 - Second player):")
    print(f"  Wins: {results['player_1_wins']} ({results['player_1_win_rate']:.2f}%)")
    print(f"\nDraws: {results['draws']} ({results['draw_rate']:.2f}%)")
    print(f"\n--- Game Length Statistics ---")
    print(f"  Average moves per game: {results['avg_moves']:.2f}")
    print(f"  Minimum moves: {results['min_moves']}")
    print(f"  Maximum moves: {results['max_moves']}")
    print("=" * 50)

    return results


def main():
    """Play a single game with visual output"""
    env = connect_four_v3.env(render_mode="human")
    env.reset(seed=42)

    agents = {
        "player_0": RandomAgent(env, player_name="RandomAgent_1"),
        "player_1": RandomAgent(env, player_name="RandomAgent_2"),
    }

    print("=== Connect Four: RandomAgent vs RandomAgent ===\n")

    winner, num_moves = play_single_game(env, agents, verbose=True)

    env.close()
    print("\n=== Game Over ===")
    print(f"Total moves: {num_moves}")

    if winner == "draw":
        print("Result: Draw!")
    else:
        print(f"Result: {agents[winner].player_name} wins!")


if __name__ == "__main__":
    # Play a single game with visualization
    # main()

    # Play multiple games and get statistics
    results = play_multiple_games(num_games=100, verbose=False)
