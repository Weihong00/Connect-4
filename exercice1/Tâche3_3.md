# Tâche 3.3 — Structure de la classe Agent

## Question
*Quel serait le squelette de cette classe (attributs, méthodes, etc.) ?*

---

## Squelette de base

```python
class Agent:
    """
    Classe de base pour tous les agents.
    Chaque stratégie hérite de cette classe.
    """

    def __init__(self, name="Agent"):
        """
        Initialisation de l'agent

        Args:
            name: nom de l'agent (pour l'affichage)
        """
        self.name = name

    def select_action(self, observation):
        """
        Méthode principale : choisir une action

        Args:
            observation: dict avec 'observation' et 'action_mask'

        Returns:
            int: numéro de colonne (0-6)
        """
        raise NotImplementedError("Chaque agent doit implémenter select_action()")
```

---

## Attributs importants

### Attributs de base
```python
self.name = "MonAgent"  # Nom de l'agent (pour debug/affichage)
```

### Attributs optionnels (selon le niveau)
```python
# Pour agents avancés
self.depth = 4  # Profondeur de recherche (Minimax)
self.simulations = 1000  # Nombre de simulations (MCTS)

# Pour agents avec mémoire
self.game_history = []  # Historique des coups
self.wins = 0  # Statistiques
self.losses = 0
self.draws = 0
```

---

## Méthodes essentielles

### 1. Méthode principale
```python
def select_action(self, observation):
    """
    Choisir une action basée sur l'observation
    C'est LA méthode appelée à chaque tour
    """
    pass
```

### 2. Méthodes utilitaires (helpers)

```python
def get_valid_actions(self, observation):
    """
    Extraire la liste des colonnes jouables

    Returns:
        list: indices des colonnes valides
    """
    mask = observation['action_mask']
    return [i for i in range(7) if mask[i] == 1]
```

```python
def simulate_move(self, board, col, player):
    """
    Simuler un coup sans modifier le plateau original

    Args:
        board: plateau actuel (6,7,2)
        col: colonne où jouer
        player: 0 ou 1 (quel joueur)

    Returns:
        nouveau plateau, ligne où le pion tombe
    """
    new_board = board.copy()
    # Trouver la ligne la plus basse disponible
    for row in range(5, -1, -1):
        if new_board[row, col, 0] == 0 and new_board[row, col, 1] == 0:
            new_board[row, col, player] = 1
            return new_board, row
    return new_board, None  # Colonne pleine
```

```python
def check_win(self, board, row, col, player):
    """
    Vérifier si un coup à (row, col) crée une victoire

    Args:
        board: plateau (6,7,2)
        row: ligne du coup
        col: colonne du coup
        player: joueur (0 ou 1)

    Returns:
        bool: True si victoire
    """
    # Implémenter la logique des 4 directions
    # (cf. Tâche 1.2)
    pass
```

```python
def find_winning_move(self, observation, player):
    """
    Chercher un coup gagnant pour un joueur

    Args:
        observation: observation actuelle
        player: 0 (moi) ou 1 (adversaire)

    Returns:
        int ou None: colonne gagnante ou None
    """
    board = observation['observation']
    valid_actions = self.get_valid_actions(observation)

    for col in valid_actions:
        new_board, row = self.simulate_move(board, col, player)
        if row is not None and self.check_win(new_board, row, col, player):
            return col

    return None
```

### 3. Méthodes d'évaluation (pour agents avancés)

```python
def evaluate_position(self, board, player):
    """
    Évaluer la qualité d'une position

    Returns:
        float: score (positif = bon pour player)
    """
    # Heuristiques : centre, menaces, etc.
    pass
```

---

## Exemples d'implémentation

### Agent Aléatoire (Niveau 0)

```python
class RandomAgent(Agent):
    def __init__(self):
        super().__init__(name="Random")

    def select_action(self, observation):
        valid_actions = self.get_valid_actions(observation)
        return np.random.choice(valid_actions)
```

### Agent Défensif (Niveau 3)

```python
class DefensiveAgent(Agent):
    def __init__(self):
        super().__init__(name="Defensive")

    def select_action(self, observation):
        # 1. Chercher coup gagnant
        winning_move = self.find_winning_move(observation, player=0)
        if winning_move is not None:
            return winning_move

        # 2. Bloquer adversaire
        blocking_move = self.find_winning_move(observation, player=1)
        if blocking_move is not None:
            return blocking_move

        # 3. Préférer le centre
        valid_actions = self.get_valid_actions(observation)
        if 3 in valid_actions:
            return 3

        # 4. Sinon aléatoire
        return np.random.choice(valid_actions)
```

### Agent Minimax (Niveau 5+)

```python
class MinimaxAgent(Agent):
    def __init__(self, depth=4):
        super().__init__(name=f"Minimax(depth={depth})")
        self.depth = depth

    def select_action(self, observation):
        # Lancer la recherche minimax
        best_action, best_score = self.minimax(
            observation,
            depth=self.depth,
            maximizing=True
        )
        return best_action

    def minimax(self, observation, depth, maximizing):
        """
        Algorithme minimax récursif
        """
        # ... implémentation récursive ...
        pass
```

---

## Structure de fichiers proposée

```
agents/
├── __init__.py
├── base_agent.py          # Classe Agent de base
├── random_agent.py        # Niveau 0
├── center_agent.py        # Niveau 1
├── offensive_agent.py     # Niveau 2
├── defensive_agent.py     # Niveau 3
├── strategic_agent.py     # Niveau 4
└── minimax_agent.py       # Niveau 5+
```

---

## Résumé : Ce qu'il faut retenir

### Attributs clés
- `name` : identification de l'agent
- (optionnel) paramètres de configuration (depth, simulations, etc.)

### Méthodes clés
1. **`select_action(observation)`** : méthode principale (obligatoire)
2. **`get_valid_actions(observation)`** : extraire actions valides
3. **`simulate_move(board, col, player)`** : simuler un coup
4. **`check_win(board, row, col, player)`** : vérifier victoire
5. **`find_winning_move(observation, player)`** : chercher coup gagnant

### Architecture
- Classe de base `Agent` avec méthodes communes
- Chaque stratégie hérite et implémente `select_action()`
- Réutilisation du code via héritage

---

## Prochaine étape

Implémenter la classe de base et les premiers agents (Random, Center) !
