import pygame
import sys
import random
import sqlite3


# Start game
pygame.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
SPEED = 10
BIG_FOOD_SIZE = BLOCK_SIZE * 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (29, 105, 21)
YELLOW = (186, 174, 67)
PINK = (255, 105, 180)

# Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

#SOUND 
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
eat_sound.play()

pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust volume




def add_name_column():
    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()
    # Add a new column to the existing table
    try:
        c.execute("ALTER TABLE highscore ADD COLUMN name TEXT")
    except sqlite3.OperationalError:
        # This error occurs if the column already exists
        pass
    conn.commit()
    conn.close()
add_name_column()

def add_to_database(score):
    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS highscore (score INTEGER, name TEXT)")
    highscore = c.execute("SELECT MAX(score) FROM highscore").fetchone()
    if highscore[0] is None or score > highscore[0]:
        name = input("Enter your name: ")
        c.execute("INSERT INTO highscore (score, name) VALUES (?, ?)", (score, name))
        conn.commit()
    conn.close()

def get_high_scores():
    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()
    c.execute("SELECT score, name FROM highscore ORDER BY score DESC LIMIT 3")
    
    high_scores = c.fetchall()
    conn.close()
    return high_scores

def show_high_scores():
    high_scores = get_high_scores()
    y_offset = HEIGHT // 2 + 130
    if not high_scores:
        no_scores_text = font.render("No high scores yet", True, WHITE)
        screen.blit(no_scores_text, (WIDTH // 2 - no_scores_text.get_width() // 2, y_offset))
        return
    for idx, (score, name) in enumerate(high_scores):
        score_text = font.render(f"{idx + 1}). {name}: {score}points", True, GREEN)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, y_offset))
        y_offset += 30

def show_menu():
    while True:
        screen.fill(BLACK)
        title_text = font.render("Snake Game", True, RED)
        start_text = font.render("Press ENTER to Start", True, WHITE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)
        highscore_title = font.render("High Scores", True, PINK)

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 50))

        # Show high scores below menu
        screen.blit(highscore_title, (WIDTH // 2 - highscore_title.get_width() // 2, HEIGHT // 2 + 100))
        show_high_scores()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start
                    return
                elif event.key == pygame.K_ESCAPE:  # Exit
                    pygame.quit()
                    sys.exit()

def reset_game():
    return [(300, 240), (280, 240), (260, 240)], (400, 300), (1, 0), 0, None

        # Drawing
def drawing():
        screen.fill(BLACK)
        for i, pos in enumerate(snake):
            if i == 0:
                pygame.draw.rect(screen, GREEN2, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
                eye_offset = BLOCK_SIZE // 4
                eye_size = BLOCK_SIZE // 5
                left_eye = (pos[0] + eye_offset, pos[1] + eye_offset)
                right_eye = (pos[0] + BLOCK_SIZE - eye_offset - eye_size, pos[1] + eye_offset)
                pygame.draw.circle(screen, YELLOW, left_eye, eye_size)
                pygame.draw.circle(screen, YELLOW, right_eye, eye_size)
            else:
                pygame.draw.rect(screen, GREEN2, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))

        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        if big_food is not None:
            pygame.draw.rect(screen, GREEN, (big_food[0], big_food[1], BIG_FOOD_SIZE, BIG_FOOD_SIZE))

        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        pygame.time.delay(1000 // SPEED)

while True:
    show_menu()
    # Game variables
    snake, food, direction, score, big_food = reset_game()
    
    while True:
        pygame.mixer.music.play(-1) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # Snake movement
        head = snake[0]
        new_head = (head[0] + direction[0] * BLOCK_SIZE, head[1] + direction[1] * BLOCK_SIZE)
        snake.insert(0, new_head)

        # Food collision
        if snake[0] == food:
            score += 1
            food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                    random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
            if score % 5 == 0 and big_food is None:
                big_food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                            random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
        else:
            snake.pop()

        # Big food collision
        if big_food is not None and (big_food[0] <= snake[0][0] < big_food[0] + BIG_FOOD_SIZE and
                                     big_food[1] <= snake[0][1] < big_food[1] + BIG_FOOD_SIZE):
            score += 5
            big_food = None

        # Collision detection
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:]):
            add_to_database(score)
            break
        drawing()


