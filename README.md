# Connect 4 - AI with Alpha-Beta Pruning

This project is a graphical Connect 4 game built with Python and Pygame. The player plays against an AI agent that uses the minimax algorithm with alpha-beta pruning to choose moves.

The game includes a main menu, difficulty selection, mouse controls, a pause menu, hover preview, falling piece animation, and a game-over screen.

---

## Features

- Graphical Connect 4 board using Pygame
- Player vs AI gameplay
- AI uses minimax with alpha-beta pruning
- Easy, Medium, and Hard difficulty options
- Mouse-click controls
- Highlight preview showing where the player piece will land
- Falling piece animation
- Pause menu during gameplay
- Restart and main menu options after the game ends
- Winning pieces are highlighted

---

## Requirements

Before running the project, make sure you have Python installed.

Recommended Python version:

```bash
Python 3.10 or newer
```

This project uses the following external library:

```bash
pygame
```

All required libraries are listed in `requirements.txt`.

---

## Installation Instructions

### 1. Download or open the project folder

Make sure all project files are in the same folder:

```text
main.py
connect4.py
ai.py
requirements.txt
README.md
```

---

### 2. Open a terminal in the project folder

On Windows, you can right-click inside the project folder and choose:

```text
Open in Terminal
```

Or manually navigate to the folder using `cd`.

Example:

```bash
cd "C:\Users\YourName\Desktop\CPSC 481\CPSC-481-Project"
```

On macOS or Linux, use:

```bash
cd path/to/your/project/folder
```

---

### 3. Create a virtual environment

This step is optional, but recommended.

#### Windows

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

### 4. Install the required libraries

Run this command inside the project folder:

```bash
pip install -r requirements.txt
```

If that does not work, try:

```bash
python -m pip install -r requirements.txt
```

On macOS/Linux, you may need:

```bash
python3 -m pip install -r requirements.txt
```

---

## Run Instructions

After installing the required libraries, run the game with:

### Windows

```bash
python main.py
```

### macOS/Linux

```bash
python3 main.py
```

The Pygame window should open and show the Connect 4 main menu.

---

## How to Play

1. Start the game by running `main.py`.
2. Choose a difficulty from the main menu.
3. Click a column to drop your piece.
4. The player uses red pieces.
5. The AI uses yellow pieces.
6. The first player to connect four pieces wins.

You can win horizontally, vertically, or diagonally.

---

## Controls

| Control | Action |
|---|---|
| Mouse click | Drop a piece into a column |
| P | Pause or resume the game |
| Esc | Pause or resume the game |
| Resume button | Continue the current game |
| Main Menu button | Return to the main menu |
| Exit Game button | Close the game |
| Play Again button | Restart after a game ends |

---

## AI Difficulty

### Easy

The AI chooses a random valid column.

### Medium

The AI uses minimax with a lower search depth.

### Hard

The AI uses minimax with a deeper search depth, making it harder to beat.

The AI also checks for immediate winning moves and blocks the player if the player is about to win.

---

## Project File Overview

### `connect4.py`

Contains the main Connect 4 game logic, including:

- Creating the board
- Checking valid moves
- Dropping pieces
- Checking for wins
- Checking if the board is full
- Finding where a piece would land
- Returning winning cells for highlighting

### `ai.py`

Contains the AI logic, including:

- Board scoring
- Minimax search
- Alpha-beta pruning
- Immediate win detection
- Blocking the player’s winning move
- Difficulty-based move selection

### `main.py`

Contains the Pygame interface, including:

- Drawing the board
- Drawing menus and buttons
- Handling mouse input
- Handling pause controls
- Drawing the hover preview
- Animating falling pieces
- Managing player and AI turns

### `requirements.txt`

Lists the external libraries needed to run the project.

---

## Troubleshooting

### Pygame is not installed

If you see this error:

```bash
ModuleNotFoundError: No module named 'pygame'
```

Run:

```bash
pip install -r requirements.txt
```

or:

```bash
python -m pip install -r requirements.txt
```

---

### The game does not open

Make sure you are running the command from the same folder as `main.py`.

Use:

```bash
python main.py
```

or:

```bash
python3 main.py
```

---

### The window opens and closes immediately

Run the game from the terminal instead of double-clicking `main.py`. This allows you to see any error messages.

---

## Notes

The project is separated into three main parts:

- `connect4.py` handles the game rules.
- `ai.py` handles the AI decision-making.
- `main.py` handles the Pygame window, drawing, input, menus, and animations.

This structure makes the game easier to update and maintain.