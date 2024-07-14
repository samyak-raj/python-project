import pygame
import random
import math
from pygame import mixer

#initializing pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load("project/Space_Invader/background.jpg")

#background sound
mixer.music.load("project/Space_Invader/background.wav")
mixer.music.play(-1)

#Title and icon
pygame.display.set_caption("Space Invaders")

#Player
playerImg = pygame.image.load("project/Space_Invader/spaceship.png")
playerX = 370
playerY = 480
playerX_change = 0

#Enemy
enemyImg =[]
enemyX = []
enemyY = []
enemyX_change =[]
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("project/Space_Invader/alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.7)
    enemyY_change.append(40)

#bullet
#Ready -[]> you can't see the bullet on the screen
#Fire -> The bullet is currently moving
bulletImg = pygame.image.load("project/Space_Invader/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255 ,255))
    screen.blit(score, (x, y))

#Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (220, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    else: 
        return False

#Game loop
running = True

while running:
    
    #background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #if keystr  oke is pressed check whether it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -0.6
                
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 0.6
            
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("project/Space_Invader/laser.wav")
                    bullet_sound.play()
                    #get the x coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    # checking boundaries of spaceship so it doesn't go out of bounds
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):
        #Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] =2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.7
            enemyY[i] += enemyY_change[i]

        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.7
            enemyY[i] += enemyY_change[i]
        
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("project/Space_Invader/explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
        
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)
        
     #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()