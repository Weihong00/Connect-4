"""
Play Connect Four vs SmartAgent
================================

Interactive game where you play against the SmartAgent.
"""

from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent
from loguru import logger

# Disable agent logging for cleaner game output
logger.disable("agents.smart_agent")


def print_board(observation):
    """Print the board in a nice format"""
    print("\n  0   1   2   3   4   5   6")
    print("+" + "---+" * 7)

    for row in range(6):
        print("|", end="")
        for col in range(7):
            if observation[row, col, 0] == 1:
                piece = " X "  # Player 0 (you if first)
            elif observation[row, col, 1] == 1:
                piece = " O "  # Player 1 (SmartAgent if first)
            else:
                piece = "   "
            print(f"{piece}|", end="")
        print()
        print("+" + "---+" * 7)


def play_game(human_first=True):
    """
    Play a game against SmartAgent

    Parameters:
        human_first: bool - If True, you play first (X), else SmartAgent plays first
    """
    env = connect_four_v3.env(render_mode=None)
    env.reset()

    smart_agent = SmartAgent(env, player_name="SmartAgent")

    if human_first:
        human_player = "player_0"
        ai_player = "player_1"
        human_symbol = "X"
        ai_symbol = "O"
        print("\nYou are X (first player)")
    else:
        human_player = "player_1"
        ai_player = "player_0"
        human_symbol = "O"
        ai_symbol = "X"
        print("\nYou are O (second player)")

    print("SmartAgent is", ai_symbol)
    print("\nEnter column number (0-6) to play, or 'q' to quit\n")

    game_over = False
    winner = None

    for current_player in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()

        if termination or truncation:
            if reward == 1:
                winner = current_player
            game_over = True
            env.step(None)
            continue

        if game_over:
            continue

        # Get board and valid moves
        board = observation["observation"]
        action_mask = observation["action_mask"]
        valid_moves = [i for i in range(7) if action_mask[i] == 1]

        print_board(board)

        if current_player == human_player:
            # Human's turn
            print(f"\nYour turn ({human_symbol})")
            print(f"Valid columns: {valid_moves}")

            while True:
                try:
                    user_input = input("Enter column (0-6): ").strip()

                    if user_input.lower() == 'q':
                        print("\nGame quit.")
                        env.close()
                        return

                    action = int(user_input)

                    if action not in valid_moves:
                        print(f"Invalid move! Choose from: {valid_moves}")
                        continue

                    break
                except ValueError:
                    print("Please enter a number (0-6) or 'q' to quit")
        else:
            # SmartAgent's turn
            print(f"\nSmartAgent's turn ({ai_symbol})...")
            action = smart_agent.choose_action(board, action_mask=action_mask)
            print(f"SmartAgent plays column: {action}")

        env.step(action)

    # Game over - show final board
    final_obs = env.observe(human_player)
    print_board(final_obs["observation"])

    # Announce result
    print("\n" + "=" * 30)
    if winner == human_player:
        print("   YOU WIN!")
    elif winner == ai_player:
        print("   SmartAgent WINS!")
    else:
        print("   DRAW!")
    print("=" * 30)

    env.close()


def main():
    print("\n" + "=" * 40)
    print("   CONNECT FOUR vs SmartAgent")
    print("=" * 40)

    while True:
        print("\nOptions:")
        print("1. Play first (you are X)")
        print("2. Play second (you are O)")
        print("q. Quit")

        choice = input("\nChoice: ").strip().lower()

        if choice == '1':
            play_game(human_first=True)
        elif choice == '2':
            play_game(human_first=False)
        elif choice == 'q':
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or q")

        # Ask to play again
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != 'y':
            print("\nThanks for playing!")
            break


if __name__ == "__main__":
    main()
