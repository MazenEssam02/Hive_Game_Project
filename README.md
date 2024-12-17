# Hive_Game_Project

Welcome to the Hive Game Project! This project is an implementation of the Hive board game using Python and Pygame.

## Installation

### From Source

1. Clone the repository:
    ```sh
    git clone https://github.com/MazenEssam02/Hive_Game_Project.git
    cd Hive_Game_Project
    ```

2. Install the required dependency:
    ```sh
    pip install pygame
    ```

3. Run the game:
    ```sh
    python game.py
    ```

### From Release

1. Download the latest release from the [Releases](https://github.com/MazenEssam02/Hive_Game_Project/releases) page.

2. Extract the downloaded zip file.

3. Navigate to the extracted folder.

4. Run the executable:
    ```sh
    ./HIVE.exe  # On Windows, double-click `HIVE.exe`
    ```

## User Manual

To start the game from source, run the following command:
```sh
python game.py
```
 The game supports:
 1. Human vs Human
 2. Human vs Computer
 3. Computer vs Computer modes.

If you choose to play against computer you can choose one of the 3 supported levels of difficulty:
1. easy (human likely to win)
2. medium (Fair game)
3. Hard (Computer likely to win)
   

## Game Rules
To find out the game rules you can visit:
https://www.ultraboardgames.com/hive/game-rules.php

## AI implementation 

The AI uses the Minimax algorithm with alpha-beta pruning and iterative deepening to determine the best move. The evaluation function considers several factors, including:

- Surrounding the opponent's Queen Bee
- Piece count
- Move count
- Piece value
- Distance to the opponent's Queen Bee

## Contributers
- 2001492	Mohanad Ahmed
- 2000106	Tasnim Ahmed Salah
- 2001490	Hana Salah
- 2000467	Zainab Galal
- 2000122	Youssef Mohammed
- 2001607	Mazen Essam Eldin Helmy
- 2000073	George Geham William
- 2000362	Sara Ahmed Mostafa 
- 2001453	Nourhan Ahmed Adelrahman
