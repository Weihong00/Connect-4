"""
Smart Agent pour Puissance 4

Agent basé sur des règles heuristiques. J'ai d'abord essayé avec juste
la détection de victoire/blocage mais c'était pas assez, donc j'ai ajouté
la détection de double menace après.
"""

import random


class SmartAgent:
    """
    Agent basé sur des règles stratégiques

    Stratégie progressive que j'ai développée:
    1. D'abord juste random (trop faible)
    2. Puis ajout win detection (mieux mais pas assez)
    3. Puis block opponent (amélioration significative)
    4. Finalement double threat detection (le plus important!)
    """

    def __init__(self, env, player_name=None):
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgent"
        # TODO: peut-être ajouter un compteur de coups pour stats?

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """Choisir une action selon la stratégie par règles"""
        # Gérer les deux formats d'observation
        if isinstance(observation, dict):
            # Format PettingZoo: {'observation': array, 'action_mask': array}
            board = observation['observation']
            if action_mask is None:
                action_mask = observation['action_mask']
        else:
            # Format direct: numpy array
            board = observation

        # Récupérer les coups valides
        valid_actions = self._get_valid_actions(action_mask)

        # Règle 1: Gagner si possible (priorité absolue!)
        winning_move = self._find_winning_move(board, valid_actions, channel=0)
        if winning_move is not None:
            return winning_move

        # Règle 2: Bloquer l'adversaire s'il peut gagner
        # Bug fix: j'avais oublié ça au début et l'agent perdait bêtement
        blocking_move = self._find_winning_move(board, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move

        # Règle 3: Créer une double menace (=victoire garantie)
        # Cette partie m'a pris du temps à débugger
        for col in valid_actions:
            if self._creates_double_threat(board, col, channel=0):
                return col

        # Règle 4: Bloquer la double menace adverse
        for col in valid_actions:
            if self._creates_double_threat(board, col, channel=1):
                return col

        # Règle 5: Préférer le centre (statistiquement meilleur)
        # colonnes centrales = plus de possibilités d'alignement
        center_preference = [3, 2, 4, 1, 5, 0, 6]
        for col in center_preference:
            if col in valid_actions:
                return col

        # Fallback: choix aléatoire (normalement on arrive rarement ici)
        action = random.choice(valid_actions)
        return action

    def _get_valid_actions(self, action_mask):
        """Retourne les colonnes jouables"""
        return [col for col in range(len(action_mask)) if action_mask[col] == 1]

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Trouve un coup qui crée un alignement de 4
        channel=0 pour nous, channel=1 pour adversaire
        """
        for col in valid_actions:
            row = self._get_next_row(observation, col)
            if row is None:
                continue  # colonne pleine

            # simuler le coup
            board_copy = observation.copy()
            board_copy[row, col, channel] = 1

            if self._check_win_from_position(board_copy, row, col, channel):
                return col

        return None

    def _get_next_row(self, board, col):
        """Trouve la ligne où le pion va atterrir (gravité)"""
        # chercher de bas en haut
        for row in range(5, -1, -1):
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row
        return None  # colonne pleine

    def _check_win_from_position(self, board, row, col, channel):
        """
        Vérifie si placer un pion à (row,col) fait un alignement de 4

        L'algorithme: pour chaque direction, on compte dans les deux sens
        (positif et négatif) combien de pions consécutifs on a
        """
        # 4 directions à vérifier: horizontal, vertical, 2 diagonales
        directions = [
            (0, 1),   # horizontal
            (1, 0),   # vertical
            (-1, 1),  # diag /
            (1, 1),   # diag \
        ]

        for dr, dc in directions:
            count = 1  # le pion qu'on vient de placer

            # compter dans le sens positif
            r, c = row + dr, col + dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc

            # compter dans le sens négatif
            r, c = row - dr, col - dc
            while 0 <= r < 6 and 0 <= c < 7 and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc

            if count >= 4:
                return True

        return False

    def _creates_double_threat(self, board, col, channel):
        """
        Détecte si un coup crée une double menace

        Double menace = après ce coup, on a 2+ façons de gagner au prochain tour
        L'adversaire peut bloquer qu'une seule => victoire assurée!

        C'est la partie la plus importante de la stratégie selon mes tests.
        """
        row = self._get_next_row(board, col)
        if row is None:
            return False

        # simuler le coup
        board_copy = board.copy()
        board_copy[row, col, channel] = 1

        # compter combien de coups gagnants on aurait au tour suivant
        winning_moves = 0
        for next_col in range(7):
            next_row = self._get_next_row(board_copy, next_col)
            if next_row is None:
                continue

            # tester ce coup
            board_copy2 = board_copy.copy()
            board_copy2[next_row, next_col, channel] = 1

            if self._check_win_from_position(board_copy2, next_row, next_col, channel):
                winning_moves += 1

            # dès qu'on a trouvé 2 coups gagnants, c'est bon
            if winning_moves >= 2:
                return True

        return False
