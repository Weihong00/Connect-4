# Connect Four Strategy Guide

## Table of Contents
1. [Game Theory Fundamentals](#game-theory-fundamentals)
2. [Strategic Principles](#strategic-principles)
3. [Agent Evolution](#agent-evolution)
4. [Position Evaluation](#position-evaluation)
5. [Advanced Techniques](#advanced-techniques)

---

## Game Theory Fundamentals

### Connect Four as a Solved Game

Connect Four is a **solved game**, meaning:
- With perfect play, the **first player can always force a win**
- The first player has a theoretical advantage
- Optimal strategy requires look-ahead search

### Key Strategic Concepts

1. **Center Control**
   - The center column (column 3) is the most valuable
   - Central positions offer maximum connectivity (4 directions)
   - Edge columns (0, 6) have limited winning potential

2. **Vertical Threat**
   - Easier to create than horizontal threats
   - Opponent must block immediately
   - Can be used to force opponent's moves

3. **Diagonal Superiority**
   - Hardest patterns to detect
   - Often overlooked by simple agents
   - Can create surprise wins

4. **Double Threat (Fork)**
   - Creating two winning moves simultaneously
   - Opponent can only block one
   - Guarantees victory on next turn

---

## Strategic Principles

### Priority Hierarchy

Our agents follow this decision hierarchy:

```
1. Win immediately (if possible)
   ↓
2. Block opponent's immediate win
   ↓
3. Create double threat (fork)
   ↓
4. Block opponent's potential double threat
   ↓
5. Improve position (center, connectivity)
   ↓
6. Random valid move
```

### Position Value

Different board positions have different strategic values:

```
3 4 5 7 5 4 3
4 6 8 10 8 6 4
5 8 11 13 11 8 5
5 8 11 13 11 8 5
4 6 8 10 8 6 4
3 4 5 7 5 4 3
```

- **Center columns (2-4)**: Highest value
- **Middle rows**: Better connectivity
- **Corners**: Lowest value

### Opening Theory

**Strong Openings (as first player):**
1. Start with column 3 (center) - best statistical performance
2. Alternative: columns 2 or 4 (off-center)
3. Avoid: edge columns (0, 6) on first move

**Response Strategy (as second player):**
1. If opponent plays center → play adjacent (2 or 4)
2. If opponent plays off-center → consider center or block
3. Mirror opponent's strategy in early game

---

## Agent Evolution

### Level 0: Naive Agent
- **Strategy**: Random column selection (no validation)
- **Win rate**: ~0% (illegal moves cause instant loss)
- **Purpose**: Demonstrates importance of action masking

### Level 1: Random Agent (Implemented)
- **Strategy**: Random valid move
- **Win rate**: ~50% vs itself (first-player advantage)
- **Key feature**: Respects action mask
- **Limitations**: No strategic thinking

### Level 2: Smart Agent (Implemented)
- **Strategy**: Rule-based with immediate threats
- **Win rate**: 98% vs Random
- **Features**:
  - Immediate win detection
  - Block opponent wins
  - Double threat detection
  - Center preference
- **Limitations**:
  - No look-ahead beyond 1 move
  - Can miss complex trap patterns

### Level 3: Minimax Agent (To Implement)
- **Strategy**: Adversarial search with evaluation function
- **Expected win rate**: 100% vs Random, ~85-95% vs Smart
- **Features**:
  - Multi-move look-ahead (depth 5-7)
  - Alpha-beta pruning for efficiency
  - Position evaluation function
  - Optimal tactical play
- **Limitations**:
  - Computationally expensive at high depth
  - Requires good evaluation function

### Level 4: MCTS Agent (Advanced)
- **Strategy**: Monte Carlo Tree Search
- **Expected win rate**: 100% vs Random/Smart, competitive with Minimax
- **Features**:
  - Probabilistic exploration
  - Adaptive depth
  - No need for evaluation function
  - Handles uncertainty well
- **Advantages**:
  - Better for complex positions
  - Anytime algorithm (can stop early)
  - Balances exploration/exploitation

---

## Position Evaluation

### Evaluation Function Components

A strong evaluation function considers:

#### 1. Immediate Threats (Weight: 1000)
```python
if has_winning_move(position):
    return +INFINITY
if opponent_has_winning_move(position):
    return -INFINITY
```

#### 2. Potential Winning Lines (Weight: 100)
Count sequences that could become 4-in-a-row:
- **Three-in-a-row with space** = +50
- **Two-in-a-row with two spaces** = +10
- **Opponent's threats** = negative values

#### 3. Center Control (Weight: 10)
```
Center column pieces: +3 each
Adjacent to center (2,4): +2 each
Edge columns (0,6): +1 each
```

#### 4. Connectivity (Weight: 5)
Pieces adjacent to friendly pieces are more valuable:
```
Adjacent pieces = +1 per connection
Diagonal connections = +2 (harder to block)
```

#### 5. Height Control (Weight: 3)
Lower pieces are generally better (more stable):
```
Bottom row: +3
Middle rows: +2
Top rows: +1
```

### Sample Evaluation Function

```python
def evaluate_position(board, player):
    score = 0

    # Check immediate win/loss
    if check_win(board, player):
        return 100000
    if check_win(board, opponent):
        return -100000

    # Count potential lines
    score += count_three_in_row(board, player) * 50
    score -= count_three_in_row(board, opponent) * 50

    score += count_two_in_row(board, player) * 10
    score -= count_two_in_row(board, opponent) * 10

    # Center control
    score += count_center_pieces(board, player) * 3
    score -= count_center_pieces(board, opponent) * 3

    return score
```

---

## Advanced Techniques

### 1. Alpha-Beta Pruning

Optimization for Minimax that skips branches that won't affect final decision:

```
function alphabeta(node, depth, α, β, maximizing):
    if depth = 0 or game_over:
        return evaluate(node)

    if maximizing:
        value = -∞
        for each child of node:
            value = max(value, alphabeta(child, depth-1, α, β, false))
            α = max(α, value)
            if β ≤ α:
                break  # β cutoff
        return value
    else:
        value = +∞
        for each child of node:
            value = min(value, alphabeta(child, depth-1, α, β, true))
            β = min(β, value)
            if β ≤ α:
                break  # α cutoff
        return value
```

**Efficiency gain**: Can reduce search from O(b^d) to O(b^(d/2)) with good move ordering

### 2. Move Ordering

To maximize alpha-beta efficiency:
1. **Check center columns first** (most likely to be good)
2. **Try moves that create threats**
3. **Consider moves near existing pieces**

### 3. Transposition Tables

Cache previously evaluated positions:
```python
transposition_table = {}

def minimax_with_cache(board, depth):
    board_hash = hash(board)
    if board_hash in transposition_table:
        return transposition_table[board_hash]

    # ... minimax logic ...

    transposition_table[board_hash] = result
    return result
```

### 4. Iterative Deepening

Gradually increase search depth:
```python
for depth in range(1, max_depth + 1):
    result = minimax(board, depth)
    if time_limit_reached():
        return result
return result
```

**Benefits**:
- Anytime algorithm
- Better move ordering from shallow searches
- Time management

### 5. Opening Book

Pre-computed optimal moves for early game:

```python
OPENING_BOOK = {
    "empty_board": 3,  # Play center
    "3": [2, 4],       # Opponent played center, play adjacent
    "2": 3,            # Opponent played 2, take center
    "4": 3,            # Opponent played 4, take center
}
```

---

## Statistical Analysis

### Expected Win Rates (Theoretical)

| Agent | vs Random | vs Smart | vs Minimax | vs MCTS |
|-------|-----------|----------|------------|---------|
| Random | 50% | 2% | 0% | 0% |
| Smart | 98% | 50% | 15% | 20% |
| Minimax (depth 5) | 100% | 85% | 50% | 45% |
| MCTS (1000 sims) | 100% | 80% | 55% | 50% |

### Performance Metrics

**Time Complexity:**
- Random: O(1)
- Smart: O(n) where n = number of valid actions
- Minimax (depth d): O(7^d) with pruning O(7^(d/2))
- MCTS (n simulations): O(n × game_length)

**Space Complexity:**
- Random: O(1)
- Smart: O(1)
- Minimax: O(d) for recursion stack
- MCTS: O(nodes_explored)

---

## Practical Recommendations

### For Tournament Play

1. **Against unknown opponents**: Start with Minimax (depth 5)
2. **Against random/weak players**: Smart agent is sufficient
3. **Against strong players**: Use MCTS or deeper Minimax
4. **Time-limited games**: Use iterative deepening

### For Learning

1. **Start with**: Understanding Random and Smart agents
2. **Progress to**: Implementing Minimax with simple evaluation
3. **Advanced**: Add alpha-beta, transposition tables
4. **Expert**: Implement MCTS with UCT formula

### Debugging Strategy

1. **Visualization**: Always visualize board states
2. **Unit tests**: Test each component separately
3. **Known positions**: Test against solved positions
4. **Gradual complexity**: Start with depth 1, then increase
5. **Performance profiling**: Identify bottlenecks

---

## Conclusion

Effective Connect Four strategy combines:
- **Tactical thinking**: Immediate threats and responses
- **Strategic planning**: Position building and long-term advantage
- **Algorithmic efficiency**: Search optimization and pruning
- **Adaptation**: Learning from opponent patterns

The progression from Random → Smart → Minimax → MCTS demonstrates increasing sophistication in both strategy and algorithm design.

---

*This document provides the theoretical foundation for the agents implemented in this project.*
