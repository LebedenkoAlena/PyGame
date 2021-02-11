import pygame, os, sys

pygame.init()


leval = 'leval_1.txt'
with open(fr'data/{leval}', mode='r') as txt:
    text = txt.read().split()
    size = WIDTH, HEIGHT = len(text[0]) * 50, len(text) * 50
all_sprites = pygame.sprite.Group()
STEP = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('CRAZY HARE')
clock = pygame.time.Clock()
FPS = 50
run = False

def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return True
        pygame.display.flip()
        clock.tick(FPS)

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


def terminate():
    pygame.quit()
    sys.exit()


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

tile_images = {
    'carrot': load_image('carrot.png'),
    'box': load_image('box.png'),
    'earth': load_image('earth.png'),
    'end': load_image('end.png'),
    'trap': load_image('trap.png'),
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
player_image = load_image('rabbit.png')
carrot_image = load_image('carrot.png')
key_image = load_image('key.png')
lock_image = load_image('lock.png')
shetchik = load_image('shetchik1.png')
ship_image = load_image('ship.png')

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


def draw_lives(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x - 5
    img_rect.y = y
    surf.blit(img, img_rect)


def draw_col(col, h):
    font = pygame.font.Font(None, 90)
    text = font.render(col, True, (255, 255, 255))
    if int(col) < 10:
        screen.blit(text, (h - 100, 5))
    else:
        screen.blit(text, (h - 130, 5))


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


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def get_coords(level, object):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == object:
                return int(x), int(y)


def coords(*args):
    return tile_width * args[0][0], tile_height * args[0][1]


def game_over(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 100)
    text = font.render("GAME OVER", True, (136, 231, 252))
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (136, 231, 252), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 10)


def moving(direction, level, x, y, col_key):
    crossing_lock = pygame.sprite.spritecollide(player, lock_group, False, pygame.sprite.collide_circle)
    logic = True
    if direction == 'right' and level[y][x + 1] == '#' \
            or direction == 'left' and level[y][x - 1] == '#' \
            or direction == 'down' and level[y + 1][x] == '#' \
            or direction == 'up' and level[y - 1][x] == '#':
        logic = False
    elif direction == 'right' and level[y][x + 1] == '0' \
            or direction == 'left' and level[y][x - 1] == '0' \
            or direction == 'down' and level[y + 1][x] == '0' \
            or direction == 'up' and level[y - 1][x] == '0':
        logic = False
    elif direction == 'right' and level[y][x + 1] == '<' \
            or direction == 'down' and level[y + 1][x] == '<' \
            or direction == 'up' and level[y - 1][x] == '<' \
            or direction == 'left' and level[y][x - 1] == '>' \
            or direction == 'down' and level[y + 1][x] == '>' \
            or direction == 'up' and level[y - 1][x] == '>' \
            or direction == 'down' and level[y + 1][x] == ')' \
            or direction == 'right' and level[y][x + 1] == ')' \
            or direction == 'left' and level[y][x - 1] == ')' \
            or direction == 'up' and level[y - 1][x] == '(' \
            or direction == 'right' and level[y][x + 1] == '(' \
            or direction == 'left' and level[y][x - 1] == '(':
        logic = False
    elif level[y][x] == '/':
        Ship(x, y)
    elif direction == 'right' and crossing_lock and col_key < 1 \
            or direction == 'left' and crossing_lock and col_key < 1 \
            or direction == 'down' and crossing_lock and col_key < 1 \
            or direction == 'up' and crossing_lock and col_key < 1:
        logic = False
    elif direction == 'right' and text[y][x + 1] == '*' \
            or direction == 'left' and text[y][x - 1] == '*' \
            or direction == 'down' and text[y + 1][x] == '-' \
            or direction == 'up' and text[y - 1][x] == '-':
        logic = False
    elif direction == 'right' and text[y][x] == '*' \
            or direction == 'left' and text[y][x] == '*':
        logic = False
    elif direction == 'down' and text[y][x] == '-' \
            or direction == 'up' and text[y][x] == '-':
        logic = False
    elif direction == 'left' and text[y][x] == '1' \
            or direction == 'down' and text[y][x] == '1' \
            or direction == 'right' and text[y][x + 1] == '1' \
            or direction == 'up' and text[y - 1][x] == '1':
        logic = False
    elif direction == 'left' and text[y][x] == '2' \
            or direction == 'up' and text[y][x] == '2' \
            or direction == 'right' and text[y][x + 1] == '2' \
            or direction == 'down' and text[y + 1][x] == '2':
        logic = False
    elif direction == 'right' and text[y][x] == '3' \
            or direction == 'up' and text[y][x] == '3' \
            or direction == 'left' and text[y][x - 1] == '3' \
            or direction == 'down' and text[y + 1][x] == '3':
        logic = False
    elif direction == 'right' and text[y][x] == '4' \
            or direction == 'down' and text[y][x] == '4' \
            or direction == 'left' and text[y][x - 1] == '4' \
            or direction == 'up' and text[y - 1][x] == '4':
        logic = False
    if text[y][x] == '*' and logic == True:
        text[y][x] = '-'
        Tile('earth', x, y)
        Tile('most=', x, y)
    elif text[y][x] == '-' and logic == True:
        text[y][x] = '*'
        Tile('earth', x, y)
        Tile('most', x, y)
    elif text[y][x] == '1' and logic == True:
        text[y][x] = '2'
        Tile('earth', x, y)
        Tile('2', x, y)
    elif text[y][x] == '2' and logic == True:
        text[y][x] = '3'
        Tile('earth', x, y)
        Tile('3', x, y)
    elif text[y][x] == '3' and logic == True:
        text[y][x] = '4'
        Tile('earth', x, y)
        Tile('4', x, y)
    elif text[y][x] == '4' and logic == True:
        text[y][x] = '1'
        Tile('earth', x, y)
        Tile('1', x, y)
    return logic


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, *args):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        x, y = args[0][0], args[0][1]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
start_screen()

