# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
import time

WIDTH = 1000
HEIGHT = 1000
FPS = 30

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
block = pygame.image.load("white_block.png")


class Block:
    side_len = 0

    def __init__(self, side_len, x, y, i_block, j_block):
        self.side_len = side_len
        self.add_image("white_block.png")
        self.x = x
        self.y = y
        self.is_created = False
        self.i_block = i_block
        self.j_block = j_block
        self.colour = "black"

    def add_image(self, image_name):
        self.block_img = pygame.image.load(image_name)
        self.block_img = pygame.transform.scale(self.block_img, (self.side_len, self.side_len))

    def draw(self):
        if self.is_created is True:
            screen.blit(self.block_img, (self.x, self.y))

    def clear(self):
        self.is_created = False
        if self.colour == "yellow" or self.colour == "blue":
            self.add_image("white_block.png")
        self.colour = "black"


class Maze:
    maze_width = 0
    maze_height = 0
    maze_start = {"i_block": 0, "j_block": 0}
    maze_end = {"i_block": 0, "j_block": 0}
    where_we_are = {"i_block": 0, "j_block": 0}
    run = False
    blocks = list()
    are_you_won = False

    def __init__(self, maze_width, maze_height, side_len, maze_start, maze_end):
        self.maze_width = 2 * maze_width - 1
        self.maze_height = 2 * maze_height - 1
        blocks = list()
        for i in range(self.maze_width):
            self.blocks.append(list())
            for j in range(self.maze_height):
                self.blocks[i].append(Block(side_len, side_len * i + 20, side_len * j + 20, i, j))
        self.maze_start["i_block"] = maze_start[0]
        self.maze_start["j_block"] = maze_start[1]
        self.maze_end["i_block"] = maze_end[0]
        self.maze_end["j_block"] = maze_end[1]
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].add_image("beauty_green_block.png")
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].colour = "green"
        self.blocks[self.maze_end["i_block"]][self.maze_end["j_block"]].add_image("beauty_red_block.png")
        self.blocks[self.maze_end["i_block"]][self.maze_end["j_block"]].colour = "red"

    def fileinit(self, filename):
        self.blocks = list()
        is_first_line = True
        i_block = 0
        j_block = 0
        with open(filename, "r") as file:
            for line in file:
                values = line.split('\n')
                # print(values)
                values = values[0].split(' ')
                # print(values)
                if is_first_line is True:
                    is_first_line = False
                    self.maze_width = int(values[0])
                    self.maze_height = eval(values[1])
                    side_len = eval(values[2])
                    self.maze_start["i_block"] = eval(values[3])
                    self.maze_start["j_block"] = eval(values[4])
                    self.maze_end["i_block"] = eval(values[5])
                    self.maze_end["j_block"] = eval(values[6])
                    self.run = eval(values[7])
                    self.are_you_won = eval(values[8])
                    self.where_we_are['i_block'] = eval(values[9])
                    self.where_we_are['j_block'] = eval(values[10])
                    continue
                if i_block == 0:
                    self.blocks.append(list())
                self.blocks[i_block].append(
                    Block(side_len, eval(values[0]), eval(values[1]), eval(values[2]), eval(values[3])))
                self.blocks[i_block][j_block].is_created = eval(values[4])
                self.blocks[i_block][j_block].colour = values[5]
                if j_block == self.maze_height - 1:
                    i_block += 1
                    j_block = 0
                else:
                    j_block += 1
            for i in range(self.maze_width):
                for j in range(self.maze_height):
                    if self.blocks[i][j].colour == "white" or self.blocks[i][j].colour == 'blue':
                        self.blocks[i][j].add_image("white_block.png")
                        self.blocks[i][j].colour = 'white'
                    elif self.blocks[i][j].colour == "green":
                        self.blocks[i][j].add_image("beauty_green_block.png")
                    elif self.blocks[i][j].colour == "red":
                        self.blocks[i][j].add_image("beauty_red_block.png")
                    elif self.blocks[i][j].colour == "yellow":
                        self.blocks[i][j].add_image("beauty_yellow_block.png")

    def write_maze(self):
        i = random.uniform(0, 1)
        with open(f"maze_{i}.txt", "w") as file:
            file.write(
                f"{self.maze_width} {self.maze_height} {self.blocks[0][0].side_len} {self.maze_start['i_block']} {self.maze_start['j_block']} {self.maze_end['i_block']} {self.maze_end['j_block']} {self.run} {self.are_you_won} {self.where_we_are['i_block']} {self.where_we_are['j_block']}\n")
            for i in range(len(self.blocks)):
                for j in range(len(self.blocks[0])):
                    file.write(
                        f"{self.blocks[i][j].x} {self.blocks[i][j].y} {self.blocks[i][j].i_block} {self.blocks[i][j].j_block} {self.blocks[i][j].is_created} {self.blocks[i][j].colour}\n")

    def start_running(self):
        print("la")
        self.where_we_are = {"i_block": self.maze_start["i_block"], "j_block": self.maze_start["j_block"]}
        self.run = True

    def checking_is_the_colour_yellow_or_green_or_red(self, i_change, j_change):
        if self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour == "yellow" or \
                self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour == "green" or \
                self.blocks[self.where_we_are["i_block"] + i_change][
                    self.where_we_are["j_block"] + j_change].colour == 'red':
            self.blocks[self.where_we_are["i_block"] + i_change][
                self.where_we_are["j_block"] + j_change].colour = 'blue'
            self.blocks[self.where_we_are["i_block"] + i_change][self.where_we_are["j_block"] + j_change].add_image(
                "beauty_blue_block.png")

    def checking_is_the_colour_white(self):
        if self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour == 'white' or \
                self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour == 'blue':
            self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour = 'yellow'
            self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].add_image("beauty_yellow_block.png")

    def checking_is_the_colour_red(self):
        if self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"]].colour == 'red':
            self.are_you_won = True
            screen.blit(you_won, (0, 0))

    def go_down(self):
        if self.where_we_are["j_block"] == self.maze_height - 1 or self.blocks[self.where_we_are["i_block"]][
            self.where_we_are["j_block"] + 1].colour == 'black':
            return
        self.where_we_are["j_block"] += 1
        self.checking_is_the_colour_yellow_or_green_or_red(0, -1)
        self.checking_is_the_colour_white()
        self.checking_is_the_colour_red()

    def go_up(self):
        if self.where_we_are["j_block"] == 0 or self.blocks[self.where_we_are["i_block"]][
            self.where_we_are["j_block"] - 1].colour == 'black':
            return
        self.where_we_are["j_block"] -= 1
        if self.blocks[self.where_we_are["i_block"]][self.where_we_are["j_block"] + 1].colour == 'red':
            return
        self.checking_is_the_colour_yellow_or_green_or_red(0, 1)
        self.checking_is_the_colour_white()
        self.checking_is_the_colour_red()

    def go_left(self):
        if self.where_we_are["i_block"] == 0 or self.blocks[self.where_we_are["i_block"] - 1][
            self.where_we_are["j_block"]].colour == 'black':
            return
        self.where_we_are["i_block"] -= 1
        if self.blocks[self.where_we_are["i_block"] + 1][self.where_we_are["j_block"]].colour == 'red':
            return
        self.checking_is_the_colour_yellow_or_green_or_red(1, 0)
        self.checking_is_the_colour_white()
        self.checking_is_the_colour_red()

    def go_right(self):
        print("bla")
        if self.where_we_are["i_block"] == self.maze_width - 1 or self.blocks[self.where_we_are["i_block"] + 1][
            self.where_we_are["j_block"]].colour == 'black':
            return
        self.where_we_are["i_block"] += 1
        if self.blocks[self.where_we_are["i_block"] - 1][self.where_we_are["j_block"]].colour == 'red':
            return
        self.checking_is_the_colour_yellow_or_green_or_red(-1, 0)
        self.checking_is_the_colour_white()
        self.checking_is_the_colour_red()

    def change_maze_start(self, i, j):
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].add_image("white_block.png")
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].colur = "white"
        self.maze_start["i_block"] = 2 * i
        self.maze_start["j_block"] = 2 * j
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].add_image("beauty_green_block.png")
        self.blocks[self.maze_start["i_block"]][self.maze_start["j_block"]].colour = 'green'

    def change_maze_end(self, i, j):
        self.blocks[self.maze_end["i_block"]][self.maze_end["j_block"]].add_image("white_block.png")
        self.maze_end["i_block"] = 2 * i
        self.maze_end["j_block"] = 2 * j
        self.blocks[self.maze_end["i_block"]][self.maze_end["j_block"]].add_image("beauty_red_block.png")
        self.blocks[self.maze_end["i_block"]][self.maze_end["j_block"]].colour = 'red'

    def draw_maze(self):
        for i in range(self.maze_width):
            for j in range(self.maze_height):
                self.blocks[i][j].draw()

    def draw_only_yellow_and_blue_blocks(self):
        for i in range(self.maze_width):
            for j in range(self.maze_height):
                if self.blocks[i][j].colour == 'yellow' or self.blocks[i][j].colour == 'blue' or self.blocks[i][
                    j].colour == 'green' or self.blocks[i][j].colour == 'red':
                    self.blocks[i][j].draw()

    def clear_walls(self):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[0])):
                self.blocks[i][j].clear()
        self.change_maze_start(int(self.maze_start["i_block"] / 2), int(self.maze_start["j_block"] / 2))
        self.change_maze_end(int(self.maze_end["i_block"] / 2), int(self.maze_end["j_block"] / 2))

    def clear_walls_from_yellow_and_blue_blocks(self):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[0])):
                if self.blocks[i][j].colour == "yellow" or self.blocks[i][j].colour == "blue":
                    self.blocks[i][j].add_image("white_block.png")
                    self.blocks[i][j].colour = "white"

    def checking_are_we_out_of_maze_or_go_to_grandpa(self, i_now_block, j_now_block, grandparent,
                                                     is_first_time) -> bool:
        if i_now_block < 0 or i_now_block >= len(self.blocks):
            return False
        if j_now_block < 0 or j_now_block >= len(self.blocks[0]):
            return False
        if is_first_time is False:
            if i_now_block == grandparent.i_block and j_now_block == grandparent.j_block:
                return False
        return True

    def checking_can_we_move_there(self, i_now_block, j_now_block, grandparent, is_first_time) -> bool:
        if self.checking_are_we_out_of_maze_or_go_to_grandpa(i_now_block, j_now_block, grandparent,
                                                             is_first_time) is False:
            return False
        if self.blocks[i_now_block][j_now_block].is_created is True:
            return False
        return True

    def checking_is_path_created(self, i_now_block, j_now_block, grandparent, is_first_time, direction):
        if self.checking_are_we_out_of_maze_or_go_to_grandpa(i_now_block, j_now_block, grandparent,
                                                             is_first_time) is False:
            return False
        if self.blocks[i_now_block - int(direction[0] / 2)][j_now_block - int(direction[1] / 2)].is_created is False:
            return False
        return True

    def create_maze_dfs_algorithm(self, now_block: Block, parent: Block, is_first_time):
        now_block.is_created = True
        if is_first_time is False:
            now_block.colour = "white"
        if now_block.i_block == self.maze_end["i_block"] and now_block.j_block == self.maze_end["j_block"]:
            return
        direction = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        random.shuffle(direction)
        for i in range(4):
            if self.checking_can_we_move_there(now_block.i_block + direction[i][0], now_block.j_block + direction[i][1],
                                               parent, is_first_time) is False:
                continue
            self.blocks[now_block.i_block + int(direction[i][0] / 2)][
                now_block.j_block + int(direction[i][1] / 2)].is_created = True
            self.blocks[now_block.i_block + int(direction[i][0] / 2)][
                now_block.j_block + int(direction[i][1] / 2)].colour = "white"
            self.create_maze_dfs_algorithm(
                self.blocks[now_block.i_block + direction[i][0]][now_block.j_block + direction[i][1]],
                now_block, False)

    def create_maze_dfs(self):
        self.clear_walls()
        start = self.blocks[2 * random.randint(0, int(self.maze_width / 2))][
            2 * random.randint(0, int(self.maze_height / 2))]
        self.create_maze_dfs_algorithm(start, start, True)
        self.change_maze_start(int(self.maze_start["i_block"] / 2), int(self.maze_start["j_block"] / 2))
        self.change_maze_end(int(self.maze_end["i_block"] / 2), int(self.maze_end["j_block"] / 2))

    def find_path(self, now_block: Block, parent: Block, is_first_time) -> bool:
        is_on_path = False
        if now_block.i_block == self.maze_end["i_block"] and now_block.j_block == self.maze_end["j_block"]:
            return True
        direction = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        random.shuffle(direction)
        for i in range(4):
            if self.checking_is_path_created(now_block.i_block + direction[i][0], now_block.j_block + direction[i][1],
                                             parent, is_first_time, direction[i]) is False:
                continue
            if self.find_path(self.blocks[now_block.i_block + direction[i][0]][now_block.j_block + direction[i][1]],
                              now_block, False) is True:
                is_on_path = True
                if is_first_time is False:
                    now_block.add_image("beauty_blue_block.png")
                    now_block.colour = "blue"
                self.blocks[now_block.i_block + int(direction[i][0] / 2)][
                    now_block.j_block + int(direction[i][1] / 2)].add_image("beauty_blue_block.png")
                self.blocks[now_block.i_block + int(direction[i][0] / 2)][
                    now_block.j_block + int(direction[i][1] / 2)].colour = "blue"
        return is_on_path

    def clear_path(self):
        for i in range(len(self.blocks)):
            for j in range(len(self.blocks[0])):
                if self.blocks[i][j].colour == "blue":
                    self.blocks[i][j].colour = "white"
                    self.blocks[i][j].add_image("white_block.png")

    def create_lateral_walls(self, block_sets, j_block, probability):  # работает за квадратичное время(
        i = 0
        while True:
            i += 1
            if (i >= len(block_sets)):
                break
            if block_sets[i] == block_sets[i - 1]:
                continue
            if random.uniform(0, 1) <= probability:
                value = block_sets[i]
                j = i - 1
                k = i
                for k in range(len(block_sets)):
                    if block_sets[k] == value:
                        block_sets[k] = block_sets[j]
                self.blocks[2 * j + 1][j_block].is_created = True
                self.blocks[2 * j + 1][j_block].colour = "white"

    def create_lower_walls_in_one_set(self, set_start, set_length, j_block, probability):
        is_smth_created = False
        for i in range(set_length):
            if random.uniform(0, 1) <= probability:
                self.blocks[set_start + 2 * i][j_block + 1].is_created = True
                self.blocks[set_start + 2 * i][j_block + 1].colour = "white"
                is_smth_created = True
        if is_smth_created is False:
            self.blocks[set_start + 2 * random.randint(0, set_length - 1)][j_block + 1].is_created = True
            self.blocks[set_start + 2 * random.randint(0, set_length - 1)][j_block + 1].colour = "white"

    def create_lower_walls(self, block_sets, j_block, probability):
        set_start = 0
        i = 0
        set_length = 0
        while True:
            if set_length == 0:
                set_length += 1
                set_start = 2 * i
                continue
            i += 1
            if i == len(block_sets):
                if set_length != 0:
                    self.create_lower_walls_in_one_set(set_start, set_length, j_block, probability)
                break
            if block_sets[i] == block_sets[i - 1]:
                set_length += 1
                continue
            else:
                self.create_lower_walls_in_one_set(set_start, set_length, j_block, probability)
                set_length = 0
                set_start = 2 * i
                continue

    def remake_sets_that_havent_lower_wall(self, j_block, block_sets):
        set_value = max(block_sets)
        for i in range(len(block_sets)):
            if self.blocks[2 * i][j_block + 1].is_created is False:
                set_value += 1
                block_sets[i] = set_value

    def unite_sets_to_one(self, block_sets):
        for i in range(len(block_sets) - 1):
            if block_sets[i + 1] != block_sets[0]:
                value = block_sets[i + 1]
                for k in range(len(block_sets)):
                    if block_sets[k] == value:
                        block_sets[k] = block_sets[0]
                self.blocks[2 * i + 1][len(self.blocks[0]) - 1].is_created = True
                self.blocks[2 * i + 1][len(self.blocks[0]) - 1].colour = "white"

    def create_maze_eller_algorithm(self, j_block, block_sets, probability):
        for i in range(len(block_sets)):
            self.blocks[2 * i][j_block].is_created = True
            self.blocks[2 * i][j_block].colour = "white"
        self.create_lateral_walls(block_sets, j_block, probability)
        if j_block != len(self.blocks[0]) - 1:
            self.create_lower_walls(block_sets, j_block, probability)
            self.remake_sets_that_havent_lower_wall(j_block, block_sets)
            self.create_maze_eller_algorithm(j_block + 2, block_sets, probability)
        else:
            self.unite_sets_to_one(block_sets)
            return

    def create_maze_eller(self, probability):
        self.clear_walls()
        block_sets = [i for i in range(int(len(self.blocks) / 2) + 1)]
        self.create_maze_eller_algorithm(0, block_sets, probability)
        self.change_maze_start(int(self.maze_start["i_block"] / 2), int(self.maze_start["j_block"] / 2))
        self.change_maze_end(int(self.maze_end["i_block"] / 2), int(self.maze_end["j_block"] / 2))


