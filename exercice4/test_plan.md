# Test Plan for Connect Four Agents

## Project Constraints (Contraintes du projet)

| Constraint | Limit | Description |
|------------|-------|-------------|
| **Time** | **3 seconds max** per move | Each decision must complete within 3s |
| **Memory** | **384 MB max** | Total memory usage must stay under 384MB |
| **CPU** | **1 core max** | Single-threaded execution only |

---

## 1.1 What to Test?

### Functional Tests (Tests fonctionnels)

| Test ID | Description | Priority |
|---------|-------------|----------|
| F1 | Agent always selects a valid column (0-6) | Critical |
| F2 | Agent respects action mask (never plays in full column) | Critical |
| F3 | Agent handles game termination correctly | Critical |
| F4 | Agent works as both player_0 (first) and player_1 (second) | High |
| F5 | Agent handles edge case: only one valid move | Medium |
| F6 | Agent handles edge case: board almost full | Medium |
| F7 | Agent returns correct data type (int) | Low |

### Performance Tests (Tests de performance)

| Test ID | Description | Priority | Constraint |
|---------|-------------|----------|------------|
| P1 | Decision time per move | **Critical** | **< 3 seconds** |
| P2 | Memory usage during game | **Critical** | **< 384 MB** |
| P3 | CPU usage (single core) | **Critical** | **1 core only** |
| P4 | Performance over many games (no memory leaks) | High | Stable memory |
| P5 | Worst-case decision time (complex board) | High | < 3 seconds |

### Strategic Tests (Tests stratégiques)

| Test ID | Description | Priority |
|---------|-------------|----------|
| S1 | Win rate against RandomAgent | Critical |
| S2 | Takes winning move when available | Critical |
| S3 | Blocks opponent's winning move | Critical |
| S4 | Creates double threats when possible | High |
| S5 | Blocks opponent's double threats | High |
| S6 | Prefers center columns in opening | Medium |
| S7 | Win rate as first player vs second player | Medium |

---

## 1.2 How to Test?

### Functional Tests Methods

#### F1 & F2: Valid Move Selection
```python
# Create specific board states and verify action is valid
def test_valid_action():
    board = create_test_board()
    action_mask = get_action_mask(board)
    action = agent.choose_action(board, action_mask=action_mask)

    assert 0 <= action <= 6, "Action must be 0-6"
    assert action_mask[action] == 1, "Action must be valid per mask"
```

#### F3: Game Termination
```python
# Play complete games and verify no errors at termination
def test_game_completion():
    for _ in range(100):
        play_complete_game()  # Should not raise exceptions
```

#### F4: Both Player Positions
```python
# Test agent as player_0 and player_1
def test_both_positions():
    results_as_first = play_games(agent_position="player_0", num_games=50)
    results_as_second = play_games(agent_position="player_1", num_games=50)
    # Both should work without errors
```

### Performance Tests Methods

#### P1: Decision Time
```python
import time

def test_decision_time():
    times = []
    for _ in range(1000):
        start = time.time()
        agent.choose_action(observation, action_mask=mask)
        times.append(time.time() - start)

    avg_time = sum(times) / len(times)
    max_time = max(times)
    return avg_time, max_time
```

#### P2: Memory Usage
```python
import tracemalloc

def test_memory_usage():
    tracemalloc.start()

    for _ in range(100):
        play_complete_game()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return current / 1024 / 1024, peak / 1024 / 1024  # MB
```

### Strategic Tests Methods

#### S1: Win Rate Against Random
```python
def test_win_rate():
    results = {"wins": 0, "losses": 0, "draws": 0}

    for game in range(100):
        # Alternate first/second player
        winner = play_game(smart_first=(game % 2 == 0))
        if winner == "smart":
            results["wins"] += 1
        elif winner == "random":
            results["losses"] += 1
        else:
            results["draws"] += 1

    win_rate = results["wins"] / 100 * 100
    return win_rate
```

