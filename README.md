# 2048 - Single Selected Tile Movement

A Python implementation of the classic 2048 puzzle game with a unique twist: single-tile selection movement. Built using Tkinter for the graphical interface.

## Game Features

- **Single Tile Selection**: Unlike the classic 2048 where all tiles move simultaneously, this version requires you to select a specific tile first, then move only that tile in the chosen direction
- **Swipe Support**: Touch and mouse drag gestures for mobile-like interaction
- **Configurable Board Size**: Adjustable board size from 2x2 to 8x8
- **Score Tracking**: Current score and best score display
- **Responsive Controls**: Keyboard (arrow keys/WASD) and swipe input methods

## Installation

### Requirements
- Python 3.x
- Tkinter (included with Python's standard library)

### Setup
1. Ensure Python 3 is installed on your system
2. No additional dependencies required - Tkinter is included with Python
3. Clone or download the `2048.py` file to your desired directory

## Running the Game

### Basic Usage
```bash
python 2048.py
```

### With Custom Board Size
```bash
python 2048.py [size]
```
Where `[size]` is an integer between 2 and 8 (default: 4)

### Examples
```bash
# Default 4x4 board
python 2048.py

# 5x5 board
python 2048.py 5

# 6x6 board
python 2048.py 6
```

## Gameplay Instructions

### Objective
Reach the target tile value of 100 (configurable) by combining tiles with the same value.

### How to Play

1. **Select a Tile**: Click or tap on any tile with a value (2, 4, 8, etc.) to select it
   - Selected tiles are highlighted with a thicker border
   - Empty tiles (value 0) cannot be selected

2. **Move the Selected Tile**:
   - **Keyboard**: Use arrow keys or WASD keys to move the selected tile
     - ↑/W: Move up
     - ↓/S: Move down
     - ←/A: Move left
     - →/D: Move right
   - **Swipe/Touch**: Drag your finger or mouse in the desired direction

3. **Tile Movement Rules**:
   - The selected tile moves as far as possible in the chosen direction
   - Movement stops when hitting the board edge or another tile
   - If the tile encounters another tile with the same value, they merge into a single tile with double the value
   - Only one merge can occur per move
   - After each move, a new tile (2 or 4) appears in a random empty position

4. **Game End Conditions**:
   - **Win**: Reach a tile with value ≥ 100
   - **Lose**: No valid moves remaining (board is full and no adjacent tiles can merge)

### Game Controls

- **Restart**: Click the "Restart" button to start a new game
- **Board Size**: Enter a new size (2-8) in the text field and click "Apply"
- **Swipe Toggle**: Enable/disable swipe gestures with the checkbox
- **Tile Selection**: Click any numbered tile to select/deselect it

## Implementation Details

### Architecture
- **Single File Implementation**: All game logic contained in `2048.py`
- **Class-based Design**: `Game2048Single` class encapsulates all game functionality
- **Event-driven GUI**: Built with Tkinter's event binding system

### Key Components

#### Game Logic
- `new_board(n)`: Creates an empty n×n game board
- `add_random_tile(board)`: Adds a 2 or 4 tile to a random empty position (90% chance of 2, 10% chance of 4)
- `any_moves_possible(board)`: Checks if any valid moves remain
- `reached_target(board, target)`: Verifies win condition

#### Movement System
- **Single Tile Movement**: Only the selected tile moves when a direction is chosen
- **Collision Detection**: Handles tile merging and movement boundaries
- **Merge Logic**: Tiles combine when they have identical values (single merge per move)

#### User Interface
- **Dynamic Board**: Supports configurable board sizes (2×2 to 8×8)
- **Visual Feedback**: Selected tiles highlighted with enhanced borders
- **Color Coding**: Different colors for each tile value
- **Score Display**: Real-time score and best score tracking

#### Input Handling
- **Keyboard Support**: Arrow keys and WASD for movement
- **Mouse/Touch Support**: Click to select, drag to swipe
- **Responsive Design**: Minimum swipe threshold to prevent accidental moves

### Technical Features

#### Swipe Detection
- Mouse and touch event handling for drag gestures
- Coordinate-based direction calculation
- Threshold filtering to prevent accidental inputs

#### GUI Updates
- Real-time board state synchronization
- Efficient tile color and text updates
- Dynamic score tracking and persistence

#### Configuration
- Default board size: 4×4
- Win target: 100
- Adjustable parameters through in-game UI

### File Structure
```
2048.py          # Main game file containing all implementation
best_score.txt   # Stores the player's best score (auto-generated)
```

## Customization

### Changing Default Settings
Edit the configuration variables at the top of `2048.py`:
```python
BOARD_SIZE = 4      # Default board size (2-8)
TARGET = 100        # Win target value
```

### Adding New Features
The modular design makes it easy to extend:
- Add new tile colors to the `TILE_COLORS` dictionary
- Modify movement logic in the `move_selected()` method
- Extend input handling in the event binding section

## Troubleshooting

### Common Issues

**Game won't start:**
- Ensure Python 3 is installed
- Check that `2048.py` is in the current directory
- Verify Tkinter is available (`import tkinter` in Python console)

**Swipe not working:**
- Ensure "Enable Swipe" checkbox is checked in-game
- Try increasing the swipe threshold in the code if needed

**Display issues:**
- The game window is not resizable - this is intentional for consistent gameplay
- If tiles appear too small/large, adjust the board size in-game

## License

This implementation is provided as-is for educational and entertainment purposes.

## Acknowledgments

Based on the classic 2048 game concept by Gabriele Cirulli.