level = load_level(leval)
player, level_x, level_y = generate_level(level)
col = level_carrot[leval]
col_key = 0

target = AnimatedSprite(load_image("animation.png"), 2, 1, coords(get_coords(level, '$')))

fullname = os.path.join('data', "music.ogg")
filepath = os.path.abspath(__file__)
filedir = os.path.dirname(filepath)
musicpath = os.path.join(filedir, fullname)
pygame.mixer.music.load(musicpath)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)
carrot_sound_name = os.path.join('data', "carrot_music.mp3")
carrot_sound = pygame.mixer.Sound(os.path.join(filedir, carrot_sound_name))
lock_sound_name = os.path.join('data', "lock_sound.mp3")
lock_sound = pygame.mixer.Sound(os.path.join(filedir, lock_sound_name))
key_sound_name = os.path.join('data', "key_sound.mp3")
key_sound = pygame.mixer.Sound(os.path.join(filedir, key_sound_name))
deatn_sound_name = os.path.join('data', "death_sound.mp3")
death_sound = pygame.mixer.Sound(os.path.join(filedir, deatn_sound_name))

# death_sound_name = os.path.join('data', "death_sound.mp3")
# death_sound = pygame.mixer.Sound(os.path.join(filedir, death_sound_name))
with open(fr'data/{leval}', mode='r') as txt:
    text_help = txt.read().split()
text = list([] * len(text_help))
for i in range(len(text_help)):
    spisok = []
    for j in range(len(text_help[0])):
        spisok.append(text_help[i][j])
    text.append(spisok)
running = True
x, y = get_coords(level, '@')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if moving('left', level, x, y, col_key):
                    player.rect.x -= STEP
                    x -= 1
            if event.key == pygame.K_RIGHT:
                if moving('right', level, x, y, col_key):
                    player.rect.x += STEP
                    x += 1
            if event.key == pygame.K_UP:
                if moving('up', level, x, y, col_key):
                    player.rect.y -= STEP
                    y -= 1
            if event.key == pygame.K_DOWN:
                if moving('down', level, x, y, col_key):
                    player.rect.y += STEP
                    y += 1
    fon = pygame.transform.scale(load_image('grass.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    tiles_group.draw(screen)
    carrot_group.draw(screen)
    key_group.draw(screen)
    ship_group.draw(screen)
    lock_group.draw(screen)
    player_group.draw(screen)
    draw_lives(screen, WIDTH - 50, 5,
               shetchik)

    crossing_carrot = pygame.sprite.spritecollide(player, carrot_group, True, pygame.sprite.collide_circle)
    crossing_ship = pygame.sprite.spritecollide(player, ship_group, False, pygame.sprite.collide_circle)
    crossing_key = pygame.sprite.spritecollide(player, key_group, True, pygame.sprite.collide_circle)
    if crossing_carrot:
        col -= 1
        carrot_sound.play()
    draw_col(str(col), HEIGHT)
    if crossing_ship:
        pygame.mixer.music.stop()
        death_sound.play()
        running = False
        run = True

    if crossing_key:
        col_key += 1
        key_sound.play()
    if col_key >= 1:
        crossing_lock = pygame.sprite.spritecollide(player, lock_group, True, pygame.sprite.collide_circle)
        if crossing_lock:
            col_key -= 1
            lock_sound.play()
    if col == 0:
        all_sprites.draw(screen)
        target.update()

    pygame.display.flip()
    clock.tick(FPS)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('CRAZY HARE')
clock = pygame.time.Clock()
FPS = 50
screen.fill((0, 0, 0))
while run:
    for event in pygame.event.get():
        font = pygame.font.Font(None, 100)
        font_res = pygame.font.Font(None, 75)
        text = font.render("GAME OVER", True, (136, 231, 252))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (136, 231, 252), (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20), 10)
        text_res = font_res.render('RESTART', True, (136, 231, 252))
        text_res_x = WIDTH // 1.5 - text.get_width() // 1.7
        text_res_y = HEIGHT // 1.5 - text.get_height() // 3
        screen.blit(text_res, (text_res_x, text_res_y))
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if x >= 286 and x <= 523 and y >= 511 and y <= 562:
                pygame.quit()
                os.system('1.py')
    pygame.display.flip()
    clock.tick(FPS)
terminate()