#### S2 & S3: Winning/Blocking Moves
```python
import numpy as np

def test_takes_winning_move():
    # Create board where agent can win
    board = np.zeros((6, 7, 2))
    board[5, 0, 0] = 1
    board[5, 1, 0] = 1
    board[5, 2, 0] = 1
    # Agent should play column 3 to win

    action = agent.choose_action(board, action_mask=[1]*7)
    assert action == 3, "Should take winning move"

def test_blocks_opponent():
    # Create board where opponent can win
    board = np.zeros((6, 7, 2))
    board[5, 0, 1] = 1  # Opponent's pieces
    board[5, 1, 1] = 1
    board[5, 2, 1] = 1
    # Agent should play column 3 to block

    action = agent.choose_action(board, action_mask=[1]*7)
    assert action == 3, "Should block opponent"
```

---

## 1.4 Specific Test Scenarios (Scénarios de test spécifiques)

### Scenario 1: Detect Immediate Win (Horizontal)
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . . . . .    (row 2)
. . . . . . .    (row 3)
. . . . . . .    (row 4)
X X X . . . .    (row 5) <- Bottom row, 3 X's connected
```
**Expected Behavior:** Agent plays column 3 to win immediately

```python
def test_scenario_1_horizontal_win():
    board = np.zeros((6, 7, 2))
    board[5, 0, 0] = 1  # X at (5,0)
    board[5, 1, 0] = 1  # X at (5,1)
    board[5, 2, 0] = 1  # X at (5,2)

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    assert action == 3, "Should complete horizontal 4-in-a-row"
```

---

### Scenario 2: Block Opponent's Win (Horizontal)
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . . . . .    (row 2)
. . . . . . .    (row 3)
. . . . . . .    (row 4)
O O O . . . .    (row 5) <- Opponent has 3 O's connected
```
**Expected Behavior:** Agent plays column 3 to block opponent

```python
def test_scenario_2_block_horizontal():
    board = np.zeros((6, 7, 2))
    board[5, 0, 1] = 1  # O at (5,0) - opponent
    board[5, 1, 1] = 1  # O at (5,1)
    board[5, 2, 1] = 1  # O at (5,2)

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    assert action == 3, "Should block opponent's horizontal win"
```

---

### Scenario 3: Detect Vertical Win
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . . . . .    (row 2)
. . X . . . .    (row 3) <- Need to play here to win
X . X . . . .    (row 4)
X . X . . . .    (row 5)
```
**Expected Behavior:** Agent plays column 2 to complete vertical 4-in-a-row

```python
def test_scenario_3_vertical_win():
    board = np.zeros((6, 7, 2))
    # Vertical stack in column 2
    board[5, 2, 0] = 1  # X at (5,2)
    board[4, 2, 0] = 1  # X at (4,2)
    board[3, 2, 0] = 1  # X at (3,2)
    # Some opponent pieces to make it realistic
    board[5, 0, 1] = 1
    board[4, 0, 1] = 1

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    assert action == 2, "Should complete vertical 4-in-a-row"
```

---

### Scenario 4: Detect Diagonal Win (Bottom-Left to Top-Right)
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . X . . .    (row 2) <- Need to play here to win
. . X O . . .    (row 3)
. X O O . . .    (row 4)
X O O O . . .    (row 5)
```
**Expected Behavior:** Agent plays column 3 to complete diagonal

```python
def test_scenario_4_diagonal_win():
    board = np.zeros((6, 7, 2))
    # Diagonal X pieces (bottom-left to top-right)
    board[5, 0, 0] = 1  # X at (5,0)
    board[4, 1, 0] = 1  # X at (4,1)
    board[3, 2, 0] = 1  # X at (3,2)
    # Supporting opponent pieces
    board[5, 1, 1] = 1  # O
    board[5, 2, 1] = 1  # O
    board[5, 3, 1] = 1  # O
    board[4, 2, 1] = 1  # O
    board[3, 3, 1] = 1  # O

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    assert action == 3, "Should complete diagonal 4-in-a-row"
```

---

