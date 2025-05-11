from pygame import *
import pyganim
import os
from random import randint

MOVE_SPEED = 7
WIDTH = 50
HEIGHT = 50
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Гравітация
ANIMATION_DELAY = 0.1 # Швидкість зміни кадрів

ANIMATION_RIGHT = [('images/player/r1.png'),
                   ('images/player/r2.png'),
                   ('images/player/r3.png')]
ANIMATION_LEFT = [('images/player/l1.png'),
                  ('images/player/l2.png'),
                  ('images/player/l3.png')]
ANIMATION_JUMP_LEFT = [('images/player/jl.png', 0.1)]
ANIMATION_JUMP_RIGHT = [('images/player/jr.png', 0.1)]
ANIMATION_JUMP = [('images/player/j.png', 0.1)]
ANIMATION_STAY = [('images/player/0.png', 0.1)]

class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # Швидкість переміщення. 0 - стояти на місці
        self.startX = x  # Початкова позиція X
        self.startY = y  # Початкова позиція Y
        self.yvel = 0  # Швидкість вертикального переміщення
        self.onGround = False  # Чи знаходжуся я на землі
        self.score = 0 # Скільки монет гравець зібрав
        self.ex = False # Чи
        self.death = False
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямокутний об'єкт
        self.image.set_colorkey(Color(COLOR))  # робимо фон прозорим
        # Анімація руху вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        # Анімація руху вліво
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        
        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0)) # За замовчуванням стоїмо
        # Анімація стрибка вліво
        self.boltAnimJumpLeft= pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()
        # Анімація стрибка вправо
        self.boltAnimJumpRight= pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()
        # Анімація стрибка
        self.boltAnimJump= pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()


    def update(self, left, right, up, platforms, crystals, exits, spikes):
        
        if up:
            if self.onGround: # стрибаємо, тільки якщо торкнулися землі
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED # Ліво = x- n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
 
        if right:
            self.xvel = MOVE_SPEED # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
         
        if not(left or right): # Просто стоїмо
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
            
        if not self.onGround:
            self.yvel += GRAVITY
            
        self.onGround = False
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, crystals, exits, spikes)

        self.rect.x += self.xvel # переносимо своє положення на xvel
        self.collide(self.xvel, 0, platforms, crystals, exits, spikes)

    def collide(self, xvel, yvel, platforms, crystals, exits, spikes):
        for p in platforms:
            if sprite.collide_rect(self, p):  # Перевірка зіткнення з платформою

                if xvel > 0:  # Рух вправо
                    self.rect.right = p.rect.left

                if xvel < 0:  # Рух вліво
                    self.rect.left = p.rect.right

                if yvel > 0:  # Падіння вниз
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:  # Рух вгору
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

        hit_crystals = sprite.spritecollide(self, crystals, True)  # Автоматично видаляє уламків, що торкнулися гравця
        if hit_crystals:
            self.score += len(hit_crystals)  # Додаємо кількість зібраних уламків до очок
            mixer.Sound("images/music/coin.wav").play()

        for e in exits:
            if sprite.collide_rect(self, e):
                if xvel > 0:  # Рух вправо
                    self.rect.right = e.rect.left

                if xvel < 0:  # Рух вліво
                    self.rect.left = e.rect.right

                if yvel > 0:  # Падіння вниз
                    self.rect.bottom = e.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:  # Рух вгору
                    self.rect.top = e.rect.bottom
                    self.yvel = 0

                if self.score >= 5:
                    self.ex = True

        for s in spikes:
            if sprite.collide_rect(self, s):
                self.death = True
