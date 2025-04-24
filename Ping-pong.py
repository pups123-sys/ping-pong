from pygame import *
from random import choice

# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
WIN_W = 700
WIN_H = 500
FPS = 60
step = 4
size  = 100
GREY = (100,100,100)
BLUE = (76,249,255)
font.init()
title_font = font.SysFont('papyrus' , 70)

left_lost = title_font.render('Левый игрок проиграл (лооох)' ,True , BLUE)

right_lost = title_font.render('Правый игрок проиграл (лооох)' ,True , BLUE)

# создание окна размером 700 на 500
window = display.set_mode((WIN_W, WIN_H))

# название окна
display.set_caption("пинг-понг")
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            # здесь - размеры картинки
            (w, h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Playr(GameSprite):
    def __init__(self, img, x, y, w, h , speed = step):
        super().__init__(img, x, y, w, h )
        self.speed = speed 
        
    def update(self , up , down)  :
        key_pressed = key.get_pressed()

        if key_pressed[up] and self.rect.y > 5:
            self.rect.y -= step

        if key_pressed[down] and self.rect.bottom < WIN_H-5:
            self.rect.y += step

class Ball(GameSprite):
    def __init__(self, img, x, y, w, h , speed = step, speed_x = step, speed_y = step ):
        super().__init__(img, x, y, w, h )
        self.speed = speed
        self.speed_x = speed*choice([-1,1])
        self.speed_y = speed*choice([-1,1])
    
    def update( self ):
        if self.rect.x <= 0 or self.rect.x >= WIN_W - self.rect.width :
            self.speed_x *=-1
        self.rect.x += self.speed_x

        if self.rect.y <= 0 or self.rect.y >= WIN_H - self.rect.height :
            self.speed_y *=-1
        self.rect.y += self.speed_y

        

rkn1 = Playr('RKN.png',0 ,0 ,40 ,size*2 )

rkn2 = Playr('RKN.png',660 ,0 ,40 ,size*2 )

discord = Ball('Discord.png',300 ,200 , size,size)

game = True
finish = False
while game:
    for e in event.get():
    # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False
    if not finish:
        window.fill(GREY)

        rkn1.draw(window)
        rkn2.draw(window)

        discord.draw(window)
        discord.update()

        rkn1.update(K_w , K_s)
        rkn2.update(K_UP , K_DOWN)

        if sprite.collide_rect(discord , rkn1):
            discord.speed_x *=-1
            discord.rect.x += discord.speed_x

            discord.speed_y *=-1
            discord.rect.y += discord.speed_y

        if sprite.collide_rect(discord , rkn2):
            discord.speed_x *=-1
            discord.rect.x += discord.speed_x

            discord.speed_y *=-1
            discord.rect.y += discord.speed_y

        if discord.rect.x <=0 :
            window.blit( left_lost, (200, 200))
            finish = True

        if discord.rect.x >= WIN_W - discord.rect.width :
            window.blit( right_lost, (200, 200))
            finish = True
    else:
        discord.kill()
        #не накаркать бы)
        time.delay(3000)

        discord = Ball('Discord.png',300 ,200 , size,size)

        finish = False

    display.update()
    clock.tick(FPS)
