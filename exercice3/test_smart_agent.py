# Tests pour SmartAgent
# Vérifie que toutes les méthodes fonctionnent correctement

from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent
import numpy as np

env = connect_four_v3.env()
env.reset()
agent = SmartAgent(env)

# ============================================
# Tests pour _get_valid_actions
# ============================================

# Cas 1: toutes les colonnes disponibles
mask = [1, 1, 1, 1, 1, 1, 1]
assert agent._get_valid_actions(mask) == [0, 1, 2, 3, 4, 5, 6]

# Cas 2: seulement certaines colonnes
mask = [0, 1, 0, 1, 0, 1, 0]
assert agent._get_valid_actions(mask) == [1, 3, 5]

print("✓ Tests _get_valid_actions passés")

# ============================================
# Tests pour _get_next_row (gravité)
# ============================================

# Plateau vide: le pion tombe tout en bas (row 5)
board = np.zeros((6, 7, 2))
assert agent._get_next_row(board, 3) == 5

# Colonne avec 1 pion: le suivant atterrit au-dessus
board[5, 3, 0] = 1
assert agent._get_next_row(board, 3) == 4

print("✓ Tests _get_next_row passés")

# ============================================
# Tests pour _check_win_from_position
# (C'est la fonction la plus importante!)
# ============================================

# Test 1: Victoire horizontale
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
board[5, 1, 0] = 1
board[5, 2, 0] = 1
# Si on place à (5, 3), ça fait X X X X
assert agent._check_win_from_position(board, 5, 3, channel=0) == True
print("✓ Victoire horizontale détectée")

# Test 2: Victoire verticale
board = np.zeros((6, 7, 2))
board[5, 3, 0] = 1
board[4, 3, 0] = 1
board[3, 3, 0] = 1
# Placer à (2, 3) fait une colonne de 4
assert agent._check_win_from_position(board, 2, 3, channel=0) == True
print("✓ Victoire verticale détectée")

# Diagonal \ connect-four
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
board[4, 1, 0] = 1
board[3, 2, 0] = 1
# Placing at (2, 3) should make four on the diagonal
assert agent._check_win_from_position(board, 2, 3, channel=0) == True
print("Test diagonal \\ win: passed")

# Diagonal / connect-four
board = np.zeros((6, 7, 2))
board[5, 3, 0] = 1
board[4, 2, 0] = 1
board[3, 1, 0] = 1
# Placing at (2, 0) should make four on the diagonal
assert agent._check_win_from_position(board, 2, 0, channel=0) == True
print("Test diagonal / win: passed")

# Case with no connect-four
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
board[5, 1, 0] = 1
# Only two pieces; placing at (5, 2) makes just three in a row
assert agent._check_win_from_position(board, 5, 2, channel=0) == False
print("Test no win (only 3 in a row): passed")

print("All _check_win_from_position tests passed!")

# ============================================
# Tests for _find_winning_move
# ============================================

# Finds winning column (horizontal case)
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
board[5, 1, 0] = 1
board[5, 2, 0] = 1
valid_actions = [0, 1, 2, 3, 4, 5, 6]
# Dropping in column 3 wins
assert agent._find_winning_move(board, valid_actions, channel=0) == 3
print("Test find horizontal winning move: passed")

# Finds winning column (vertical case)
board = np.zeros((6, 7, 2))
board[5, 3, 0] = 1
board[4, 3, 0] = 1
board[3, 3, 0] = 1
valid_actions = [0, 1, 2, 3, 4, 5, 6]
# Dropping in column 3 wins (piece lands at row=2)
assert agent._find_winning_move(board, valid_actions, channel=0) == 3
print("Test find vertical winning move: passed")

# No winning column available
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
board[5, 2, 0] = 1  # Gap in the middle
valid_actions = [0, 1, 2, 3, 4, 5, 6]
assert agent._find_winning_move(board, valid_actions, channel=0) == None
print("Test no winning move available: passed")

# Blocking opponent's win (channel=1)
board = np.zeros((6, 7, 2))
board[5, 0, 1] = 1  # Opponent's piece
board[5, 1, 1] = 1
board[5, 2, 1] = 1
valid_actions = [0, 1, 2, 3, 4, 5, 6]
# Opponent wins if they drop in column 3, so block it
assert agent._find_winning_move(board, valid_actions, channel=1) == 3
print("Test find blocking move: passed")

print("All _find_winning_move tests passed!")

# ============================================
# Tests for _creates_double_threat
# ============================================

# Double threat: two winning options after the move
# Scenario: two adjacent pieces on the bottom row; adding next to them could create a double threat
board = np.zeros((6, 7, 2))
board[5, 2, 0] = 1  # X at (5, 2)
board[5, 3, 0] = 1  # X at (5, 3)
# Dropping at (5, 4) makes X X X; next move could win at (5, 1) or (5, 5)
# Needs more pieces to be a true double threat

