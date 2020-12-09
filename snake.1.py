# -*- coding: utf-8 -*-
'''
1、游戏基本框架：初始化，加载资源，主循环，退出事件
2、实现游戏流程：开始，游戏，失败
'''

import pygame                   # 导入pygame库
from pygame.locals import *     # 导入pygame库中的一些常量
from sys import exit            # 导入sys库中的exit函数

# 定义窗口的分辨率
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FRAME_RATE = 60                 # 定义画面帧率
clock = pygame.time.Clock()

# 初始化
pygame.init()                                                       # 初始化pygame
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])     # 初始化窗口
pygame.display.set_caption('贪吃蛇')                                # 设置窗口标题

start_img = pygame.image.load('res/start.jpg')                      # 开始图
back_img = pygame.image.load('res/back.jpg')                        # 背景图

# 游戏状态：0 开始，1 游戏，2 失败
state_index = 0

# 事件循环(main loop)
while True:
    clock.tick(FRAME_RATE)      # 控制游戏最大帧率

    # 处理游戏退出,从消息队列中循环取
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state_index in [0, 2]:
                    state_index = 1

    # 绘制背景
    img = start_img if state_index==0 else back_img
    screen.blit(img, (0, 0))   # 绘制背景

    # 更新屏幕
    pygame.display.update()     # 更新屏幕
