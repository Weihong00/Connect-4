from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
    """
    Print a human-readable version of the board

    observation: numpy array of shape (6, 7, 2)
        observation[:,:,0] = current player's pieces
        observation[:,:,1] = opponent's pieces
    """
    # Afficher les numéros de colonnes
    print("  0 1 2 3 4 5 6")
    print(" " + "-" * 15)

    # Parcourir chaque ligne
    for row in range(6):
        print("|", end=" ")
        # Parcourir chaque colonne
        for col in range(7):
            if observation[row, col, 0] == 1:
                print("X", end=" ")  # Mon pion
            elif observation[row, col, 1] == 1:
                print("O", end=" ")  # Pion adverse
            else:
                print(".", end=" ")  # Case vide
        print("|")

    print(" " + "-" * 15)

# Test de la fonction
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Faire quelques coups pour voir le plateau changer
    print("\nJe joue colonne 3")
    env.step(3)

    # Afficher le plateau après le coup
    observation, reward, termination, truncation, info = env.last()
    print("\nPlateau après le coup:")
    print_board(observation['observation'])

    if agent == env.agents[0]:
        break

env.close()
