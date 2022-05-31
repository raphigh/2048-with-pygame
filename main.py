from game import *

import pygame
from pygame.locals import *
from random import choice

pygame.init()
pygame.font.init()

if __name__ == '__main__':
    ogame = MyGame()
    ogame.rungame()