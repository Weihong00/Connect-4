"""
Random Agent - baseline pour comparaisons

Agent le plus simple: choisit aléatoirement parmi les coups valides.
Sert de baseline pour mesurer les améliorations des autres agents.

Win rate attendu: ~50% contre lui-même (légère tendance 1er joueur)
"""

import random
import numpy as np


class RandomAgent:
    """Agent aléatoire simple (baseline)"""

    def __init__(self, env, player_name=None):
        self.env = env
        self.player_name = player_name or "RandomAgent"
        # expérimental: compter les coups joués pour stats
        self.moves_count = 0

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """Choisir un coup aléatoire parmi les coups valides"""
        self.moves_count += 1

        # Obtenir le mask (plusieurs méthodes possibles)
        mask = action_mask

        # Si pas de mask fourni, essayer de l'extraire de observation
        if mask is None and isinstance(observation, dict):
            mask = observation.get("action_mask")
            board = observation.get("observation", observation)
        else:
            board = observation

        # Dernière option: calculer le mask depuis le plateau
        if mask is None:
            # Une colonne est jouable si la case du haut (row 0) est vide
            board_occupancy = board.sum(axis=2)
            mask = (board_occupancy[0, :] == 0).astype(np.int8)

        # Récupérer les colonnes valides
        legal_moves = np.nonzero(mask)[0]

        if legal_moves.size == 0:
            raise ValueError("No legal moves available for RandomAgent")

        # Choix aléatoire uniforme
        action = int(random.choice(legal_moves))

        # # DEBUG: afficher parfois le coup choisi
        # if self.moves_count % 10 == 0:
        #     print(f"RandomAgent: move {self.moves_count}, chose col {action}")

        return action

    # Version expérimentale avec biais vers le centre (pas utilisée finalement)
    # def _choose_action_with_center_bias(self, legal_moves):
    #     """Favorise légèrement les colonnes centrales"""
    #     weights = [1, 2, 3, 4, 3, 2, 1]  # plus de poids au centre
    #     move_weights = [weights[col] for col in legal_moves]
    #     return random.choices(legal_moves, weights=move_weights)[0]