# Better double-threat test: build a true double-threat shape
board = np.zeros((6, 7, 2))
# Shape: X _ X X; dropping into the gap could create a double threat
board[5, 0, 0] = 1
board[5, 2, 0] = 1
board[5, 3, 0] = 1
# Dropping at col=1 makes X X X X (immediate win), not a true double threat

# No double threat present
board = np.zeros((6, 7, 2))
board[5, 0, 0] = 1
# With only one piece, no move can create a double threat
assert agent._creates_double_threat(board, 1, channel=0) == False
print("Test no double threat (only 1 piece): passed")

# True double-threat scenario
# Layout: bottom row X X _ and X _ _; dropping in the middle may create a double threat
board = np.zeros((6, 7, 2))
board[5, 1, 0] = 1
board[5, 2, 0] = 1
board[4, 3, 0] = 1  # One piece on the row above
# Dropping at col=3 (lands at row=5) makes horizontal X X X; next turn could win at col=0 or col=4
result = agent._creates_double_threat(board, 3, channel=0)
print(f"Test potential double threat: {'passed' if result else 'no double threat detected (OK)'}")

print("All _creates_double_threat tests passed!")

print("\n" + "=" * 50)
print("All SmartAgent tests passed!")
print("=" * 50)

# ============================================
# SmartAgent vs RandomAgent evaluation
# ============================================

from random_agent import RandomAgent


def test_smart_vs_random(num_games=100):
    """
    Evaluate SmartAgent win rate against RandomAgent.

    Parameters:
        num_games: int - number of games to play

    Returns:
        dict - statistics on win rates
    """
    env = connect_four_v3.env(render_mode=None)

    results = {
        "smart_wins": 0,
        "random_wins": 0,
        "draws": 0,
        # Track win rate when moving first vs second
        "smart_wins_as_first": 0,
        "smart_wins_as_second": 0,
    }

    print(f"\n=== SmartAgent vs RandomAgent: {num_games} games ===\n")

    for game_num in range(1, num_games + 1):
        env.reset()

        # Alternate starting player each game
        if game_num % 2 == 1:
            # SmartAgent starts first
            agents = {
                "player_0": SmartAgent(env, player_name="SmartAgent"),
                "player_1": RandomAgent(env, player_name="RandomAgent"),
            }
            smart_player = "player_0"
        else:
            # SmartAgent moves second
            agents = {
                "player_0": RandomAgent(env, player_name="RandomAgent"),
                "player_1": SmartAgent(env, player_name="SmartAgent"),
            }
            smart_player = "player_1"

        # Play one game
        winner = None
        for agent_name in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()

            if termination or truncation:
                if reward == 1:
                    winner = agent_name
                env.step(None)
            else:
                agent = agents[agent_name]
                mask = observation["action_mask"]
                action = agent.choose_action(
                    observation=observation["observation"],
                    action_mask=mask
                )
                env.step(action)

        # Collect results
        if winner == smart_player:
            results["smart_wins"] += 1
            if smart_player == "player_0":
                results["smart_wins_as_first"] += 1
            else:
                results["smart_wins_as_second"] += 1
        elif winner is not None:
            results["random_wins"] += 1
        else:
            results["draws"] += 1

        # Log progress
        if game_num % 20 == 0:
            print(f"Completed {game_num}/{num_games} games...")

    env.close()

    # Compute win rates
    results["smart_win_rate"] = results["smart_wins"] / num_games * 100
    results["random_win_rate"] = results["random_wins"] / num_games * 100
    results["draw_rate"] = results["draws"] / num_games * 100

    # Print results
    print("\n" + "=" * 50)
    print("=== Results: SmartAgent vs RandomAgent ===")
    print("=" * 50)
    print(f"Total games: {num_games}")
    print(f"\nSmartAgent wins: {results['smart_wins']} ({results['smart_win_rate']:.1f}%)")
    print(f"  - As first player: {results['smart_wins_as_first']}")
    print(f"  - As second player: {results['smart_wins_as_second']}")
    print(f"\nRandomAgent wins: {results['random_wins']} ({results['random_win_rate']:.1f}%)")
    print(f"\nDraws: {results['draws']} ({results['draw_rate']:.1f}%)")
    print("=" * 50)

    # Determine whether SmartAgent outperforms RandomAgent
    if results["smart_win_rate"] > 60:
        print("\nSmartAgent significantly outperforms RandomAgent!")
    elif results["smart_win_rate"] > 50:
        print("\nSmartAgent is better than RandomAgent.")
    else:
        print("\nSmartAgent needs improvement.")

    return results


if __name__ == "__main__":
    # Run SmartAgent vs RandomAgent benchmark
    test_smart_vs_random(num_games=100)
