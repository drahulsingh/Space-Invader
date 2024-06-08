import math
import random
import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('background.png')

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player properties
player_img = pygame.image.load('player.png')
player_x = 370
player_y = 480
player_x_change = 0

# Enemy properties
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for _ in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# Bullet properties
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"  # "ready" - bullet is not visible, "fire" - bullet is moving

# Score properties
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
score_x = 10
score_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
restart_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    restart_text = restart_font.render("Play Again", True, (255, 255, 255))
    screen.blit(restart_text, (330, 350))

def draw_player(x, y):
    screen.blit(player_img, (x, y))

def draw_enemy(x, y, index):
    screen.blit(enemy_img[index], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
    return distance < 27

def restart_game():
    global player_x, player_y, player_x_change, bullet_x, bullet_y, bullet_state, score_value
    player_x = 370
    player_y = 480
    player_x_change = 0
    bullet_x = 0
    bullet_y = 480
    bullet_state = "ready"
    score_value = 0
    for i in range(num_of_enemies):
        enemy_x[i] = random.randint(0, 736)
        enemy_y[i] = random.randint(50, 150)

# Main game loop
running = True
game_over = False
while running:
    screen.fill((0, 0, 0))  # RGB background fill
    screen.blit(background, (0, 0))  # Draw background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_x, mouse_y = event.pos
            if 330 <= mouse_x <= 470 and 350 <= mouse_y <= 390:
                game_over = False
                restart_game()

    if not game_over:
        player_x += player_x_change
        player_x = max(0, min(player_x, 736))

        for i in range(num_of_enemies):
            if enemy_y[i] > 440:
                for j in range(num_of_enemies):
                    enemy_y[j] = 2000
                game_over = True
                break

            enemy_x[i] += enemy_x_change[i]
            if enemy_x[i] <= 0:
                enemy_x_change[i] = 4
                enemy_y[i] += enemy_y_change[i]
            elif enemy_x[i] >= 736:
                enemy_x_change[i] = -4
                enemy_y[i] += enemy_y_change[i]

            if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 1
                enemy_x[i] = random.randint(0, 736)
                enemy_y[i] = random.randint(50, 150)

            draw_enemy(enemy_x[i], enemy_y[i], i)

        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        draw_player(player_x, player_y)
        show_score(score_x, score_y)
    else:
        game_over_text()

    pygame.display.update()
