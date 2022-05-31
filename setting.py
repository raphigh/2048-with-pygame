import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()


class Setting:
    def __init__(self):
        
        #N = blocks in each row and column
        self.N = 4
        
        #hardship
        self.end = 16
        
        #windwos setting
        self.WIDTH = 750
        self.HEIGHT = 750
        self.CAPTION = '2048'
        
        #grid setting
        self.TOP = 125
        self.LEFT = 50
        self.GAP = 7
        
        
        #font setting
        self.TITLE_FONT = pygame.font.SysFont('arial', 75)
        self.BLOCK_FONT = pygame.font.SysFont('arial', 25)
        self.STATS_FONT = pygame.font.SysFont('arial', 40)
        self.CREATOR_FONT = pygame.font.SysFont('arial',80)
        self.GAME_OVER_FONT = pygame.font.SysFont('arial', 45)
        
       #colors
        self.BLACK = '#000000'
        self.WHITE = '#ffffff'
        self.BLUE =  '#0000ff'
        self.RED =   '#ff0000'
        
        self.BG_COLOR = '#bbada0'
        self.bg_menu_img = pygame.image.load("img/bg.jpg")
        self.bg_game_img = pygame.image.load("img/bg_game.jpg")
        
        self.COLOR_MAP = {
            0:     ('#CCC0B4', None),
            2:     ('#eee4da', '#776e65'),
            4:     ('#ede0c8', '#776e65'),
            8:     ('#f2b179', '#f9f6f2'),
            16:    ('#f59563', '#f9f6f2'),
            32:    ('#f67c5f', '#f9f6f2'),
            64:    ('#f65e3b', '#f9f6f2'),
            128:   ('#edcf72', '#f9f6f2'),
            256:   ('#edcc61', '#f9f6f2'),
            512:   ('#edc850', '#f9f6f2'),
            1024:  ('#edc53f', '#f9f6f2'),
            2048:  ('#edc22e', '#f9f6f2')
        }
        
        
        #activity
        self.game_deactive = True
    def update_block_font(self):
        self.BLOCK_FONT = pygame.font.SysFont('arial', (25//(self.N))*4)
        
        