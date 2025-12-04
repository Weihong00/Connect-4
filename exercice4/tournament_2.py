# tournament_2.py
from pettingzoo.classic import connect_four_v3
import numpy as np
from itertools import combinations


def run_tournament(agents_classes, num_games=10):
    """
    Exécute un tournoi round-robin entre plusieurs agents (2, 3, ou plus).
    Chaque paire d'agents joue num_games parties.

    Args:
        agents_classes: Liste de classes d'agents [Agent1Class, Agent2Class, ...]
        num_games: Nombre de parties entre chaque paire

    Returns:
        dict: Résultats détaillés du tournoi
    """
    n_agents = len(agents_classes)

    if n_agents < 2:
        raise ValueError("Il faut au moins 2 agents pour un tournoi")

    # Initialiser les statistiques
    stats = {i: {'wins': 0, 'losses': 0, 'draws': 0, 'name': agents_classes[i].__name__}
             for i in range(n_agents)}

    # Résultats head-to-head
    head_to_head = {}

    print("=" * 70)
    print(f"TOURNOI ROUND-ROBIN - {n_agents} agents")
    print("=" * 70)
    print(f"Agents: {', '.join([cls.__name__ for cls in agents_classes])}")
    print(f"Nombre de parties par paire: {num_games}")
    print("=" * 70)
    print()

    # Générer toutes les paires
    pairs = list(combinations(range(n_agents), 2))
    total_games = len(pairs) * num_games
    games_played = 0

    # Jouer chaque paire
    for idx1, idx2 in pairs:
        agent1_class = agents_classes[idx1]
        agent2_class = agents_classes[idx2]

        print(f"\n--- {agent1_class.__name__} vs {agent2_class.__name__} ---")

        # Statistiques pour cette paire
        pair_wins = {0: 0, 1: 0}
        pair_draws = 0

        for game_idx in range(num_games):
            env = connect_four_v3.env()
            env.reset()

            # Alterner qui commence (player_0 ou player_1)
            if game_idx % 2 == 0:
                # Agent1 commence
                agent_instances = {
                    'player_0': agent1_class(env, player_name=agent1_class.__name__),
                    'player_1': agent2_class(env, player_name=agent2_class.__name__)
                }
                agent_map = {0: idx1, 1: idx2}  # player_0 -> idx1, player_1 -> idx2
            else:
                # Agent2 commence
                agent_instances = {
                    'player_0': agent2_class(env, player_name=agent2_class.__name__),
                    'player_1': agent1_class(env, player_name=agent1_class.__name__)
                }
                agent_map = {0: idx2, 1: idx1}  # player_0 -> idx2, player_1 -> idx1

            # Jouer la partie
            winner = None
            for agent_id in env.agent_iter():
                observation, reward, termination, truncation, info = env.last()

                if termination or truncation:
                    if reward == 1:
                        winner = agent_id
                    env.step(None)
                else:
                    curr_agent = agent_instances[agent_id]
                    mask = observation["action_mask"]
                    action = curr_agent.choose_action(observation, reward, termination, truncation, info, mask)
                    env.step(action)

            # Enregistrer le résultat
            games_played += 1
            if winner == 'player_0':
                winner_idx = agent_map[0]
                loser_idx = agent_map[1]
                stats[winner_idx]['wins'] += 1
                stats[loser_idx]['losses'] += 1
                if game_idx % 2 == 0:
                    pair_wins[0] += 1
                else:
                    pair_wins[1] += 1
                print(f"  Partie {game_idx+1}: {stats[winner_idx]['name']} gagne", end="")
            elif winner == 'player_1':
                winner_idx = agent_map[1]
                loser_idx = agent_map[0]
                stats[winner_idx]['wins'] += 1
                stats[loser_idx]['losses'] += 1
                if game_idx % 2 == 0:
                    pair_wins[1] += 1
                else:
                    pair_wins[0] += 1
                print(f"  Partie {game_idx+1}: {stats[winner_idx]['name']} gagne", end="")
            else:
                stats[idx1]['draws'] += 1
                stats[idx2]['draws'] += 1
                pair_draws += 1
                print(f"  Partie {game_idx+1}: Match nul", end="")

            print(f" [{games_played}/{total_games}]")

        # Résumé de la paire
        print(f"\nRésumé {agent1_class.__name__} vs {agent2_class.__name__}:")
        print(f"  {agent1_class.__name__}: {pair_wins[0]} victoires")
        print(f"  {agent2_class.__name__}: {pair_wins[1]} victoires")
        print(f"  Nuls: {pair_draws}")

        # Stocker head-to-head
        head_to_head[(idx1, idx2)] = (pair_wins[0], pair_wins[1], pair_draws)

    # Afficher les résultats finaux
    print("\n" + "=" * 70)
    print("CLASSEMENT FINAL")
    print("=" * 70)

    # Trier par nombre de victoires
    ranking = sorted(stats.items(), key=lambda x: x[1]['wins'], reverse=True)

    print(f"\n{'Rang':<6} {'Agent':<25} {'V':<5} {'D':<5} {'N':<5} {'Win%':<8}")
    print("-" * 70)

    medals = ["🥇", "🥈", "🥉"]
    for rank, (idx, data) in enumerate(ranking, 1):
        total = data['wins'] + data['losses'] + data['draws']
        win_rate = (data['wins'] / total * 100) if total > 0 else 0
        medal = medals[rank-1] if rank <= 3 else "  "
        print(f"{medal} {rank:<4} {data['name']:<25} {data['wins']:<5} {data['losses']:<5} {data['draws']:<5} {win_rate:>6.1f}%")

    # Head-to-head
    print("\n" + "=" * 70)
    print("HEAD-TO-HEAD")
    print("=" * 70)
    print()

    for (idx1, idx2), (w1, w2, d) in head_to_head.items():
        name1 = stats[idx1]['name']
        name2 = stats[idx2]['name']
        print(f"{name1} vs {name2}: {w1}-{w2}-{d}")

    print("\n" + "=" * 70)

    return {
        'stats': stats,
        'head_to_head': head_to_head,
        'ranking': ranking
    }
