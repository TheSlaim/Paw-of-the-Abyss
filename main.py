# Імпортуємо бібліотеку pygame
import time

import pygame
from pygame import *
from player import *
from blocks import *
from game_sprite import *
from camera import *

# Оголошуємо змінні
WIN_WIDTH = 800  # Ширина створюваного вікна
WIN_HEIGHT = 640  # Висота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Групуємо ширину і висоту в одну змінну

pygame.font.init()
font = pygame.font.Font(None, 36)  # Розмір тексту 36, стандартний шрифт

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не рухаємося далі лівої межі
    l = max(-(camera.width - WIN_WIDTH), l)  # Не рухаємося далі правої межі
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не рухаємося далі нижньої межі
    t = min(0, t)  # Не рухаємося далі верхньої межі

    return Rect(l, t, w, h)

def fade(screen, width, height): # Затемнення екрану
    fade_surface = Surface((width, height))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        display.update()
        time.delay(30)


def main():
    pygame.init()  # Ініціалізація PyGame, обов’язковий рядок

    game = True

    # Створюємо всі спрайти
    bg = GameSprite("images/blocks/bg.png", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    bg_2 = GameSprite("images/blocks/bg2.png", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    bg_3 = GameSprite("images/blocks/bg3.png", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    bg_the_end = GameSprite("images/blocks/the_end.png", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    bg_menu = GameSprite("images/blocks/bg_menu.png", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    comics = GameSprite("images/comics/1.jpg", 0, 0, WIN_WIDTH, WIN_HEIGHT)
    die = GameSprite("images/Died/died.jpg", 100, 100, 575, 350)
    logo = GameSprite("images/blocks/logo.png", 290, 50, 250, 250)
    btn_play = GameSprite("images/blocks/PLAY.png", 349, 330, 140, 80)
    btn_exit = GameSprite("images/blocks/EXIT.png", 349, 450, 140, 80)
    hero = Player(55, 900)  # Створюємо героя з координатами (x, y)

    left = right = False  # За замовчуванням – стоїмо
    up = False

    entities = pygame.sprite.Group()  # Усі об'єкти
    platforms = []  # Те, у що будемо врізатися або опиратися
    crystals = pygame.sprite.Group()  # Група уламків
    exits = []  # Список виходів
    spikes = []  # Список шипів
    entities.add(hero)

    # Масиви level1, level2 і level3 можна змінювати. Тобто можна зробити будь-який рівень.
    # "-" це платформа, "*" це уламок, " " це нічого, "=" це прохід на наступний рівень, "A" це шип.
    level1 = [
        "-----------------------------------",
        "-                                 =",
        "-                                 =",
        "-                               ---",
        "-                                 -",
        "-                        *        -",
        "-                       --        -",
        "-                                 -",
        "-            --                   -",
        "-*                           --   -",
        "--                                -",
        "-                   ----          -",
        "-                     *      ---  -",
        "-*                                -",
        "--                                -",
        "-            --                   -",
        "-                    ---          -",
        "-                                 -",
        "-                                 -",
        "-                            ---  -",
        "-      ---                        -",
        "-       *                         -",
        "-                                 -",
        "-   -------         ----          -",
        "-                                 -",
        "-                         -       -",
        "-                            --   -",
        "-                                 -",
        "-            AA                   -",
        "-----------------------------------"]

    level2 = [
        "-----------------------------------",
        "-                                 -",
        "-                                 -",
        "-                               ---",
        "-                                 -",
        "-*             ---                -",
        "--                       ---      -",
        "-                                 -",
        "-         --        AA      -     -",
        "-                   --            -",
        "-       A                       ---",
        "-      --                         -",
        "-                         ---     -",
        "--               ---              -",
        "-                                 -",
        "-   *        ---                  -",
        "-  ---                            -",
        "-                               * -",
        "-       ---                  ------",
        "-                                 -",
        "-        A *       --             -",
        "-        ----                     -",
        "-                                 -",
        "-                       --        -",
        "-             ---                 -",
        "-A*                               -",
        "----                 --           -",
        "=                                 -",
        "=       AA                   AAA  -",
        "-----------------------------------"]

    level3 = [
        "-----------------------------------",
        "=                                 -",
        "=                       *A        -",
        "---               --   ---        -",
        "-     --                         *-",
        "-                                --",
        "-*         --                     -",
        "--                                -",
        "-                 A        -      -",
        "-                --               -",
        "-A*                              *-",
        "----                             --",
        "-             --                  -",
        "-                           -     -",
        "-*    --               -          -",
        "--                                -",
        "-                -         A      -",
        "-      A                   ---    -",
        "-      ---                        -",
        "-*                                -",
        "--                                -",
        "-                                --",
        "-                ---              -",
        "-                                 -",
        "-      A                          -",
        "-      ----                 ---   -",
        "-                                 -",
        "-                                 -",
        "-                 -               -",
        "-                                 -",
        "-                                 -",
        "-                       ---       -",
        "-                                 -",
        "-          AA                     -",
        "-----------------------------------"]

    def draw_level(level):
        x = y = 0  # Координати
        for row in level:  # Весь рядок рівня
            for col in row:  # Кожен символ у рядку рівня
                if col == "-":
                    pf = Platform(x, y)  # Створення платформи
                    entities.add(pf)  # Додавання платформи в групу сутностей
                    platforms.append(pf)  # Додавання платформи у список платформ

                x += PLATFORM_WIDTH  # Розміщення блоків платформи на ширині блоків
            y += PLATFORM_HEIGHT  # Те саме для висоти
            x = 0  # Починаємо з нуля на кожному новому рядку

        x = y = 0  # Координати для монет
        for row in level:  # Весь рядок рівня
            for col in row:  # Кожен символ у рядку рівня
                if col == "*":
                    crystal = Сrystal(x, y)  # Створення уламку
                    entities.add(crystal)  # Додавання уламку в групу сутностей
                    crystals.add(crystal)  # Додавання в `pygame.sprite.Group()`

                x += CRYSTAL_WIDTH  # Розміщення уламків на ширині блоків
            y += CRYSTAL_HEIGHT  # Те саме для висоти
            x = 0  # Починаємо з нуля на кожному новому рядку

        x = y = 0  # Координати
        # Цикл для розміщення виходів у рівні
        for row in level:  # Весь рядок
            for col in row:  # Кожен символ
                if col == "=":
                    pf = Exit(x, y)  # Створення виходу
                    entities.add(pf)  # Додавання виходу в групу сутностей
                    exits.append(pf)  # Додавання виходу в список виходів

                x += PLATFORM_WIDTH  # Блоки виходу розміщуються на ширині блоків
            y += PLATFORM_HEIGHT  # Те саме для висоти
            x = 0  # Починаємо з нуля на кожному новому рядку

        x = y = 0  # Координати
        # Цикл для розміщення шипів у рівні
        for row in level:  # Весь рядок
            for col in row:  # Кожен символ
                if col == "A":
                    pf = Spike(x, y)  # Створення шипа
                    entities.add(pf)  # Додавання шипа в групу сутностей
                    spikes.append(pf)  # Додавання шипа в список шипів

                x += PLATFORM_WIDTH  # Блоки шипів розміщуються на ширині блоків
            y += PLATFORM_HEIGHT  # Те саме для висоти
            x = 0  # Починаємо з нуля на кожному новому рядку

    def total_level_width(level):
        return len(level[0]) * PLATFORM_WIDTH  # Розрахунок фактичної ширини рівня

    def total_level_height(level):
        return len(level) * PLATFORM_HEIGHT  # Розрахунок фактичної висоти рівня

    timer = time.Clock()

    mixer.music.load("images/music/music_comics.mp3")
    mixer.music.set_volume(0.1)
    mixer.music.play(-1)

    screen_now = "menu"
    tick = 0

    while game: # Основний цикл гри

        # Меню
        if screen_now == "menu":
            bg_menu.reset()
            btn_play.reset()
            btn_exit.reset()
            logo.reset()

            for e in event.get():
                if e.type == QUIT:
                    game = False
                elif e.type == MOUSEBUTTONDOWN:
                    if btn_play.rect.collidepoint(e.pos):
                        screen_now = "comics"
                        tick = 0
                        fade(screen, WIN_WIDTH, WIN_HEIGHT)
                    if btn_exit.rect.collidepoint(e.pos):
                        fade(screen, WIN_WIDTH, WIN_HEIGHT)
                        game = False

        timer.tick(60)
        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                game = False

            if e.type == KEYDOWN and e.key == K_SPACE:
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                right = True

            if e.type == KEYUP and e.key == K_SPACE:
                up = False
            if e.type == KEYUP and e.key == K_d:
                right = False
            if e.type == KEYUP and e.key == K_a:
                left = False

            if e.type == KEYDOWN and e.key == K_SPACE and screen_now == "comics":  # Пропустити комікс
                tick = 1000

        # Комікс: щось типу пред історії
        if screen_now == "comics":
            comics.reset()
            comics.gif()
            tick += 1

            if tick >= 1000:
                screen_now = "level1"
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                mixer.music.load("images/music/music1.wav")
                mixer.music.set_volume(0.2)
                mixer.music.play(-1)
                tick = 0


        # Перший рівень
        if screen_now == "level1":
            if tick == 0:
                draw_level(level1)
                camera = Camera(camera_configure, total_level_width(level1), total_level_height(level1))  # Налаштування камери

            bg.reset()
            camera.update(hero)  # Центруємо камеру відносно персонажа
            hero.update(left, right, up, platforms, crystals, exits, spikes)  # Оновлення руху героя
            for e in entities:
                screen.blit(e.image, camera.apply(e))

            # Створення тексту для відображення очок
            score_text = font.render(f"Уламки: {hero.score}/5", True, (255, 255, 255))  # Білий текст
            screen.blit(score_text, (10, 10))  # Відображення у верхньому лівому куті

            tick += 1

            if hero.score == 5 and hero.ex == True: # Якщо гравець зібрав 5 монет та торкнувся прохід на наступний рівень він переходить на наступний рівень.
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "level2"
                hero.score = 0 # Обнулення рахунку героя
                hero.ex = False

            if hero.death == True:
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "Die"
                mixer.music.load("images/music/died.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()


        # Другий рівень
        if screen_now == "level2":
            if tick == 0:
                sprite.Group.empty(entities)  # Очищення групи сутностей
                sprite.Group.empty(crystals)  # Очищення групи уламків
                platforms.clear()  # Очищення списку платформ
                exits.clear()  # Очищення списку виходів
                spikes.clear() # Очищення списку шипів
                entities.add(hero)  # Додавання героя

                draw_level(level2)
                camera = Camera(camera_configure, total_level_width(level2), total_level_height(level2))  # Налаштування камери


            bg_2.reset()  # Оновлення фону
            camera.update(hero)  # Центруємо камеру відносно персонажа
            hero.update(left, right, up, platforms, crystals, exits, spikes)  # Оновлення руху персонажа
            for e in entities:
                screen.blit(e.image, camera.apply(e))  # Відображення сутностей на екрані

            # Створення тексту для відображення очок
            score_text = font.render(f"Уламки: {hero.score}/5", True, (255, 255, 255))  # Білий текст
            screen.blit(score_text, (10, 10))  # Відображення в лівому верхньому куті

            tick += 1

            if hero.score == 5 and hero.ex == True: # Якщо гравець зібрав 5 монет та торкнувся прохід на наступний рівень він переходить на наступний рівень.
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "level3"
                hero.score = 0  # Обнулення рахунку героя
                hero.ex = False

            if hero.death == True:
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "Die"
                mixer.music.load("images/music/died.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()


        # Третій рівень
        if screen_now == "level3":
            if tick == 0:
                sprite.Group.empty(entities)  # Очищення групи сутностей
                sprite.Group.empty(crystals)  # Очищення групи уламків
                platforms.clear()  # Очищення списку платформ
                exits.clear()  # Очищення списку виходів
                spikes.clear() # Очищення списку шипів
                entities.add(hero)  # Додавання героя

                draw_level(level3)
                camera = Camera(camera_configure, total_level_width(level3),total_level_height(level3))  # Налаштування камери

            bg_3.reset()  # Оновлення фону
            camera.update(hero)  # Центруємо камеру відносно персонажа
            hero.update(left, right, up, platforms, crystals, exits, spikes)  # Оновлення руху персонажа
            for e in entities:
                screen.blit(e.image, camera.apply(e))  # Відображення сутностей на екрані

            # Створення тексту для відображення очок
            score_text = font.render(f"Уламки: {hero.score}/7", True, (255, 255, 255))  # Білий текст
            screen.blit(score_text, (10, 10))  # Відображення в лівому верхньому куті

            tick += 1

            if hero.score == 7 and hero.ex == True: # Якщо гравець зібрав 7 монет та торкнувся прохід на наступний рівень він переходить на наступний рівень.
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "the_end"
                mixer.music.load("images/music/Final_music.mp3")
                mixer.music.set_volume(0.5)
                mixer.music.play(-1)
                hero.score = 0 # Обнулення рахунку героя
                hero.ex = False
            if hero.score < 7:
                hero.ex = False

            if hero.death == True:
                tick = 0
                fade(screen, WIN_WIDTH, WIN_HEIGHT)
                screen_now = "Die"
                mixer.music.load("images/music/died.mp3")
                mixer.music.set_volume(0.7)
                mixer.music.play()


        if screen_now == "Die":
            screen.fill((0, 0, 0))
            die.reset()

        if screen_now == "the_end":
            bg_the_end.reset()

        pygame.time.delay(15)  # Додаємо невелику затримку для кращої реакції
        pygame.display.update()  # Оновлення екрану

        

if __name__ == "__main__":
    main()
