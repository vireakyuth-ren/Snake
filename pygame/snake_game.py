import pygame
import sys
import random
import sqlite3


#start
pygame.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
SPEED = 10
BIG_FOOD_SIZE = BLOCK_SIZE * 2

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN2 = (29, 105, 21)
YELLOW = (255, 255, 102)
PINK = (255, 105, 180)

#display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

#sound
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("pygame/snake_game/assets/sounds/red.mp3")
big_food_sound = pygame.mixer.Sound("pygame/snake_game/assets/sounds/bigfood.mp3")
game_over_sound = pygame.mixer.Sound("pygame/snake_game/assets/sounds/gameover1.mp3")


pygame.mixer.music.load("pygame/snake_game/assets/sounds/fein.mp3")
pygame.mixer.music.set_volume(0.2)  #adjust volume

#image files
grass = pygame.image.load("pygame/snake_game/assets/images/grass.jpg")
grass = pygame.transform.scale(grass, (BLOCK_SIZE, BLOCK_SIZE))
food_img = pygame.image.load("pygame/snake_game/assets/images/apple.png")
food_img = pygame.transform.scale(food_img, (BLOCK_SIZE, BLOCK_SIZE))
big_food_img = pygame.image.load("pygame/snake_game/assets/images/green_apple.png")
big_food_img = pygame.transform.scale(big_food_img, (BIG_FOOD_SIZE, BIG_FOOD_SIZE))
snake_red_body = pygame.image.load("pygame/snake_game/assets/images/red_body.png")
snake_red_body = pygame.transform.scale(snake_red_body, (BLOCK_SIZE, BLOCK_SIZE))
snake_red_head = pygame.image.load("pygame/snake_game/assets/images/red_head.png")
snake_red_head = pygame.transform.scale(snake_red_head, (BLOCK_SIZE, BLOCK_SIZE))
snake_red_tail = pygame.image.load("pygame/snake_game/assets/images/red_tail.png")
snake_red_tail = pygame.transform.scale(snake_red_tail, (BLOCK_SIZE, BLOCK_SIZE))




def input_name():
    input_active = True
    user_text = ""
    color_inactive = WHITE
    color_active = RED
    color = color_inactive
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 40)

    while input_active:
        screen.fill(BLACK)
        new_best = font.render("New Best!", True, YELLOW)
        prompt_text = font.render("Enter your name:", True, WHITE)
        screen.blit(new_best, (WIDTH // 2 - 100, HEIGHT // 2 - 100))
        screen.blit(prompt_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.draw.rect(screen, color, input_box, 2)

        text_surface = font.render(user_text, True, WHITE)
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 5))
        input_box.w = max(200, text_surface.get_width() + 20)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #press Enter to submit
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:  #handle backspace
                    user_text = user_text[:-1]
                else:  #add the typed character to the text
                    user_text += event.unicode

    return user_text

def add_to_database(score):
    conn = sqlite3.connect('highscore.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS highscore (score INTEGER, name TEXT)")
    high_scores = c.execute("SELECT score, name FROM highscore ORDER BY score DESC").fetchall()
    if len(high_scores) < 3 or score > high_scores[-1][0]:  #if there are less than 3 scores or the new score is higher than the lowest score
        
        name = input_name()
        
        
        if len(high_scores) < 3:
            c.execute("INSERT INTO highscore (score, name) VALUES (?, ?)", (score, name))   #add to db if there arent 3 highscores yet
        else:
            
            lowest_score = high_scores[-1][0]
            if score > lowest_score:
                
                
                for i in range(len(high_scores)):   #find the index of the lowest score
                    if high_scores[i][0] == lowest_score:
                        #replace the lowest score with the new score
                        c.execute("UPDATE highscore SET score = ?, name = ? WHERE score = ? AND name = ?", (score, name, lowest_score, high_scores[i][1]))
                        break
        
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

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 180))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - 80))
        screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 - 20))

        #show high scores below menu
        screen.blit(highscore_title, (WIDTH // 2 - highscore_title.get_width() // 2, HEIGHT // 2 + 40))
        show_high_scores()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  #start
                    return
                elif event.key == pygame.K_ESCAPE:  #exit
                    pygame.quit()
                    sys.exit()

def reset_game():
    return [(300, 240), (280, 240), (260, 240)], (400, 300), (1, 0), 0, None #game variables

        #drawing the game
def draw_grass():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            screen.blit(grass, (x, y))

def drawing():
    draw_grass()


    #draw the food
    screen.blit(food_img, (food[0], food[1]))

    #draw big food if it exists
    if big_food is not None:
        screen.blit(big_food_img, (big_food[0], big_food[1]))

    #draw the main character(snake) and movement logic
    for i, pos in enumerate(snake):
        if i == 0:  #snake head
            if direction == (1, 0):  #moving right
                rotated_head = snake_red_head
            elif direction == (-1, 0):  #moving left
                rotated_head = pygame.transform.rotate(snake_red_head, 180)
            elif direction == (0, -1):  #moving up
                rotated_head = pygame.transform.rotate(snake_red_head, 90)
            elif direction == (0, 1):  #moving down
                rotated_head = pygame.transform.rotate(snake_red_head, 270)

            screen.blit(rotated_head, (pos[0], pos[1]))
        elif i == len(snake) - 1:
            tail_dir = (snake[-2][0] - pos[0], snake[-2][1] - pos[1])
            if tail_dir == (BLOCK_SIZE, 0):
                rotated_tail = snake_red_tail
            elif tail_dir == (-BLOCK_SIZE, 0):
                rotated_tail = pygame.transform.rotate(snake_red_tail, 180)
            elif tail_dir == (0, -BLOCK_SIZE):
                rotated_tail = pygame.transform.rotate(snake_red_tail, 90)
            elif tail_dir == (0, BLOCK_SIZE):
                rotated_tail = pygame.transform.rotate(snake_red_tail, 270)
                
            screen.blit(rotated_tail, pos)
        else:  #snake body
            screen.blit(snake_red_body, (pos[0], pos[1]))
        
        
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    pygame.time.delay(1000 // SPEED)

while True:
    show_menu()
    
    snake, food, direction, score, big_food = reset_game()   #game variables

    pygame.mixer.music.play()
    while True:
        
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

        #snake movement
        head = snake[0]
        new_head = (head[0] + direction[0] * BLOCK_SIZE, head[1] + direction[1] * BLOCK_SIZE)
        snake.insert(0, new_head)

        #food collision
        if snake[0] == food:
            eat_sound.play()
            score += 1
            food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                    random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
            if score % 5 == 0 and big_food is None:
                big_food = (random.randint(0, WIDTH - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE,
                            random.randint(0, HEIGHT - BLOCK_SIZE) // BLOCK_SIZE * BLOCK_SIZE)
        else:
            snake.pop()

        #big food collision
        if big_food is not None and (big_food[0] <= snake[0][0] < big_food[0] + BIG_FOOD_SIZE and
                                     big_food[1] <= snake[0][1] < big_food[1] + BIG_FOOD_SIZE):
            score += 5
            big_food_sound.play()
            big_food = None

        #collision detection
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT or
            snake[0] in snake[1:]):
            game_over_sound.play()
            add_to_database(score)
            break
        drawing()