### Scenario 5: Priority - Win Over Block
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . . . . .    (row 2)
. . . . . . .    (row 3)
. . . . . . .    (row 4)
X X X . O O O    (row 5) <- Both can win with column 3!
```
**Expected Behavior:** Agent should prioritize winning (column 3) over blocking

```python
def test_scenario_5_win_priority():
    board = np.zeros((6, 7, 2))
    # Agent can win
    board[5, 0, 0] = 1  # X
    board[5, 1, 0] = 1  # X
    board[5, 2, 0] = 1  # X
    # Opponent can also win
    board[5, 4, 1] = 1  # O
    board[5, 5, 1] = 1  # O
    board[5, 6, 1] = 1  # O

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    assert action == 3, "Should prioritize winning over blocking"
```

---

### Scenario 6: Only One Valid Move
**Board State:**
```
X O X O X O .    (row 0) <- Only column 6 is available
O X O X O X O    (row 1)
X O X O X O X    (row 2)
O X O X O X O    (row 3)
X O X O X O X    (row 4)
O X O X O X O    (row 5)
```
**Expected Behavior:** Agent must play column 6 (only valid option)

```python
def test_scenario_6_single_valid_move():
    board = np.zeros((6, 7, 2))
    # Fill the board except column 6
    for row in range(6):
        for col in range(6):
            if (row + col) % 2 == 0:
                board[row, col, 0] = 1
            else:
                board[row, col, 1] = 1

    # Action mask: only column 6 is valid
    action_mask = np.array([0, 0, 0, 0, 0, 0, 1])

    action = agent.choose_action(board, action_mask=action_mask)
    assert action == 6, "Should play the only available column"
```

---

### Scenario 7: Double Threat Creation
**Board State:**
```
. . . . . . .    (row 0)
. . . . . . .    (row 1)
. . . . . . .    (row 2)
. . . . . . .    (row 3)
. . X . . . .    (row 4)
. X X . . . .    (row 5) <- Playing col 0 or 3 creates double threat
```
**Expected Behavior:** Agent creates a double threat (two ways to win)

```python
def test_scenario_7_double_threat():
    board = np.zeros((6, 7, 2))
    board[5, 1, 0] = 1  # X at (5,1)
    board[5, 2, 0] = 1  # X at (5,2)
    board[4, 2, 0] = 1  # X at (4,2)

    action = agent.choose_action(board, action_mask=np.array([1,1,1,1,1,1,1]))
    # Either column 0 or 3 creates a double threat
    assert action in [0, 3], "Should create double threat"
```

---

### Scenario Summary Table

| Scenario | Type | Expected Action | Priority Tested |
|----------|------|-----------------|-----------------|
| 1 | Horizontal Win | Column 3 | Rule 1: Take winning move |
| 2 | Block Horizontal | Column 3 | Rule 2: Block opponent |
| 3 | Vertical Win | Column 2 | Rule 1: Take winning move |
| 4 | Diagonal Win | Column 3 | Rule 1: Take winning move |
| 5 | Win vs Block | Column 3 | Priority: Win > Block |
| 6 | Single Option | Column 6 | Edge case handling |
| 7 | Double Threat | Column 0 or 3 | Rule 3: Create threats |

#### Tournament (Tournoi)
```python
def run_tournament(agents, games_per_pair=20):
    """Round-robin tournament between multiple agents"""
    results = {name: {"wins": 0, "losses": 0, "draws": 0}
               for name in agents.keys()}

    for name1, agent1 in agents.items():
        for name2, agent2 in agents.items():
            if name1 >= name2:
                continue

            for _ in range(games_per_pair):
                winner = play_game(agent1, agent2)
                # Update results...

    return results
