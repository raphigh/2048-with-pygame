import sys

from setting import *

import pygame
from pygame.locals import *
from random import choice
import pygwidgets

from InputNumber import *



pygame.init()
pygame.font.init()


class MyGame:
    def __init__(self):
        
        self.setting = Setting()
        
        self.window = pygame.display.set_mode((self.setting.WIDTH, self.setting.HEIGHT))
        pygame.display.set_caption(self.setting.CAPTION)
        
        self.BLOCK_WIDTH = (self.setting.WIDTH//self.setting.N)*(0.3)
        self.BLOCK_HEIGHT = (self.setting.HEIGHT//self.setting.N)*(0.3)
        
        self.running = False
        self.moves = 0
        self.grid = []
        for i in range(self.setting.N):
            self.grid.append([])
            for j in range(self.setting.N):
                self.grid[i].append(0)
        self.add_block()
        
        self.PlayButton = pygwidgets.CustomButton(self.window, (325, 325),
                                                 'img/play_button.png',
                                                 down='img/play_button2.png',
                                                 over='img/play_button.png',
                                                 disabled='img/play_button.png')
        self.hardship512 = pygwidgets.CustomButton(self.window, (500, 320),
                                                 'img/512.png',
                                                 down='img/5120ff.png',
                                                 over='img/512.png',
                                                 disabled='img/512.png')
        self.hardship1024 = pygwidgets.CustomButton(self.window, (500, 400),
                                                 'img/1024.png',
                                                 down='img/1024off.png',
                                                 over='img/1024.png',
                                                 disabled='img/1024.png')
        self.hardship2048 =pygwidgets.CustomButton(self.window, (500, 480),
                                                 'img/2048.png',
                                                 down='img/2048off.png',
                                                 over='img/2048.png',
                                                 disabled='img/2048.png')
        
        self.inputNumberCaption = pygwidgets.DisplayText(self.window, (150, 250), 'Input dimention of game(only numbers allowed):',
                                                    fontSize=24, width=190, justified='right')
        self.oInputNumber = InputNumber(self.window, (230, 280), '', width=150)

    def init_variables(self):
        self.running = True
        self.moves = 0
        self.grid = []
        for i in range(self.setting.N):
            self.grid.append([])
            for j in range(self.setting.N):
                self.grid[i].append(0)
        self.add_block()
        
        
    def update_block(self):
        self.BLOCK_WIDTH = (self.setting.WIDTH//self.setting.N)*(0.3)
        self.BLOCK_HEIGHT = (self.setting.HEIGHT//self.setting.N)*(0.3)


    def rot90(self, matrix):
        '''Rotates the given matrix 90 degree and returns it'''
        return [list(reversed(row)) for row in zip(*matrix)]

    def rot180(self, matrix):
        return self.rot90(self.rot90(matrix))

    def rot270(self, matrix):
        return self.rot180(self.rot90(matrix))

    def push_right(self):
        self.control_moves = 0
        for col in range(self.setting.N - 2,-1, -1):
            for row in self.grid:
                if row[col] == row[col+1] and row[col + 1] != 0 :
                        row[col], row[col + 1] = row[col]*2 , 0
                
                elif row[col + 1] == 0:
                    row[col], row[col + 1] = 0, row[col]
                    if self.control_moves == 0:
                        self.moves += 1
                        self.control_moves = 1

    def right(self):
        self.push_right()
        self.update()

    def left(self):
        self.grid = self.rot180(self.grid)
        self.push_right()
        self.grid = self.rot180(self.grid)
        self.update()

    def up(self):
        self.grid = self.rot90(self.grid)
        self.right()
        self.grid = self.rot270(self.grid)
        self.update()

    def down(self):
        self.grid = self.rot270(self.grid)
        self.push_right()
        self.grid = self.rot90(self.grid)
        self.update()

    def game_state(self):
        if self.setting.end:
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == self.setting.end:
                        return 'WIN'
                    
                    
            for row in range(len(self.grid)):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == 0:
                        return 'BLOCK AVAILABLE'


            for row in range(len(self.grid)):
                for col in range(len(self.grid[row]) - 1):
                    if self.grid[row][col] == self.grid[row][col + 1]:
                        return 'CAN MERGE'

            for row in range(len(self.grid) - 1):
                for col in range(len(self.grid[row])):
                    if self.grid[row][col] == self.grid[row + 1][col]:
                        return 'CAN MERGE'
                
                

        return 'LOSE'

    def add_block(self):
        free_blocks = [(y, x) for y, row in enumerate(self.grid) for x, num in enumerate(row) if num == 0]
        y, x = choice(free_blocks)
        self.grid[y][x] = choice([2,4])

    def update(self) :
        state = self.game_state()
        if state == 'WIN':
            self.game_over(True)
        elif state == 'LOSE':
            self.game_over(False)
        elif state == 'BLOCK AVAILABLE':
            self.add_block()

    def game_over(self, is_win) :
        self.draw_win()
        if is_win:
            label = self.setting.GAME_OVER_FONT.render(f'You won! Your moves: {self.moves} ', 1, self.setting.BLUE)
        else:
            label = self.setting.GAME_OVER_FONT.render(f'You lost! your moves: {self.moves}', 1,self.setting.RED)
        self.window.blit(label, (self.setting.WIDTH//2 - label.get_width()//2, 
            self.setting.HEIGHT//2 - label.get_height()//2))
        pygame.display.update()
        pygame.time.delay(3000)
        self.setting.game_deactive = True
        self.main_menu()
        
       
        

    def draw_win(self):
        self.window.blit(self.setting.bg_game_img, (0,0))
        self.draw_grid()
        self.draw_stats()

    def draw_grid(self):
        pygame.draw.rect(self.window, self.setting.BG_COLOR,
            (self.setting.LEFT - self.setting.GAP, self.setting.TOP - self.setting.GAP, len(self.grid[0]) * (self.BLOCK_WIDTH + self.setting.GAP) + self.setting.GAP, 
            len(self.grid) * (self.BLOCK_HEIGHT + self.setting.GAP) + self.setting.GAP))
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                x = self.setting.LEFT + (col * (self.BLOCK_WIDTH + self.setting.GAP))
                y = self.setting.TOP + (row * (self.BLOCK_HEIGHT + self.setting.GAP))
                value = self.grid[row][col]
                bg_color, font_color = self.setting.COLOR_MAP[value]
                color_rect = pygame.Rect(x, y, self.BLOCK_WIDTH, self.BLOCK_HEIGHT)
                pygame.draw.rect(self.window, bg_color, color_rect)

                if value != 0:
                    label = self.setting.BLOCK_FONT.render(str(value), 1, font_color)
                    font_rect = label.get_rect()
                    font_rect.center = color_rect.center
                    self.window.blit(label, font_rect)

    def draw_stats(self):
        label = self.setting.TITLE_FONT.render(f'2048', 1, self.setting.WHITE)
        self.window.blit(label, (150, 5))

        label = self.setting.STATS_FONT.render(f'moves: {self.moves}', 1, self.setting.WHITE)
        self.window.blit(label, (450, 5))
        
        label = self.setting.STATS_FONT.render(f'your aim: {self.setting.end}', 1, self.setting.WHITE)
        self.window.blit(label, (450, 50))
        
        label = self.setting.CREATOR_FONT.render("@ra.phi", 1, self.setting.WHITE)
        self.window.blit(label, (450, 350))

            
    def rungame(self):
        if not self.setting.game_deactive:
            self.init_variables()
            while self.running:
                self.draw_win()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                        
                    if event.type == KEYDOWN:
                        if event.key in [K_LEFT]:
                            self.left()
                        if event.key in [K_RIGHT]:
                            self.right()
                        if event.key in [K_UP]:
                            self.up()
                        if event.key in [K_DOWN]:
                            self.down()
        else:
            self.main_menu()
            

    def main_menu(self) :
        
        while self.setting.game_deactive :
            self.window.blit(self.setting.bg_menu_img, (0,0))
            self.PlayButton.draw()
            self.hardship512.draw()
            self.hardship1024.draw()
            self.hardship2048.draw()
            self.inputNumberCaption.draw()
            self.oInputNumber.draw()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if self.PlayButton.handleEvent(event):
                    self.setting.game_deactive = False
                    self.rungame()
                elif self.hardship512.handleEvent(event):
                    self.setting.end = 512
                elif self.hardship1024.handleEvent(event):
                    self.setting.end = 1024
                elif self.hardship2048.handleEvent(event):
                    self.setting.end = 2048
                elif self.oInputNumber.handleEvent(event):
                    self.setting.N = self.oInputNumber.getValue()
                    self.update_block()
                    self.setting.update_block_font()
                    