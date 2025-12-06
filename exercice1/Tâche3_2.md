# Tâche 3.2 — Plan de progression des agents (du simple au complexe)

## Décomposition du problème avec progression d'agent

### Niveau 0 : **Agent Aléatoire**
*Le plus simple possible*

**Stratégie** : Choisir une colonne au hasard parmi les colonnes valides.

**Implémentation** :
```python
def random_agent(observation):
    mask = observation['action_mask']
    valid_actions = np.where(mask == 1)[0]
    return np.random.choice(valid_actions)
```

**Avantages** :
- Très simple à coder
- Toujours joue un coup valide (grâce à l'action_mask)
- Bon pour tester l'environnement

**Limites** :
- Aucune stratégie
- Ne cherche pas à gagner ni à bloquer

---

### Niveau 1 : **Agent Centre**
*Légèrement plus intelligent - préférence pour le centre*

**Stratégie** : Préférer jouer au centre (colonnes 3, 2, 4) car ça offre plus de possibilités d'alignement.

**Implémentation** :
```python
def center_agent(observation):
    mask = observation['action_mask']
    # Ordre de préférence : centre d'abord
    preference = [3, 2, 4, 1, 5, 0, 6]
    for col in preference:
        if mask[col] == 1:
            return col
```

**Avantages** :
- Meilleur positionnement que aléatoire
- Toujours simple à coder

**Limites** :
- Ne détecte pas les opportunités de victoire
- Ne bloque pas l'adversaire

---

### Niveau 2 : **Agent Offensif**
*Chercher des opportunités immédiates de victoire*

**Stratégie** :
1. Si je peux gagner en un coup → jouer ce coup
2. Sinon → jouer au hasard (ou préférer centre)

**Implémentation** :
```python
def offensive_agent(observation):
    board = observation['observation']
    mask = observation['action_mask']

    # Tester chaque colonne valide
    for col in range(7):
        if mask[col] == 1:
            # Simuler le coup
            if would_win(board, col, player=0):
                return col  # Coup gagnant !

    # Sinon, jouer au centre ou aléatoire
    return fallback_strategy(mask)
```

**Avantages** :
- Gagne quand c'est possible
- Début de logique tactique

**Limites** :
- Ne bloque pas l'adversaire
- Peut perdre bêtement

---

### Niveau 3 : **Agent Défensif**
*Jeu défensif - bloquer l'adversaire*

**Stratégie** :
1. Si je peux gagner → gagner
2. Si l'adversaire peut gagner → bloquer
3. Sinon → jouer au centre ou aléatoire

**Implémentation** :
```python
def defensive_agent(observation):
    board = observation['observation']
    mask = observation['action_mask']

    # 1. Chercher coup gagnant
    for col in range(7):
        if mask[col] == 1 and would_win(board, col, player=0):
            return col

    # 2. Bloquer l'adversaire
    for col in range(7):
        if mask[col] == 1 and would_win(board, col, player=1):
            return col  # Bloquer !

    # 3. Sinon, stratégie de repli
    return fallback_strategy(mask)
```

**Avantages** :
- Gagne quand possible
- Empêche l'adversaire de gagner facilement
- Bon niveau pour battre des humains débutants

**Limites** :
- Ne planifie pas à l'avance (seulement 1 coup)
- Ne crée pas de menaces multiples

---

### Niveau 4 : **Agent Stratégique (Heuristiques)**
*Positionnement stratégique avec règles*

**Stratégie** :
1. Gagner si possible
2. Bloquer si nécessaire
3. Créer des menaces doubles (deux façons de gagner au prochain coup)
4. Contrôler le centre
5. Éviter de donner à l'adversaire des opportunités (ne pas jouer juste au-dessus de sa menace)

**Fonctions à implémenter** :
- Détection de menaces multiples
- Évaluation de la position (score heuristique)
- Anticipation de 2-3 coups à l'avance

**Avantages** :
- Jeu beaucoup plus fort
- Crée des situations gagnantes
- Difficile à battre pour un humain moyen

**Limites** :
- Ne fait pas de recherche exhaustive
- Peut manquer des coups tactiques profonds

---

### Niveau 5+ : **Algorithmes Avancés**
*Recherche dans l'arbre de jeu*

#### Option A : **Minimax avec Alpha-Beta Pruning**

**Principe** : Explorer l'arbre de jeu, supposer que l'adversaire joue optimal.

**Avantages** :
- Jeu théoriquement optimal (avec profondeur suffisante)
- Trouve les meilleurs coups

**Limites** :
- Lent pour grandes profondeurs
- Besoin d'une bonne fonction d'évaluation

#### Option B : **Monte Carlo Tree Search (MCTS)**

**Principe** : Simuler des milliers de parties aléatoires, choisir le coup avec meilleur taux de victoire.

**Avantages** :
- Pas besoin de fonction d'évaluation
- Parallélisable
- Très fort avec assez de simulations

**Limites** :
- Lent (besoin de beaucoup de simulations)
- Stochastique (peut varier)

#### Option C : **Deep Reinforcement Learning**

**Principe** : Entraîner un réseau de neurones à jouer en jouant contre lui-même.

**Avantages** :
- Peut découvrir des stratégies non-évidentes
- Très rapide à l'inférence (après entraînement)

**Limites** :
- Entraînement long et complexe
- Besoin de beaucoup de ressources

---

## Mon plan d'implémentation

### Phase 1 : Bases (Niveaux 0-1)
- [x] Agent aléatoire
- [ ] Agent centre

### Phase 2 : Tactique simple (Niveaux 2-3)
- [ ] Fonction `would_win()` pour détecter victoire en 1 coup
- [ ] Agent offensif
- [ ] Agent défensif

### Phase 3 : Stratégie (Niveau 4)
- [ ] Évaluation de position (heuristiques)
- [ ] Détection de menaces doubles
- [ ] Agent stratégique complet

### Phase 4 : Algorithmes avancés (Niveau 5+)
- [ ] Minimax de base
- [ ] Alpha-Beta pruning
- [ ] MCTS (si temps)

---

## Tests et comparaisons

Pour chaque niveau, je vais :
1. Implémenter l'agent
2. Le tester contre les agents précédents
3. Mesurer le taux de victoire
4. Documenter les résultats

**Objectif** : Avoir au minimum un agent défensif (Niveau 3) fonctionnel !
