from pygame import *
from main import *

screen = pygame.display.set_mode(DISPLAY)  # Створюємо вікно
display.set_icon(pygame.image.load("images/icon/icon.png"))
pygame.display.set_caption("Paw of the Abyss")  # Заголовок вікна


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        sprite.Sprite.__init__(self)
        self.image_normal = transform.scale(image.load(player_image), (size_x, size_y))
        self.image = self.image_normal
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x  = size_x
        self.size_y = size_y
        self.counter = 0

    def update(self, mouse_pos, player_image_hover, size_x, size_y):
        if self.rect.collidepoint(mouse_pos):
            self.image_hover = transform.scale(image.load(player_image_hover), (size_x, size_y))
            self.image = self.image_hover
        else:
            self.image = self.image_normal

    def gif(self):
        self.counter += 1
        n = 50
        if 0 <= self.counter < n:
            self.image = transform.scale(image.load('images/comics/1.jpg'), (self.size_x, self.size_y))
        elif n*2 <= self.counter < n*3:
            self.image = transform.scale(image.load('images/comics/2.jpg'), (self.size_x, self.size_y))
        elif n*4 <= self.counter < n*5:
            self.image = transform.scale(image.load('images/comics/3.jpg'), (self.size_x, self.size_y))
        elif n*6 <= self.counter < n*7:
            self.image = transform.scale(image.load('images/comics/4.jpg'), (self.size_x, self.size_y))
        elif n*8 <= self.counter < n*9:
            self.image = transform.scale(image.load('images/comics/5.jpg'), (self.size_x, self.size_y))
        elif n*10 <= self.counter < n*11:
            self.image = transform.scale(image.load('images/comics/6.jpg'), (self.size_x, self.size_y))
        elif n*12 <= self.counter < n*13:
            self.image = transform.scale(image.load('images/comics/7.jpg'), (self.size_x, self.size_y))
        elif n*14 <= self.counter < n*15:
            self.image = transform.scale(image.load('images/comics/8.jpg'), (self.size_x, self.size_y))
        elif n*16 <= self.counter < n*17:
            self.image = transform.scale(image.load('images/comics/9.jpg'), (self.size_x, self.size_y))

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
