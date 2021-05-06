import pygame
import random
import os

pygame.mixer.init()

pygame.init()

# Game Colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

# Screen Resolution
screen_width = 900
screen_height = 600

gameScreen = pygame.display.set_mode((screen_width, screen_height))

bgimg = pygame.image.load("assets\\images\\background.png")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("SNAKE GAME BY ANSHUMAN THAKUR")
pygame.display.update()

# Game's fps
clock = pygame.time.Clock()

# Game's Text font
font = pygame.font.SysFont(None, 55)

# Game Specific Functions


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameScreen.blit(screen_text, [x, y])


def plot_snake(gameScreen, color, snake_list, snake_size):
    for x, y in snake_list:
        pygame.draw.rect(gameScreen, color, [x, y, snake_size, snake_size])


def welcome_screen():
    exit_game = False
    while not exit_game:
        gameScreen.fill((100, 240, 180))
        text_screen("Welcome to the Snake Game", black, 190, 200)
        text_screen("Press Enter to play", black, 273, 240)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        pygame.display.update()
        clock.tick(30)

# Game Loop
def gameloop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 50
    snake_y = 50
    snake_size = 10
    fps = 30
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    score = 0
    snake_length = 1
    snake_list = []
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)

    # Check If highscore.txt File Exist 
    if (not os.path.exists("gamesave\\highscore.txt")):
        with open("gamesave\\highscore.txt", "w") as h:
            h.write("0")

    # Highscore
    with open("gamesave\\highscore.txt", "r") as h:
        highscore = h.read()

    while not exit_game:
        if game_over == True:
            with open("gamesave\\highscore.txt", "w") as h:
                h.write(str(highscore))
            gameScreen.fill(white)
            
            text_screen("Game Over! Please press enter to continue!",
                        black, 50, screen_height/2-60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_a:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_w:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_s:
                        velocity_y = init_velocity
                        velocity_x = 0

            # Score Updation
            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                pygame.mixer.music.load("assets\\sound\\point.mp3")
                pygame.mixer.music.play()
                score += 10
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snake_length += 3
                if score > int(highscore):
                    highscore = score

            snake_x += velocity_x
            snake_y += velocity_y

            gameScreen.fill(white)
            gameScreen.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "  Highscore: " + str(highscore), black, 5, 3)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True
                pygame.mixer.music.load("assets\\sound\\gameover.mp3")
                pygame.mixer.music.play()

            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("assets\\sound\\gameover.mp3")
                pygame.mixer.music.play()

            plot_snake(gameScreen, black, snake_list, snake_size)
            pygame.draw.rect(gameScreen, red, [food_x, food_y, snake_size, snake_size])

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome_screen()
