import sys, pygame
from variables import *

# функция выхода из программы
def terminate():
    pygame.quit()
    sys.exit()

# отображение картинки морковки в счёте
def draw_lives(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x - 5
    img_rect.y = y
    surf.blit(img, img_rect)

# отображение количества оставшейся моркови
def draw_col(col, h):
    font = pygame.font.Font(None, 90)
    text = font.render(col, True, (255, 255, 255))
    if int(col) < 10:
        screen.blit(text, (h - 100, 5))
    else:
        screen.blit(text, (h - 130, 5))

# функция для работы с координатами на поле
def coords(*args):
    return tile_width * args[0][0], tile_height * args[0][1]

def restart(surf, img):
    img_rect = img.get_rect()
    img_rect.x = 5
    img_rect.y = 5
    surf.blit(img, img_rect)