```

---

## 1.3 Success Criteria (Critères de succès)

### SmartAgent Success Criteria

| Category | Metric | Target | Constraint | Priority |
|----------|--------|--------|------------|----------|
| **Strategy** | Win rate vs RandomAgent | > 90% | - | Critical |
| **Strategy** | Takes winning move | 100% | - | Critical |
| **Strategy** | Blocks opponent's win | 100% | - | Critical |
| **Performance** | Avg decision time | < 500ms | **< 3s (hard limit)** | **Critical** |
| **Performance** | Max decision time | < 2s | **< 3s (hard limit)** | **Critical** |
| **Performance** | Memory usage | < 300MB | **< 384MB (hard limit)** | **Critical** |
| **Performance** | CPU cores used | 1 | **1 core (hard limit)** | **Critical** |
| **Functional** | Valid moves | 100% | - | Critical |
| **Functional** | Works both positions | Yes | - | Critical |

### RandomAgent Success Criteria

| Category | Metric | Target | Priority |
|----------|--------|--------|----------|
| **Functional** | Valid moves | 100% | Critical |
| **Functional** | Works both positions | Yes | Critical |
| **Performance** | Avg decision time | < 1ms | High |
| **Strategy** | Win rate vs itself | ~50% (balanced) | Low |

### Detailed Thresholds

#### Win Rate Interpretation
| Win Rate | Interpretation |
|----------|----------------|
| > 95% | Excellent - Agent dominates |
| 90-95% | Very Good - Strong performance |
| 80-90% | Good - Solid advantage |
| 60-80% | Acceptable - Clear improvement over random |
| < 60% | Needs Improvement |

#### Performance Thresholds (Aligned with Project Constraints)

**Hard Limits (Must Not Exceed):**
| Constraint | Limit | Consequence if Exceeded |
|------------|-------|------------------------|
| Time per move | **3 seconds** | Disqualification |
| Memory | **384 MB** | Disqualification |
| CPU cores | **1 core** | Disqualification |

**Target Thresholds:**
| Metric | Excellent | Good | Acceptable | Violation |
|--------|-----------|------|------------|-----------|
| Avg Time | < 100ms | < 500ms | < 2s | **> 3s** |
| Max Time | < 500ms | < 1s | < 2.5s | **> 3s** |
| Memory | < 100MB | < 200MB | < 350MB | **> 384MB** |

---

## Test Execution Plan

### Phase 1: Unit Tests
1. Test `_get_valid_actions()`
2. Test `_get_next_row()`
3. Test `_check_win_from_position()`
4. Test `_find_winning_move()`
5. Test `_creates_double_threat()`

### Phase 2: Integration Tests
1. Single game completion
2. Multiple games without errors
3. Agent vs Agent matchups

### Phase 3: Performance Tests
1. Decision time benchmarks
2. Memory profiling
3. Stress testing (1000+ games)

### Phase 4: Strategic Tests
1. Win rate analysis
2. Tournament results
3. Edge case handling

---

## Test Commands

```bash
# Run all unit tests
python tests/test_smart_agent.py

# Run random agent tests
python tests/test_random_agent.py

# Run performance benchmark (with constraint verification)
python -c "
import time
import tracemalloc
from pettingzoo.classic import connect_four_v3
from agents.smart_agent import SmartAgent

# Constants - Project Constraints
MAX_TIME_PER_MOVE = 3.0  # seconds
MAX_MEMORY = 384  # MB

env = connect_four_v3.env()
env.reset()
agent = SmartAgent(env)

# Start memory tracking
tracemalloc.start()

times = []
violations = 0
for _ in range(1000):
    obs = env.observe('player_0')
    start = time.time()
    agent.choose_action(obs['observation'], action_mask=obs['action_mask'])
    elapsed = time.time() - start
    times.append(elapsed)
    if elapsed > MAX_TIME_PER_MOVE:
        violations += 1

# Get memory stats
current_mem, peak_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

peak_mb = peak_mem / 1024 / 1024

print('=== Performance Results ===')
print(f'Avg Time: {sum(times)/len(times)*1000:.3f}ms')
print(f'Max Time: {max(times)*1000:.3f}ms')
print(f'Peak Memory: {peak_mb:.2f}MB')
print()
print('=== Constraint Verification ===')
print(f'Time Violations (> {MAX_TIME_PER_MOVE}s): {violations}/1000')
print(f'Memory OK: {\"YES\" if peak_mb < MAX_MEMORY else \"NO - VIOLATION\"} ({peak_mb:.2f}/{MAX_MEMORY}MB)')
print(f'Max Time OK: {\"YES\" if max(times) < MAX_TIME_PER_MOVE else \"NO - VIOLATION\"} ({max(times):.3f}/{MAX_TIME_PER_MOVE}s)')
"

# Verify single-core execution (CPU constraint)
python -c "
import os
import multiprocessing
print(f'Available CPUs: {multiprocessing.cpu_count()}')
print(f'Agent should use only 1 core (single-threaded)')
# Note: SmartAgent is single-threaded by design
"
```

---

*Test Plan Version 1.1 - Updated with Project Constraints (3s/move, 384MB memory, 1 CPU core)*
