#########################################
# Programmer: Daniel Haber
# Date: 23/4/2018
# File Name: Sanke Game
# Description: eat as many apples with snake in limited amount of time
#########################################

import random
import pygame
pygame.init()

from math import sqrt

HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("Gucci Snakes.png")
background = background.convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
intro_picture = pygame.image.load("intro.jpg")
intro_picture = intro_picture.convert_alpha()
intro_picture = pygame.transform.scale(intro_picture, (WIDTH, HEIGHT))
pygame.display.set_caption('GUCCI SNAKE')
eating = pygame.mixer.Sound('Gulp.wav')
coin = pygame.image.load("coin.png")
coin = coin.convert_alpha()
coin = pygame.transform.scale(coin, (30, 30))

WHITE = (255,255,255)
BLACK = (0,  0,  0)
GREEN = (35,150,59)
RED = (173,68,16)
outline=0

#---------------------------------------#
# snake's properties                    #
#---------------------------------------#
BODY_SIZE = 10
HSPEED = 20
VSPEED = 20

appleListX=[i for i in range(20,WIDTH, 20)]
appleListY=[i for i in range(20,HEIGHT, 20)]
apple_x = random.choice(appleListX)
apple_y = random.choice(appleListY)
apple_radius = random.randint(10,15)
appleListX2=[i for i in range(20,WIDTH, 20)]
appleListY2=[i for i in range(20,HEIGHT, 20)]
apple_x2 = random.choice(appleListX2)
apple_y2 = random.choice(appleListY2)
apple_radius2 = random.randint(10,15)

speedX = 0
speedY = -VSPEED
segx = [int(WIDTH/2.)]*3
segy = [HEIGHT//2, HEIGHT//2+VSPEED, HEIGHT//2+2*VSPEED]
counter = 0
speed = 30
extraSeconds = 0

#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
def introScreen():
    screen.blit(intro_picture, (0,0))
    introtext = pygame.font.SysFont("Futura", 60)
    introtext1 = pygame.font.SysFont("Futura", 25)
    text1 = introtext.render("Welcome to Gucci Snake!", 1, WHITE)
    text2 = introtext1.render("Press the space key to begin! Beat the clock to eat the apples!", 1, WHITE)
    text3 = introtext1.render("Avoid the poisonous green apples!", 1, WHITE)
    screen.blit(text1, (50,100))
    screen.blit(text2, (50, 500))
    screen.blit(text3, (200, 550))
    pygame.display.update()

def redraw_screen():
    screen.blit(background, (0,0))
    game_font = pygame.font.SysFont("Andale Mono", 20)
    game_timer = game_font.render("Time: {}".format(seconds), 1, WHITE)
    screen.blit(game_timer, (200,1))
    countertext = game_font.render("Score: {0}".format(counter), 1, WHITE)
    screen.blit(countertext, (0, 0))
    for i in range(len(segx)):
        screen.blit(coin, (segx[i], segy[i]))
    pygame.draw.circle(screen, GREEN, (apple_x2, apple_y2), apple_radius2, outline)
    pygame.draw.circle(screen, RED, (apple_x, apple_y), apple_radius, outline)
    pygame.display.update()

def over():
    screen.fill(BLACK)
    font = pygame.font.SysFont("Andale Mono", 40)
    text = font.render("Game Over!", 1, WHITE)
    text2 = font.render("Apples eaten: {}".format(counter), 1, WHITE)
    screen.blit(text, [200, 200])
    screen.blit(text2, [200, 300])
    pygame.display.update()
                                       
def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)

#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
pygame.mixer.music.load('Tyga - Gucci Snakes.ogg')          #loading game music
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops = -1)

inPlay = 1
while inPlay == 1: 
    introScreen()
    keys = pygame.key.get_pressed()             #press space to begin game
    for event in pygame.event.get():    
        if keys[pygame.K_SPACE]:
            inPlay = 2
            timer = pygame.time.get_ticks()
    pygame.display.update()

while inPlay== 2:
    seconds = 20- round(((pygame.time.get_ticks()-timer)/1000))
    seconds += extraSeconds

# check for events
    pygame.event.get()
    for event in pygame.event.get():    # check for any events
        if event.type == pygame.QUIT:       # If user clicked close
            inPlay = 3               # Flag that we are done so we exit this loop

    keys = pygame.key.get_pressed()
# act upon key events
    if keys[pygame.K_LEFT] and speedX != HSPEED:
        speedX = -HSPEED
        speedY = 0
    elif keys[pygame.K_RIGHT] and speedX != -HSPEED:
        speedX = HSPEED
        speedY = 0
    elif keys[pygame.K_UP] and speedY != VSPEED:
        speedX = 0
        speedY = -VSPEED
    elif keys[pygame.K_DOWN] and speedY != -VSPEED:
        speedX = 0
        speedY = VSPEED
  
    if distance(segx[0]+15, segy[0]+15, apple_x, apple_y) <= apple_radius+10:
        counter += 1
        eating.play()
        apple_x = random.choice(appleListX)
        apple_y = random.choice(appleListY)
        apple_radius = random.randint(10, 15)
        segx.append(segx[-1])         
        segy.append(segy[-1])
        extraSeconds += 5
    if counter == 6 or counter//6== int:
        speed -=1
    if distance(segx[0], segy[0], apple_x2, apple_y2) <= apple_radius2+10:
        apple_x2 = random.choice(appleListX2)
        apple_y2 = random.choice(appleListY2)
        apple_radius2 = random.randint(10, 15)
        segx.pop()
        segy.pop()

    if segx[0] < 0 or segx[0] > WIDTH or segy[0] < 0 or segy[0] > HEIGHT or len(segx) < 2 or seconds <= 0:
        inPlay = 3
                                        #game is over if these if statements happen

# move all segments
    for i in range(len(segx)-1,0,-1):   # start from the tail, and go backwards:
        segx[i]=segx[i-1]               # every segment takes the coordinates
        segy[i]=segy[i-1]               # of the previous one
# move the head
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY
# update the screen
    if inPlay == 2:
        redraw_screen()
        pygame.time.delay(speed)
        seconds -= 0.001*speed
    if inPlay == 3:
        over()
        pygame.mixer.music.stop()
    #pygame.time.delay(3000)
    #pygame.quit()                           # always quit pygame when done!

#submitted late because of computer issues
# commented pygame.quit() to show game over screen
