import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# ekran 
screen = pygame.display.set_mode((800, 600))

# arkaplan
background = pygame.image.load('background.png')

# arkaplan sesi
mixer.music.load("background.wav")
mixer.music.play(-1)

# caption ve ikon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('space.png')
pygame.display.set_icon(icon)

# oyuncu
playerImg = pygame.image.load('space-invaders(2).png')
playerX = 370
playerY = 480
playerX_change = 0

# düşman
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# hızlı düşman
fast_enemyImg = []
fast_enemyX = []
fast_enemyY = []
fast_enemyX_change = []
fast_enemyY_change = []
num_of_fast_enemies = 2

for i in range(num_of_fast_enemies):
    fast_enemyImg.append(pygame.image.load('fast_alien.png'))
    fast_enemyX.append(random.randint(0, 736))
    fast_enemyY.append(random.randint(50, 150))
    fast_enemyX_change.append(5)
    fast_enemyY_change.append(40)

# mermi

# Ready - daha ateş falan edilmedi
# Fire - mermi ateş edilmeye hazır durumda

bulletImg = pygame.image.load('bullet(1).png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fast_enemy(x, y, i):
    screen.blit(fast_enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# oyun döngüsü
running = True
while running:

    # RGB şeklinde
    screen.fill((0, 0, 0))
    # arkaplan resmi
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # sağa solan hareket kısmı 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # düşman hareketi
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # fast enemy kısmı hareket ve çarpışması
    for i in range(num_of_fast_enemies):

        # game over olan kısım
        if fast_enemyY[i] > 440:
            for j in range(num_of_fast_enemies):
                fast_enemyY[j] = 2000
            game_over_text()
            break

        fast_enemyX[i] += fast_enemyX_change[i]
        if fast_enemyX[i] <= 0:
            fast_enemyX_change[i] = 5
            fast_enemyY[i] += fast_enemyY_change[i]
        elif fast_enemyX[i] >= 736:
            fast_enemyX_change[i] = -5
            fast_enemyY[i] += fast_enemyY_change[i]

        # çarpışma
        collision = isCollision(fast_enemyX[i], fast_enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 2
            fast_enemyX[i] = random.randint(0, 736)
            fast_enemyY[i] = random.randint(50, 150)
        fast_enemy(fast_enemyX[i], fast_enemyY[i], i)

    # mermi hareketi
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
