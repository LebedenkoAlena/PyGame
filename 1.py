import pygame, os, sys

pygame.init()

all_sprites = pygame.sprite.Group()
size = HEIGHT, WIDTH = 800, 800
STEP = 50
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Перемещение героя')
clock = pygame.time.Clock()
FPS = 50


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
shetchik = load_image('shetchik1.png')
ship_image = load_image('ship.png')

tile_width = tile_height = 50
# основной персонаж
player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
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


class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(ship_group, all_sprites)
        self.image = ship_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


def draw_lives(surf, x, y, img):
    img_rect = img.get_rect()
    img_rect.x = x - 5
    img_rect.y = y
    surf.blit(img, img_rect)


def draw_col(col):
    font = pygame.font.Font(None, 90)
    text = font.render(col, True, (255, 255, 255))
    if int(col) < 10:
        screen.blit(text, (700, 5))
    else:
        screen.blit(text, (670, 5))


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
                Tile('lock', x, y)
            elif level[y][x] == '!':
                Tile('earth', x, y)
                Tile('key', x, y)
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


def get_coords(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                return int(x), int(y)


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


def moving(direction, level, x, y):
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

    return logic


level = load_level('leval_26.txt')
player, level_x, level_y = generate_level(level)
col = 0

running = True
x, y = get_coords(level)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if moving('left', level, x, y):
                    player.rect.x -= STEP
                    x -= 1
            if event.key == pygame.K_RIGHT:
                if moving('right', level, x, y):
                    player.rect.x += STEP
                    x += 1
            if event.key == pygame.K_UP:
                if moving('up', level, x, y):
                    player.rect.y -= STEP
                    y -= 1

            if event.key == pygame.K_DOWN:
                if moving('down', level, x, y):
                    player.rect.y += STEP
                    y += 1

    fon = pygame.transform.scale(load_image('grass.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    tiles_group.draw(screen)
    player_group.draw(screen)
    carrot_group.draw(screen)
    ship_group.draw(screen)
    draw_lives(screen, WIDTH - 50, 5,
               shetchik)

    hits = pygame.sprite.spritecollide(player, carrot_group, True, pygame.sprite.collide_circle)
    hit = pygame.sprite.spritecollide(player, ship_group, False, pygame.sprite.collide_circle)
    if hits:
        col += 1
    draw_col(str(col))
    if hit:
        game_over(screen)

    pygame.display.flip()
    clock.tick(FPS)

terminate()
