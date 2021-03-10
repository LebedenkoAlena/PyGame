from PyQt5.QtWidgets import QApplication, QMainWindow

from functions import *
from level import returning, Generate

# инициализация pygame
pygame.init()


# открытие первоначального окна
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


# проверка возможности передвижения
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
    elif direction == 'right' and text[y][x + 1] == '%' and col_key < 1 \
            or direction == 'left' and text[y + 1][x] == '%' and col_key < 1 \
            or direction == 'down' and text[y][x - 1] == '%' and col_key < 1 \
            or direction == 'up' and text[y - 1][x] == '%' and col_key < 1:
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
    # поворот мостов при пересечении
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


# класс, реализующий анимацию мишени
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


# открытие Qt-окна
if start_screen():
    app = QApplication(sys.argv)
    generate = Generate()
    generate.show()
    app.exec()

# определение выбранного уровня и прогрузка
leval, level_numder = returning()
level = load_level(leval)
# определение необходимого размера окна
with open(fr'data/{leval}', mode='r') as txt:
    text = txt.read().split()
    size = WIDTH, HEIGHT = len(text[0]) * 50, len(text) * 50
# установление размера и генерация уровня
screen = pygame.display.set_mode(size)
player, level_x, level_y = generate_level(level)
# определение количества морковок на данном уровне
col = level_carrot[leval]

# создание экземпляра класса для запуска анимации
target = AnimatedSprite(load_image("animation.png"), 2, 1, coords(get_coords(level, '$')))

# запуск фоновой музыки в бесконечном режиме
pygame.mixer.music.load(musicpath)
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(loops=-1)

# добавление второстепенных звуков
carrot_sound = pygame.mixer.Sound(os.path.join(filedir, carrot_sound_name))
lock_sound = pygame.mixer.Sound(os.path.join(filedir, lock_sound_name))
key_sound = pygame.mixer.Sound(os.path.join(filedir, key_sound_name))
death_sound = pygame.mixer.Sound(os.path.join(filedir, deatn_sound_name))

# создание копии уровня (необходимо для поворотов мостов)
with open(fr'data/{leval}', mode='r') as txt:
    text_help = txt.read().split()
text = list([] * len(text_help))
for i in range(len(text_help)):
    spisok = []
    for j in range(len(text_help[0])):
        spisok.append(text_help[i][j])
    text.append(spisok)

x, y = get_coords(level, '@')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            a, b = event.pos
            if a <= 50 and b <= 50:
                running = False
                pygame.mixer.music.stop()
                death_sound.play()
                run = True
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
    restart(screen, res)
    if get_coords(level, '$')[0] == x and get_coords(level, '$')[1] == y:
        crossing_target = True
    else:
        crossing_target = False
    crossing_carrot = pygame.sprite.spritecollide(player, carrot_group, True, pygame.sprite.collide_circle)
    crossing_ship = pygame.sprite.spritecollide(player, ship_group, False, pygame.sprite.collide_circle)
    crossing_key = pygame.sprite.spritecollide(player, key_group, True, pygame.sprite.collide_circle)
    if crossing_carrot:
        col -= 1
        carrot_sound.play()
    draw_col(str(col), WIDTH)
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
            text[y][x] = '.'
    if col == 0:
        all_sprites.draw(screen)
        target.update()
        player_group.draw(screen)
        if crossing_target:
            with open('levels_unblock.txt', mode='r') as levels_unblock:
                levels_unblock_text = levels_unblock.read().split()
            with open('levels_unblock.txt', mode='w') as levels_completed:
                if len(levels_unblock_text) > 0:
                    if int(levels_unblock_text[0]) < level_numder:
                        levels_completed.write(f' {level_numder}')
                    else:
                        levels_completed.write(levels_unblock_text[0])
                else:
                    levels_completed.write('1')
            with open('levels_unblock.txt', mode='r') as levels_unblock:
                levels_unblock_text = levels_unblock.read().split()
            if levels_unblock_text[0] == '16':
                while True:
                    size = HEIGHT, WIDTH = 600, 600
                    fon = pygame.transform.scale(load_image('fon_victory.jpg'), (WIDTH, HEIGHT))
                    screen = pygame.display.set_mode(size)
                    screen.blit(fon, (0, 0))
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminate()
                        elif event.type == pygame.KEYDOWN or \
                                event.type == pygame.MOUSEBUTTONDOWN:
                            with open('levels_unblock.txt', 'w') as level_zero:
                                level_zero.write(' ')
                            pygame.quit()
                            os.system('main.py')

                    pygame.display.flip()
                    clock.tick(FPS)
                pygame.display.flip()
                clock.tick(FPS)
            else:
                pygame.quit()
                os.system('main.py')
    pygame.display.flip()
    clock.tick(FPS)

# пересоздание окна
size = WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('CRAZY RABBIT')
clock = pygame.time.Clock()
FPS = 50
screen.fill((0, 0, 0))
# окно после смерти
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
        text_res_x = WIDTH // 2 - text.get_width() // 3
        text_res_y = HEIGHT // 2 + text.get_height()
        screen.blit(text_res, (text_res_x, text_res_y))
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            if x >= text_res_x and y >= text_res_y and x <= 400 and y <= 420:
                #возможность рестарта
                pygame.quit()
                os.system('main.py')
    pygame.display.flip()
    clock.tick(FPS)
terminate()
