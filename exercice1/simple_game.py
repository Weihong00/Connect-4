from pettingzoo.classic import connect_four_v3

# Créer l'environnement avec affichage visuel
# render_mode="human" pour voir le jeu en direct
# render_mode=None si je veux juste voir dans la console
env = connect_four_v3.env(render_mode="human")
env.reset(seed=42)

# Boucle de jeu : les deux joueurs jouent à tour de rôle
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    # Vérifier si le jeu est terminé
    if termination or truncation:
        action = None
        # Afficher le résultat
        if reward == 1:
            print(f"{agent} Wins!")
        elif reward == 0:
            print("It's a draw!")
        else:
            print(f"{agent} lose!")
    else:
        # Choisir une colonne aléatoire parmi celles qui sont jouables
        mask = observation["action_mask"]
        action = env.action_space(agent).sample(mask)
        print(f"{agent} joue la colonne {action}")

    # Jouer le coup
    env.step(action)

input("Press Enter to close...")
env.close()
