# -*- coding: utf-8 -*-
'''
1、控制小蛇的运动
2、检测是否发生碰撞
3、游戏失败提示
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

# 图片资源
start_img = pygame.image.load('res/start.jpg')                      # 开始图
back_img = pygame.image.load('res/back.jpg')                        # 背景图
fail_img = pygame.image.load('res/fail.png')                        # 失败图


##############################################################


# 定义一些常量
GRID_SIZE = 20                  # 格子大小
X_MAX = SCREEN_WIDTH / GRID_SIZE
Y_MAX = SCREEN_HEIGHT / GRID_SIZE
# 四个运动方向
DIRE_LEFT, DIRE_RIGHT, DIRE_UP, DIRE_DOWN = [-1, 0], [1, 0], [0, -1], [0, 1]
KEY_DIRECTION = {pygame.K_LEFT: DIRE_LEFT, pygame.K_RIGHT: DIRE_RIGHT,
                 pygame.K_UP: DIRE_UP, pygame.K_DOWN: DIRE_DOWN}


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
        self.add(SnakeBlock(X_MAX/2 - 3, Y_MAX/2))
        self.add(SnakeBlock(X_MAX/2 - 4, Y_MAX/2))
        self.add(SnakeBlock(X_MAX/2 - 5, Y_MAX/2))
        self.add(SnakeBlock(X_MAX/2 - 6, Y_MAX/2))

    def __del__(self):
        '析构函数'
        self.empty()

    def SetDirection(self, direction):
        ''''
        设置方向。
        小蛇的运动方向 就是蛇头的运动方向'
        上下运动时才能向左/右，左右运动时才能向上/下
        '''
        st = self.sprites()[0]
        if direction in [DIRE_LEFT, DIRE_RIGHT] and st.direction in [DIRE_UP, DIRE_DOWN]:
            st.direction = direction
        elif direction in [DIRE_UP, DIRE_DOWN] and st.direction in [DIRE_LEFT, DIRE_RIGHT]:
            st.direction = direction

    def ChangeDirection(self):
        ''
        # 依次改变蛇身运动方向为上一段（第一段不变）
        pre_direction = DIRE_RIGHT          # 记录上一段蛇身的运动方向
        for (i, s) in enumerate(self):
            t = s.direction
            if i > 0:                       # 改为上一段蛇身的运动方向
                s.direction = pre_direction
            pre_direction = t

    def Collide(self):
        '检测是否发生碰撞'
        return self.CollideBox() or self.CollideSelf()

    def CollideBox(self):
        '检测是否碰撞边沿'
        rect = self.sprites()[0].rect
        return rect.left < 0 or rect.right > SCREEN_WIDTH or rect.top < 0 or rect.bottom > SCREEN_HEIGHT

    def CollideSelf(self):
        '检测是否碰撞自身'
        return len(pygame.sprite.spritecollide(self.sprites()[0], self, False)) > 1


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
            if state_index == 1 and event.key in KEY_DIRECTION:
                snake.SetDirection(KEY_DIRECTION[event.key])
                # if event.key == pygame.K_LEFT:
                #     snake.SetDirection(DIRE_LEFT)
                # elif event.key == pygame.K_RIGHT:
                #     snake.SetDirection(DIRE_RIGHT)
                # elif event.key == pygame.K_UP:
                #     snake.SetDirection(DIRE_UP)
                # elif event.key == pygame.K_DOWN:
                #     snake.SetDirection(DIRE_DOWN)

    if state_index == 0:
        screen.blit(start_img, (0, 0))    # 绘制背景
    elif state_index == 2:
        '游戏失败'
        # screen.blit(fail_img, (0, 0))
    else:
        # 正常游戏时
        screen.blit(back_img, (0, 0))
        snake.update()
        snake.draw(screen)
        snake.ChangeDirection()
        if snake.Collide():
            state_index = 2
            screen.blit(fail_img, (0, 0))    # 状态改变时运行一次即可

    # 更新屏幕
    pygame.display.update()     # 更新屏幕
