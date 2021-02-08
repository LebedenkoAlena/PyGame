import os
import sys
import pygame


class Game():
    def __init__(self):
        pygame.init()
        self.game_init()

    def game_init(self):
        self.size = self.WIDTH, self.HEIGHT = 600, 400
        self.screen = pygame.display.set_mode(self.size)
        self.fon = pygame.transform.scale(self.load_image('grass.jpg'), (self.WIDTH, self.HEIGHT))
        self.shetchik = self.load_image('shetchik1.png')
        self.x_pos = 15
        self.v = 10
        self.x = 1
        self.tile_images = {
            'carrot': self.load_image('carrot.png'),
            'box': self.load_image('box.png'),
            'earth': self.load_image('earth.png'),
            'end': self.load_image('end.png'),
            'trap': self.load_image('trap.png'),
            'arrow_l': self.load_image('arrow_l.png'),
            'arrow_r': self.load_image('arrow_r.png'),
            'arrow_b': self.load_image('arrow_b.png'),
            'arrow_t': self.load_image('arrow_t.png'),
            'most=': self.load_image('most=.png'),
            'most': self.load_image('most.png'),
            '1': self.load_image('1.png'),
            '2': self.load_image('2.png'),
            '3': self.load_image('3.png'),
            '4': self.load_image('4.png'),
            'button_no': self.load_image('button_no.png'),
            'button_yes': self.load_image('button_yes.png'),
            'lock': self.load_image('lock.png'),
            'key': self.load_image('key.png'),
        }
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
        leval = 'leval_18.txt'
        self.col = level_carrot[leval]
        self.clock = pygame.time.Clock()

    def loop(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.x = event.pos
                self.x_pos = 0
        self.screen.blit(self.fon, (0, 0))
        self.draw_lives(self.screen, self.WIDTH - 50, 5,
                        self.shetchik)
        self.draw_col(str(self.col), self.WIDTH)
        if self.x != 1:
            pygame.draw.circle(self.screen, (255, 255, 0), self.x, self.x_pos)
            self.x_pos += self.v * self.clock.tick() / 1000
        pygame.display.update()
        return False

    def load_image(self, name, colorkey=None):
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

    def draw_lives(self, surf, x, y, img):
        img_rect = img.get_rect()
        img_rect.x = x - 5
        img_rect.y = y
        surf.blit(img, img_rect)

    def draw_col(self, col, h):
        font = pygame.font.Font(None, 90)
        text = font.render(col, True, (255, 255, 255))
        if int(col) < 10:
            self.screen.blit(text, (h - 100, 5))
        else:
            self.screen.blit(text, (h - 130, 5))

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


class Tile(pygame.sprite.Sprite, Game):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(self.tiles_group, self.all_sprites)
        self.image = self.tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            self.tile_width * pos_x, self.tile_height * pos_y)



