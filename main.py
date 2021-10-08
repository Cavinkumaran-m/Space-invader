import pygame
from pygame import *
import sys
import random
from time import *



pygame.init()

x = 400
y = 700
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption('Vin Veli Veeran')

class Ship():

    def __init__(self):

        self.temp = pygame.image.load(r'ship.png')
        self.img = pygame.Surface((40, 40))
        self.img.fill((6, 251, 23))
        self.img.set_colorkey((6, 251, 23))
        self.img.blit(self.temp, (0,0))
        self.rect = pygame.Rect(0, 0, 40, 40)

    def draw(self, x, y):

        screen.blit(self.img, (x, y))
        self.rect = pygame.Rect(x, y, 40, 40)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, img):

        super().__init__()
        self.temp = img
        self.temp = pygame.transform.scale(self.temp, (10, 10))
        self.img = pygame.Surface((10, 10))
        self.img.fill((6, 251, 23))
        self.img.set_colorkey((6, 251, 23))
        self.img.blit(self.temp, (0,0))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.state = True

    def draw(self):

        screen.blit(self.img, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.y -= 2
        if(self.y < 0):
            self.state = False
            
class Alien(pygame.sprite.Sprite):

    def __init__(self, x, y, img):
        
        super().__init__()
        self.temp = img
        self.temp = pygame.transform.scale(self.temp, (40, 40))
        self.img = pygame.Surface((40, 40))
        self.img.fill((6, 251, 23))
        self.img.set_colorkey((6, 251, 23))
        self.img.blit(self.temp, (0,0))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.state = True

    def draw(self):

        screen.blit(self.img, (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.y += 2
        if(self.y > 700):
            self.state = False

class Timer():

    def __init__(self, duration):

        self.start = pygame.time.get_ticks()
        self.end = 0
        self.time = 0
        self.duration = duration

    def count(self):

        self.end = pygame.time.get_ticks()
        self.time = self.end - self.start
        if (self.time > self.duration):
            self.start = pygame.time.get_ticks()
            return True
        else:
            return False
        
        
#Objects
ship = Ship()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullet_img = pygame.image.load(r'bullet.png')
alien_img = pygame.image.load(r'alien.png')
font = pygame.font.Font("freesansbold.ttf", 22)
lives = 3
bullets_count = 10
reloading_label = font.render("Reloading", True, (255,255, 255))

FPS = 90
fpsclock = pygame.time.Clock()
pygame.mouse.set_visible(False)
clock = Timer(2000)
Game_over = False
reloaded = False


while(not Game_over):
    
    fpsclock.tick(FPS)
    screen.fill((0,0,0))
    lives_label = font.render("Lives : X {}".format(lives), True, (240,255, 255))
    bullets_label = font.render("Shells : {}".format(bullets_count), True, (255,255, 255))
    screen.blit(lives_label, (10, 670))

    if(lives < 1): 
        screen.fill((0,0,0))
        lives_label = font.render("Game Over", True, (240,255, 255))
        screen.blit(lives_label, (140, 340))
        pygame.display.update()
        sleep(5)
        pygame.quit()
        sys.exit()

    def bullet_():
        global bullets_count, reloaded, reload_timer
        if(bullets_count > 0):
            screen.blit(bullets_label, (280, 670))
        else:
            screen.blit(reloading_label, (280, 670))
            if(reloaded == False):
                reload_timer = Timer(3000)
                reloaded = True
            if(reload_timer.count()):
                reloaded = False
                bullets_count = 10
                
    bullet_()
    a, b = pygame.mouse.get_pos()
    x, y = a-5, b-5

    #draw_bullets
    for i in bullets:
        if(i.state):
            i.draw()
        else:
            bullets.remove(i)

    #draw_aliens
    for j in aliens:
        if(j.state):
            j.draw()
        else:
            aliens.remove(j)
    if(clock.count()):
        alien_x = random.randint(0, 360)
        alien = Alien(alien_x, 0, alien_img)
        aliens.add(alien)

    #collision_checker
    for k in aliens:
        if k.rect.colliderect(ship.rect):
            aliens.remove(k)
            lives -= 1
            
        for l in bullets:
            if k.rect.colliderect(l.rect):
                aliens.remove(k)
                bullets.remove(l)
                break

    
    #checks for input
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if(reloaded != True):
                bullets_count -= 1
                bullet = Bullet(x, y, bullet_img)
                bullets.add(bullet)

    #draws_player
    x -= 15
    y -= 15
    ship.draw(x, y)
    
    pygame.display.update()
    
