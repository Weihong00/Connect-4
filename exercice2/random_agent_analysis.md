# Random Agent Analysis Report

## Experiment Setup
- **Number of games**: 100
- **Players**: Two RandomAgent instances (random move selection)
- **Environment**: PettingZoo Connect Four

---

## Results Summary

| Metric | Value |
|--------|-------|
| Player 0 (First) Wins | 55 (55.00%) |
| Player 1 (Second) Wins | 44 (44.00%) |
| Draws | 1 (1.00%) |

### Game Length Statistics
| Metric | Value |
|--------|-------|
| Average moves per game | 22.37 |
| Minimum moves | 7 |
| Maximum moves | 42 |

---

## Analysis

### 1. Win Distribution
Player 0 (first player) won 55 games, while Player 1 (second player) won 44 games. The distribution is **not perfectly equal**, with a difference of 11 games (11 percentage points).

### 2. First-Mover Advantage
**Yes, there appears to be a first-mover advantage.** Player 0 (first player) has a win rate of 55%, which is higher than Player 1's 44%. This makes sense because:
- The first player gets to place their piece first, giving them more opportunities to create winning combinations
- In Connect Four, the first player can always occupy the center column first, which is strategically advantageous
- The first player has one more move than the second player in most games

The ~11% advantage for the first player is consistent with theoretical analysis of Connect Four, which proves that with perfect play, the first player can always win.

### 3. Game Length Analysis
- **Average game length**: 22.37 moves
- **Shortest game**: 7 moves (the theoretical minimum to win Connect Four is 7 moves - 4 by one player, 3 by the other)
- **Longest game**: 42 moves (the maximum possible is 42 moves when the board is completely filled)

The average of ~22 moves indicates that most games end well before the board is full, meaning wins are achieved rather than draws being common.

### 4. Draw Frequency
**Draws are very rare** - only 1 out of 100 games (1.00%). This is because:
- Random play is unlikely to result in a perfectly blocked board
- With 42 possible cells and only 4 needed in a row, there are many opportunities to accidentally complete a winning line
- Draws require very specific piece placements that block all winning possibilities for both players

---

## Conclusions

1. **Random play leads to a first-mover advantage of approximately 10-11%**
2. **Draws are extremely rare (~1%) in random play** because winning combinations are easily formed by chance
3. **Games typically end around move 22**, well before the board fills up
4. **The minimum game length (7 moves) was achieved**, showing that quick wins are possible even with random play
5. **Random agents are not strategic** - they don't block opponent wins or set up their own winning moves, leading to relatively short games

---

*Report generated from 100 games of RandomAgent vs RandomAgent*
