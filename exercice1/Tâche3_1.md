# Tâche 3.1 — Décomposition de l'implémentation d'un agent

## 1. Analyse des entrées : Quelles informations l'agent reçoit-il ?

L'agent reçoit un **dictionnaire d'observation** avec deux clés :

- **`observation['observation']`** : tableau numpy de forme (6, 7, 2)
  - Canal 0 : mes pions (1 = pion présent, 0 = vide)
  - Canal 1 : pions de l'adversaire (1 = pion présent, 0 = vide)

- **`observation['action_mask']`** : tableau de 7 éléments (un par colonne)
  - 1 = colonne jouable (pas pleine)
  - 0 = colonne pleine (action invalide)

En plus, l'agent peut recevoir :
- `reward` : récompense du coup précédent (0, 1 ou -1)
- `termination` / `truncation` : si le jeu est terminé
- `info` : dict avec infos supplémentaires (souvent vide)

## 2. Détection des coups valides : Comment déterminer quelles colonnes sont jouables ?

C'est simple grâce à l'**action_mask** !

```python
mask = observation['action_mask']
colonnes_valides = np.where(mask == 1)[0]
# ou
colonnes_valides = [i for i in range(7) if mask[i] == 1]
```

**Pourquoi c'est important ?**
- Jouer dans une colonne pleine = erreur
- L'action_mask nous évite de vérifier manuellement si la colonne est pleine

## 3. Sélection du coup : Quel algorithme utiliser pour choisir un coup ?

Plusieurs options selon le niveau de l'agent :

### Agent aléatoire (simple)
```python
action = np.random.choice(colonnes_valides)
```

### Agent avec heuristiques (intermédiaire)
- Vérifier s'il y a un coup gagnant → le jouer
- Vérifier si l'adversaire peut gagner → bloquer
- Sinon, jouer au centre ou une colonne stratégique

### Agent avec recherche (avancé)
- Minimax : explorer l'arbre de jeu, évaluer les positions
- MCTS (Monte Carlo Tree Search) : simuler des parties aléatoires
- Alpha-Beta pruning : optimiser minimax

## 4. Sortie : Que doit retourner l'agent ?

L'agent doit retourner un **entier entre 0 et 6** représentant la colonne choisie.

```python
def select_action(observation):
    # ... logique de sélection ...
    return action  # int entre 0 et 6
```

**Important** :
- L'action doit être valide (vérifier avec action_mask)
- Type : `int` ou `np.int64` (pas str, float, etc.)
- Retourner une action invalide = erreur ou défaite automatique

---

## Squelette d'un agent basique

```python
def mon_agent(observation):
    # 1. Extraire les infos
    board = observation['observation']
    mask = observation['action_mask']

    # 2. Trouver les coups valides
    valid_actions = np.where(mask == 1)[0]

    # 3. Choisir un coup
    # (ici on fait aléatoire, mais on peut améliorer)
    action = np.random.choice(valid_actions)

    # 4. Retourner
    return action
```

Prochaine étape : implémenter cet agent et le tester !