class MouseAndKey():
    start = False
    end = False
    blind = False
    anything = False


you_won = pygame.image.load("you_won.png")
mouse = MouseAndKey()
block_size = int((min(WIDTH, HEIGHT) - 20) / 19)
maze = Maze(10, 10, block_size, (0, 0), (18, 18))
maze.create_maze_dfs()

# Цикл игры
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and mouse.anything is False:
            if event.key is pygame.K_SPACE:
                if maze.run is True:
                    print("Не-не-не-не-не")
                else:
                    maze.find_path(maze.blocks[maze.maze_start["i_block"]][maze.maze_start["j_block"]],
                                   maze.blocks[maze.maze_end["i_block"]][maze.maze_end["j_block"]],
                                   True)

            if event.key is pygame.K_d:
                maze.create_maze_dfs()
                maze.run = False
                maze.are_you_won = False
                mouse.blind = False
                print("Ваш лабиринт теперь построен по технологии dfs")

            if event.key is pygame.K_l:
                maze.create_maze_eller(0.47)
                maze.run = False
                maze.are_you_won = False
                mouse.blind = False
                print("Ваш лабиринт теперь построен по технологии Эллера")

            if event.key is pygame.K_s:
                print("Вы нажали на кнопку изменения стартовой точки лабиринта")
                print("Кликните на соответствующую улетку лабиринта для изменения")
                mouse.start = True
                mouse.anything = True

            if event.key is pygame.K_e:
                print("Вы нажали на кнопку изменения конечной точки лабиринта")
                print("Кликните на соответствующую улетку лабиринта для изменения")
                mouse.end = True
                mouse.anything = True

            if event.key is pygame.K_f:
                maze.write_maze()

            if event.key is pygame.K_o:
                print("Введите название файла:", end=' ')
                filename = input()
                maze.fileinit(filename)

            if event.key is pygame.K_r:
                maze.start_running()

            if event.key is pygame.K_q:
                maze.run = False
                mouse.blind = False
                maze.clear_walls_from_yellow_and_blue_blocks()

            if event.key == pygame.K_DOWN and maze.run is True:
                maze.go_down()

            if event.key == pygame.K_UP and maze.run is True:
                maze.go_up()

            if event.key == pygame.K_LEFT and maze.run is True:
                maze.go_left()

            if event.key == pygame.K_RIGHT and maze.run is True:
                maze.go_right()

            if event.key == pygame.K_y:
                if mouse.blind is False:
                    mouse.blind = True
                else:
                    mouse.blind = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("^v^")
            if mouse.start is True:
                i_coord = int((event.pos[0] - 20) / block_size)
                j_coord = int((event.pos[1] - 20) / block_size)
                if i_coord < 0 or i_coord > maze.maze_width or j_coord < 0 or j_coord > maze.maze_height:
                    print("Ой, Вы не попали по ячейке!")
                else:
                    mouse.start = False
                    mouse.anything = False
                    maze.change_maze_start(int(i_coord / 2), int(j_coord / 2))
            if mouse.end is True:
                i_coord = int((event.pos[0] - 20) / block_size)
                j_coord = int((event.pos[1] - 20) / block_size)
                if i_coord < 0 or i_coord > maze.maze_width or j_coord < 0 or j_coord > maze.maze_height:
                    print("Ой, Вы не попали по ячейке!")
                else:
                    mouse.end = False
                    mouse.anything = False
                    maze.change_maze_end(int(i_coord / 2), int(j_coord / 2))

        if event.type == pygame.KEYUP and mouse.anything is False:
            if event.key is pygame.K_SPACE:
                maze.clear_path()

    screen.fill((0, 0, 0))
    if maze.are_you_won == True:
        screen.blit(you_won, (0, 0))
    elif mouse.blind == False:
        maze.draw_maze()
    else:
        maze.draw_only_yellow_and_blue_blocks()
    pygame.display.flip()
    pass

pygame.quit()
