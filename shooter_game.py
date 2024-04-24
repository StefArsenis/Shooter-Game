#Create your own shooter
print('Hello World')
from pygame import *
from random import randint
#create game window
window = display.set_mode((1280, 720))
#set scene background
clock = time.Clock()
FPS = 240
volume_sound = 0.5


#creat 2 sprites and place them on the scene
background = transform.scale(image.load('galaxy.jpg'), (1280, 720))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (100, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bull = sprite.Group()


class Spaceship(GameSprite):
    def movement(self):
        pres = key.get_pressed()
        if pres[K_LEFT]:
            self.rect.x -= 10

        if pres[K_RIGHT]:
            self.rect.x += 10

    def fire(self):
        bullets = Bullet('bullet.png', self.rect.x, 400, 10)
        bull.add(bullets)


class Ufooo(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 680:
            self.rect.y = 0
            self.rect.x = randint(0, 1280)


uf0 = sprite.Group()
for i in range(1, 10):
    ufo = Ufooo('ufo.png', randint(0, 550), 0, randint(5, 30))
    uf0.add(ufo)



class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

rocket = Spaceship('rocket.png', 100, 400, 10)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(volume_sound)
mixer.music.play()

score = 0
font.init()
font1 = font.SysFont('Arial', 40) 
missed = 0
win = font1.render('Score' + str(score), True, (255, 255, 255))





game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    key1 = key.get_pressed()

    if key1[K_u] and volume_sound < 1:
        print(volume_sound)
        volume_sound += 0.01
        mixer.music.set_volume(volume_sound)
        mixer.music.play()
    
    elif key1[K_d] and volume_sound > 0:
        print(volume_sound)
        volume_sound -= 0.01
        mixer.music.set_volume(volume_sound)
        mixer.music.play()

    collide = sprite.groupcollide(uf0, bull, True, True)
    for i in collide:
        score += 1
        ufo = Ufooo('ufo.png', randint(0, 650), 0, 6)
        uf0.add(ufo)
    window.blit(background, (0, 0))

    scr = font1.render('Score' + str(score), True, (255, 255, 255))
    window.blit(scr, (10, 20))

    miss = font1.render("Missed" + str(missed), True, (255, 255, 255))
    window.blit(miss, (10, 40))

    if sprite.spritecollide(rocket, uf0,  False) or missed > 3:
        finish = True
        window.blit(win, (200, 200))

    
    window.blit(background, (0, 0))
    uf0.draw(window)
    uf0.update()
    rocket.reset()
    rocket.movement()
    bull.draw(window)
    bull.update()
    clock.tick(FPS)
    display.update()