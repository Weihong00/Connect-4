# Tâche 2.1 — Réponses aux questions

## 1. Quelle est la forme du tableau d'observation ?

La forme est **(6, 7, 2)**.

- 6 lignes
- 7 colonnes
- 2 canaux

## 2. Que représente chaque dimension ?

- **Dimension 0 (6)** : les lignes du plateau (de haut en bas)
- **Dimension 1 (7)** : les colonnes du plateau (de gauche à droite)
- **Dimension 2 (2)** : les deux canaux qui séparent mes pions et ceux de l'adversaire
  - Canal 0 : mes pions
  - Canal 1 : pions de l'adversaire

## 3. Quelles sont les valeurs possibles dans le tableau d'observation ?

Les valeurs sont **0 ou 1** (type int8).

- **1** : il y a un pion à cette position
- **0** : la case est vide (ou c'est un pion de l'autre joueur dans l'autre canal)

Exemple :
- Si `observation[3, 2, 0] == 1` → j'ai un pion à la ligne 3, colonne 2
- Si `observation[3, 2, 1] == 1` → l'adversaire a un pion à la ligne 3, colonne 2
- Si les deux canaux valent 0 pour une case → la case est vide
