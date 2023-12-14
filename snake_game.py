import random
import pygame
import numpy as np

class Snake():
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)

    dis_width = 200
    dis_height = 200
    
    board_width = 36
    board_height = 36
    
    board_food_border = 3
    
    board_block = 10
    
    snake_head = []
    
    current_step = 0
    steps_max = 50000
    
    clock = pygame.time.Clock()
    snake_speed = 12
    
    game_over_reason = 'none'
    
    snake_max_size = 1000
    
    def __init__(self, board_size=36, food_border=3):
        self.board_width = board_size
        self.board_height = board_size
        self.board_food_border = food_border
        
        self.dis_width = board_size * self.board_block
        self.dis_height = board_size * self.board_block + 4 * self.board_block
        self.reset()
    
    def step(self, action):
        if self.game_over or self.trunc:
            return self.get_step_result()

        x1_change = 0
        y1_change = 0
        
        # process action
        if action == 0: # Left
            x1_change = -1
            y1_change = 0
        elif action == 1: # Right
            x1_change = 1
            y1_change = 0
        elif action == 2: # Down
            y1_change = -1
            x1_change = 0
        elif action == 3: # Up
            y1_change = 1
            x1_change = 0
            
        self.x1 += x1_change
        self.y1 += y1_change
        
        if self.x1 >= self.board_width or self.x1 < 0 or self.y1 >= self.board_height or self.y1 < 0:
            self.game_over = True
            self.game_over_reason = 'border'
            return self.get_step_result()
        
        self.snake_head = []
        self.snake_head.append(self.x1)
        self.snake_head.append(self.y1)
        
        if self.snake_list[-1] == self.snake_head:
            self.game_over = True
            self.game_over_reason = 'step back'
            return self.get_step_result()
        
        self.snake_list.append(self.snake_head)
        
        if len(self.snake_list) > self.length_of_snake:
            del self.snake_list[0]
        
        for x in self.snake_list[:-1]:
            if x == self.snake_head:
                self.game_over = True
                self.game_over_reason = 'self-eating'
                return self.get_step_result()
        
        if self.x1 == self.foodx and self.y1 == self.foody:
            self.put_food()
            self.length_of_snake += 1
        
        self.current_step += 1
        
        if int(self.length_of_snake) >= self.snake_max_size:
            self.game_over = True
            self.game_over_reason = 'snake max size'
            return self.get_step_result()
        
        if self.current_step >= self.steps_max:
            self.trunc = True
            self.game_over_reason = 'truncated'
            return self.get_step_result()
        
        #print('step head: {} - {}'.format(self.snake_head[0], self.snake_head[1]))
        return self.get_step_result()
        
    def put_food(self):
        rows = self.board_width
        columns = self.board_height
        
        board = np.zeros((rows, columns))
        board = np.array(board, dtype=np.uint8)
        
        for x in range(rows):
            for y in range(columns):
                if x < self.board_food_border or x >= rows-self.board_food_border or y < self.board_food_border or y >= columns-self.board_food_border:
                    board[x][y] = 1
        
        for item in self.snake_list:
            x = int(item[0])
            y = int(item[1])   
            board[x][y] = 1
        
        # Находим координаты ячеек равных нулю
        zero_cells = np.argwhere(board == 0)

        # Выбираем случайную ячейку равную нулю
        random_zero_cell = random.choice(zero_cells)
    
        self.foodx = random_zero_cell[0]
        self.foody = random_zero_cell[1]
        
    def reset(self):        
        self.game_over = False
        self.game_over_reason = 'none'
        
        self.trunc = False

        self.x1 = self.board_width / 2
        self.y1 = self.board_height / 2
        
        self.x1_change = 0
        self.y1_change = 0
        
        snake_tail_2 =    [self.x1, self.y1 - 2]
        snake_tail_1 =    [self.x1, self.y1 - 1]
        self.snake_head = [self.x1, self.y1]

        self.snake_list = []
        self.snake_list.append(snake_tail_2)
        self.snake_list.append(snake_tail_1)
        self.snake_list.append(self.snake_head)
        
        self.length_of_snake = 3

        self.put_food()
        
        self.current_step = 0
        return self.get_step_result()
    
    def get_step_result(self):
        game_over = self.game_over
        game_over_reason = self.game_over_reason
        win = int(self.length_of_snake) >= self.snake_max_size
        trunc = self.trunc
        board = self.get_obs()
        head = [int(self.snake_head[0] / 10), int(self.snake_head[1] / 10)]
        food = [int(self.foodx / 10), int(self.foody / 10)]
        length = int(self.length_of_snake)
        board_size = int(self.dis_width / 10)
        step = self.current_step
        
        state = {
            'game_over': game_over,
            'game_over_reason': game_over_reason,
            'win': win,
            'trunc': trunc,
            'board': board,
            'head': head,
            'food': food,
            'length': length,
            'board_size': board_size,
            'step': step
        }
        
        return state
        
    def get_obs(self):
        rows = self.board_width
        columns = self.board_height
        
        board = np.zeros((rows, columns))
        board = np.array(board, dtype=np.uint8)
        
        for item in self.snake_list:
            x = int(item[0])
            y = int(item[1])
            board[x][y] = 50
        
        x = int(self.snake_head[0])
        y = int(self.snake_head[1])
        board[x][y] = 150
        
        x = self.foodx
        y = self.foody
        board[x][y] = 200
        
        #board_inc = np.zeros((rows * self.board_block, columns * self.board_block))
        #board_inc = np.array(board_inc, dtype=np.uint8)
        
        #for x in range(rows * self.board_block):
        #    for y in range(columns * self.board_block):
        #        board_inc[x][y] = board[int(x / self.board_block)][int(y / self.board_block)]
        
        #return board_inc
        return board
        
            
    def init_render(self):
        pygame.init()
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)
        
        pygame.display.set_caption('Snake Game')
        
    def render(self):
        self.dis.fill(self.black)
        
        self.render_board()
        self.render_snake()
        self.render_food()
        
        self.render_score()
        self.render_game_over()
        
        pygame.display.update()
        self.clock.tick(self.snake_speed)
        
    def render_board(self):
        pygame.draw.rect(self.dis, self.blue, [0, 0, self.board_width * self.board_block, self.board_height * self.board_block])
        
    def render_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(self.dis, self.black, [x[0] * self.board_block, x[1] * self.board_block, self.board_block, self.board_block])
            
        pygame.draw.rect(self.dis, self.red, [self.x1 * self.board_block, self.y1 * self.board_block, self.board_block, self.board_block])
        
    def render_food(self):
        pygame.draw.rect(self.dis, self.green, [self.foodx * self.board_block, self.foody * self.board_block, self.board_block, self.board_block])
        
    def render_score(self):
        avg = 0
        if self.length_of_snake > 3:
            avg = self.current_step / (self.length_of_snake - 3)
        
        mesg = self.font_style.render('Score: {}  Step: {}  Avg: {}'.format(self.length_of_snake - 3, self.current_step, int(avg)), True, self.yellow)
        self.dis.blit(mesg, [0, self.board_height * self.board_block])
        
    def render_game_over(self):
        if self.game_over_reason != 'none':
            mesg = self.font_style.render('Game Over Reason: {}'.format(self.game_over_reason), True, self.yellow)
            self.dis.blit(mesg, [0, (self.board_height + 2) * self.board_block])
        
    def close(self):
        pygame.quit()