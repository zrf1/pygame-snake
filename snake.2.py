# -*- coding: utf-8 -*-
'''
1、创建蛇身精灵
2、创建小蛇类（继承自group）
3、小蛇的初始化
'''

import pygame                   # 导入pygame库
from pygame.locals import *     # 导入pygame库中的一些常量
from sys import exit            # 导入sys库中的exit函数
from random import randint

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480                              # 定义窗口的分辨率
clock = pygame.time.Clock()                                         # 时钟，用于设置游戏帧率

# 初始化
pygame.init()                                                       # 初始化pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])     # 初始化窗口
pygame.display.set_caption('贪吃蛇')                                # 设置窗口标题

start_img = pygame.image.load('res/start.jpg')                      # 开始图
back_img = pygame.image.load('res/back.jpg')                        # 背景图


##############################################################


# 定义一些常量
GRID_SIZE = 20                  # 格子大小
X_MAX = SCREEN_WIDTH / GRID_SIZE
Y_MAX = SCREEN_HEIGHT / GRID_SIZE
# 四个运动方向
DIRE_LEFT, DIRE_RIGHT, DIRE_UP, DIRE_DOWN = [-1, 0], [1, 0], [0, -1], [0, 1]


class SnakeBlock(pygame.sprite.Sprite):
    '蛇身 精灵'
    OUTER_RECT = pygame.Rect(0, 0, 20, 20)
    INNER_RECT = pygame.Rect(4, 4, 12, 12)
    OUTER_COLOR = (0, 0, 255)
    INNER_COLOR = (173, 216, 230)

    def __init__(self, x, y):
        super().__init__()
        # 绘制蛇身
        surface = pygame.Surface([GRID_SIZE, GRID_SIZE])
        pygame.draw.rect(surface, self.OUTER_COLOR, self.OUTER_RECT)
        pygame.draw.rect(surface, self.INNER_COLOR, self.INNER_RECT)
        # 初始化
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = [GRID_SIZE * x, GRID_SIZE * y]
        # 蛇身运动方向
        self.direction = DIRE_RIGHT

    def update(self):
        self.rect.left += GRID_SIZE * self.direction[0]
        self.rect.top += GRID_SIZE * self.direction[1]


class Snake(pygame.sprite.Group):
    '小蛇 组'

    def __init__(self):
        '初始化，创建三节蛇身'
        super().__init__()
        self.add(SnakeBlock(X_MAX/2, Y_MAX/2))
        self.add(SnakeBlock(X_MAX/2 - 1, Y_MAX/2))
        self.add(SnakeBlock(X_MAX/2 - 2, Y_MAX/2))

    def __del__(self):
        '析构函数'
        self.empty()


##############################################################


# 游戏状态：0 开始，1 游戏，2 失败
state_index = 0
speed = 5
snake = None

# 事件循环(main loop)
while True:
    clock.tick(speed)      # 游戏帧率（也是小蛇的运行速度）

    # 处理游戏退出,从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if state_index in [0, 2]:
                    # 开始游戏，初始化小蛇
                    state_index = 1
                    speed = 5
                    del snake   # 清空原有小蛇
                    snake = Snake()

    if state_index == 0:
        screen.blit(start_img, (0, 0))    # 绘制背景
    elif state_index == 2:
        '提示Failed！'
    else:
        # 正常游戏时
        screen.blit(back_img, (0, 0))
        snake.update()
        snake.draw(screen)

    # 更新屏幕
    pygame.display.update()     # 更新屏幕
