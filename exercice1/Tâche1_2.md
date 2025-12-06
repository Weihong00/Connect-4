# Tâche 1.2 — Conditions de victoire (mes notes)

## Les 4 motifs possibles

```
Horizontal : █ █ █ █
Vertical   :
█
█
█
█
Diag ↘ :
█ . . .
. █ . .
. . █ .
. . . █
Diag ↗ :
. . . █
. . █ .
. █ . .
█ . . .
```

## Quoi vérifier après avoir joué un pion
- Il suffit de regarder 4 directions : horizontale, verticale, diagonale ↘, diagonale ↗.

## Comment je vérifie 

Idée : je pars de la case posée `(r, c)`, j’avance dans un sens puis dans l’autre, et je compte combien de pions identiques je touche d’affilée. Si ça fait 4 ou plus en tout, c’est gagné.

### Schéma commun
```
count = 1  # le pion que je viens de poser
count += align(r, c, dr, dc)       # avance dans un sens
count += align(r, c, -dr, -dc)     # puis dans l'autre
si count >= 4 : victoire
```

### La petite fonction align
```
steps = 0
tant que (r+dr, c+dc) est dans la grille et contient mon pion :
    r += dr
    c += dc
    steps += 1
retourner steps
```

### Les couples (dr, dc) à utiliser
- Horizontal : (0, +1) et (0, -1)
- Vertical : (+1, 0) et (-1, 0)
- Diag ↘ : (+1, +1) et (-1, -1)
- Diag ↗ : (-1, +1) et (+1, -1)

### Flow complet après un coup
```
pour chaque direction parmi les 4 ci-dessus :
    appliquer le schéma commun
    si count >= 4 : retour vrai
sinon : retour faux
```
