# Connect 4 - AI with Alpha-Beta Pruning

This project is a Connect 4 game built with Python and Pygame. The player plays against an AI opponent that uses Minimax with Alpha-Beta Pruning to make strategic moves.

---

## Setup Instructions

### 1. Install Python

Make sure Python 3.10 or newer is installed on your computer.

To check your Python version, run:

```bash
python --version
```

On macOS or Linux, you may need to use:

```bash
python3 --version
```

---

### 2. Open the Project Folder

Make sure all project files are in the same folder.

The project folder should include these files:

```text
main.py
game_app.py
connect4.py
ai.py
renderer.py
ui_config.py
requirements.txt
README.md
```

Open a terminal inside the project folder.

Example on Windows:

```bash
cd "C:\Users\YourName\Desktop\Connect4Project"
```

Example on macOS/Linux:

```bash
cd path/to/Connect4Project
```

---

### 3. Create a Virtual Environment

This step is recommended because it keeps the project libraries separate from the rest of your computer.

#### Windows

Create the virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

#### macOS/Linux

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

---

### 4. Install Required Libraries

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

After the setup is complete, run the game with:

### Windows

```bash
python main.py
```

### macOS/Linux

```bash
python3 main.py
```

A Pygame window should open and display the Connect 4 main menu.

---

## How to Play

1. Choose a difficulty from the main menu.
2. Click a column to drop your piece.
3. The AI will make its move after your turn.
4. The first player to connect four pieces wins.
5. A win can happen horizontally, vertically, or diagonally.

---

## Controls

| Control | Action |
|---|---|
| Mouse click | Drop a piece into a column |
| P | Pause or resume the game |
| Esc | Pause or resume the game |
| Resume | Continue the current game |
| Main Menu | Return to the main menu |
| Exit Game | Close the game |
| Play Again | Restart after a game ends |

---

## Difficulty Options

| Difficulty | Description |
|---|---|
| Easy | AI chooses a random valid move |
| Medium | AI uses Minimax with a smaller search depth |
| Hard | AI uses Minimax with a deeper search depth |

The AI also checks for immediate winning moves and blocks the player when the player is about to win.

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

If that does not work, try:

```bash
python -m pip install -r requirements.txt
```

On macOS/Linux, you may need:

```bash
python3 -m pip install -r requirements.txt
```

---

### The game does not open

Make sure you are inside the same folder as `main.py`.

Then run:

```bash
python main.py
```

or:

```bash
python3 main.py
```

---

### The window opens and closes immediately

Run the game from the terminal instead of double-clicking `main.py`.

This allows you to see any error message that appears.