# Tâche 2.1 — Notes sur PettingZoo Connect Four

- Agents : `player_0` et `player_1`.
- `action` : l’entier qui désigne la colonne où je lâche le pion (type `int`, valeur de 0 à 6).
- `env.agent_iter()` : itérateur qui donne les agents dans l’ordre des tours (permet de boucler proprement sur chaque coup).
- `env.step(action)` : joue l’action du joueur courant, avance l’état, applique récompense/fin de partie.
- `env.last()` : renvoie pour l’agent courant `(observation, reward, termination, truncation, info)`.
- Observation : un dict avec
  - `observation` : tableau 6×7×2 (canal 0 = mes pions, canal 1 = pions adverses, dtype int8),
  - `action_mask` : vecteur de longueur 7 (1 si la colonne est jouable, 0 si elle est pleine).
- Action mask : filtre des coups légaux ; indispensable pour éviter d’envoyer un coup illégal (colonne pleine) qui ferait planter l’agent ou donner une pénalité.
