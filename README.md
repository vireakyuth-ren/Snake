1. Project Title : Python Snake Game
2. Project Issue / Problem to Be Solved

The project addresses creating a classic Snake game with enhanced features such as:

A high score system to encourage competitive play.

Visual improvements with custom assets and sound effects.

Efficient database integration to store and retrieve high scores.

3. Current Progress (PDLC: Problem Analysis, Design, etc.)

Problem Analysis: The game implements the classic Snake mechanics with added features like big food, a dynamic scoreboard, and sound effects.

Design:

UI: Custom assets for snake parts, food items, and backgrounds.

Sound Effects: Different sounds for actions like eating food, big food, and game over.

High Score System: SQLite database to store player scores.

Implementation: Fully functional Python code with gameplay mechanics, asset integration, and database management.

4. Project Functions/Features

Gameplay:

Snake movement controlled by arrow keys.

Food spawning with point increment for each consumption.

Special “big food” spawning for bonus points every 5 regular food.

Game over condition if the snake collides with itself or the walls.

High Score System:

Top 3 high scores are stored and displayed using SQLite.

Input prompt for player name when beating a high score.

Menu System:

Option to start the game or exit.

Display of high scores below menu options.

Audio and Visuals:

Background music and sound effects for game actions.

Custom-designed graphics for snake parts and food items.

5. Expected No. of Pages (Screens)

Home/Menu Page: Includes Start Game, Exit, and High Scores display.

Gameplay Screen: Displays the game environment and current score.

Game Over Screen: Allows input for name if a high score is achieved.

6. Database Applied

SQLite database (highscore.db):

Table: highscore

Fields:

score (INTEGER): Player’s score.

name (TEXT): Player’s name.

Functionality:

Insert new high scores.

Update scores if they replace lower scores in the top 3.

Retrieve and display top 3 high scores.

7. Project Reference/Source

Code Development: Developed from scratch with Python and Pygame library. Link


Asset Sources: Custom images and sounds used for gameplay. Snake body parts and grass from Link.

Tutorial References: Pygame official documentation and SQLite integration tutorials. Pygame Documentation, SQLite Documentation


Required modules: pygame

Install pygame by running: pip install pygame

