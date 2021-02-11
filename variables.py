import pygame, os, sys

# классы спрайтов
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 14, tile_height * pos_y - 25)
        self.radius = 5


class Carrot(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(carrot_group, all_sprites)
        self.image = carrot_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Key(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(key_group, all_sprites)
        self.image = key_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Lock(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lock_group, all_sprites)
        self.image = lock_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.radius = 50


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ship_group, all_sprites)
        self.image = ship_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.radius = 25


# функции, необходимые для генерации уровня и объявления переменных
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('earth', x, y)
            elif level[y][x] == '#':
                Tile('box', x, y)
            elif level[y][x] == '@':
                Tile('earth', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '$':
                Tile('earth', x, y)
                Tile('end', x, y)
            elif level[y][x] == 'm':
                Tile('earth', x, y)
                Carrot(x, y)
            elif level[y][x] == '/':
                Tile('trap', x, y)
            elif level[y][x] == '<':
                Tile('earth', x, y)
                Tile('arrow_l', x, y)
            elif level[y][x] == '>':
                Tile('earth', x, y)
                Tile('arrow_r', x, y)
            elif level[y][x] == '(':
                Tile('earth', x, y)
                Tile('arrow_b', x, y)
            elif level[y][x] == ')':
                Tile('earth', x, y)
                Tile('arrow_t', x, y)
            elif level[y][x] == '-':
                Tile('earth', x, y)
                Tile('most=', x, y)
            elif level[y][x] == '*':
                Tile('earth', x, y)
                Tile('most', x, y)
            elif level[y][x] == '1':
                Tile('earth', x, y)
                Tile('1', x, y)
            elif level[y][x] == '2':
                Tile('earth', x, y)
                Tile('2', x, y)
            elif level[y][x] == '3':
                Tile('earth', x, y)
                Tile('3', x, y)
            elif level[y][x] == '4':
                Tile('earth', x, y)
                Tile('4', x, y)
            elif level[y][x] == '8':
                Tile('earth', x, y)
                Tile('button_no', x, y)
            elif level[y][x] == '5':
                Tile('earth', x, y)
                Tile('button_yes', x, y)
            elif level[y][x] == '%':
                Tile('earth', x, y)
                Lock(x, y)
            elif level[y][x] == '!':
                Tile('earth', x, y)
                Key(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def get_coords(level, object):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == object:
                return int(x), int(y)

# переменные основных параметров
size = WIDTH, HEIGHT = 600, 600
all_sprites = pygame.sprite.Group()
STEP = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('CRAZY HARE')
clock = pygame.time.Clock()
FPS = 50
run = False

# количество моркови на каждом уровне
level_carrot = {
    'leval_1.txt': 9,
    'leval_2.txt': 13,
    'leval_3.txt': 12,
    'leval_4.txt': 35,
    'leval_5.txt': 19,
    'leval_6.txt': 24,
    'leval_7.txt': 34,
    'leval_8.txt': 8,
    'leval_9.txt': 27,
    'leval_10.txt': 17,
    'leval_11.txt': 16,
    'leval_12.txt': 27,
    'leval_13.txt': 8,
    'leval_14.txt': 17,
    'leval_15.txt': 10,
    'leval_16.txt': 21,
    'leval_17.txt': 21,
    'leval_18.txt': 18,
    'leval_19.txt': 8,
    'leval_20.txt': 23,
    'leval_21.txt': 18,
    'leval_22.txt': 18,
    'leval_23.txt': 32,
    'leval_24.txt': 11,
    'leval_25.txt': 21,
    'leval_26.txt': 65,
    'leval_27.txt': 8,
    'leval_28.txt': 22,
    'leval_29.txt': 15,
    'leval_30.txt': 10,
}

# словарь соответствия картинок
tile_images = {
    'carrot': load_image('carrot.png'),
    'box': load_image('box.png'),
    'earth': load_image('earth.png'),
    'trap': load_image('trap.png'),
    'end': load_image('end.png'),
    'arrow_l': load_image('arrow_l.png'),
    'arrow_r': load_image('arrow_r.png'),
    'arrow_b': load_image('arrow_b.png'),
    'arrow_t': load_image('arrow_t.png'),
    'most=': load_image('most=.png'),
    'most': load_image('most.png'),
    '1': load_image('1.png'),
    '2': load_image('2.png'),
    '3': load_image('3.png'),
    '4': load_image('4.png'),
    'button_no': load_image('button_no.png'),
    'button_yes': load_image('button_yes.png'),
    'lock': load_image('lock.png'),
    'key': load_image('key.png'),
}

# переменные картинок для прорисовки
player_image = load_image('rabbit.png')
carrot_image = load_image('carrot.png')
key_image = load_image('key.png')
lock_image = load_image('lock.png')
shetchik = load_image('shetchik1.png')
ship_image = load_image('ship.png')
end_image = load_image('end.png')
tile_width = tile_height = 50

# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
lock_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
carrot_group = pygame.sprite.Group()
ship_group = pygame.sprite.Group()

# создание переменных для воспроизведения фоновой музыки
fullname = os.path.join('data', "music.ogg")
filepath = os.path.abspath(__file__)
filedir = os.path.dirname(filepath)
musicpath = os.path.join(filedir, fullname)
# добавление хруста моркови при поедании
carrot_sound_name = os.path.join('data', "carrot_music.mp3")
# добавление скрежета замка при открытии
lock_sound_name = os.path.join('data', "lock_sound.mp3")
# добавление звона ключей
key_sound_name = os.path.join('data', "key_sound.mp3")
# добавление звука проигрыша (смерти)
deatn_sound_name = os.path.join('data', "death_sound.mp3")

# переменная для работы цикла
running = True
# количество съеденных морковок
col_key = 0