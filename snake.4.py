# -*- coding: utf-8 -*-
'''
1、随机产生食物（食物闪烁效果）
2、吃到食物（食物消失，再次产生食物）
3、小蛇增长（速度提升）
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
food_img = pygame.image.load('res/food.png')                        # 食物图
food_img2 = pygame.image.load('res/food2.png')                      # 食物图2


##############################################################


# 定义一些常量
GRID_SIZE = 20                  # 格子大小
X_MAX = SCREEN_WIDTH / GRID_SIZE
Y_MAX = SCREEN_HEIGHT / GRID_SIZE
# 四个运动方向
DIRE_LEFT, DIRE_RIGHT, DIRE_UP, DIRE_DOWN = [-1, 0], [1, 0], [0, -1], [0, 1]
KEY_DIRECTION = {pygame.K_LEFT: DIRE_LEFT, pygame.K_RIGHT: DIRE_RIGHT,
                 pygame.K_UP: DIRE_UP, pygame.K_DOWN: DIRE_DOWN}
SPEED_INC = 0.2


class SnakeBlock(pygame.sprite.Sprite):
    '蛇身 精灵'
    OUTER_RECT = pygame.Rect(0, 0, 20, 20)
    INNER_RECT = pygame.Rect(4, 4, 12, 12)
    OUTER_COLOR = (0, 0, 255)
    INNER_COLOR = (173, 216, 230)

    def __init__(self, x, y, direction=DIRE_RIGHT):
        super().__init__()
        self.x = x
        self.y = y
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
        self.x += self.direction[0]
        self.y += self.direction[1]
        self.rect.left = GRID_SIZE * self.x
        self.rect.top = GRID_SIZE * self.y


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

    def Eat(self, foods):
        '检测是否吃到食物。吃到时：在尾部添加蛇身，再次创建食物'
        if len(pygame.sprite.spritecollide(self.sprites()[0], foods, True)) > 0:
            t = self.sprites()[len(self.sprites()) - 1]  # 蛇尾
            x = t.x - t.direction[0]                     # 前一个位置
            y = t.y - t.direction[1]
            n = SnakeBlock(x, y, t.direction)
            self.add(n)
            foods.CreateFood(self)
            global speed
            speed += SPEED_INC


class Food(pygame.sprite.Sprite):
    '食物类'
    SHAN_SUO_COUNT = 20

    def __init__(self):
        super().__init__()
        self.image = food_img
        self.rect = self.image.get_rect()
        x = randint(1, X_MAX - 1)
        y = randint(1, Y_MAX - 1)
        self.rect.topleft = [GRID_SIZE * x, GRID_SIZE * y]
        self.img_n = 0
        self.ss_count = 0

    def update(self):
        '食物闪烁'
        self.ss_count += 1
        if (60 / speed) * self.ss_count > self.SHAN_SUO_COUNT:
            self.ss_count = 0
            if self.img_n == 0:
                self.image = food_img2
                self.img_n = 1
            else:
                self.image = food_img
                self.img_n = 0


class Foods(pygame.sprite.Group):
    '食物组'
    MAX_FOOD_COUNT = 3

    def CreateFood(self, snake):
        '新增食物。食物不能在蛇身上，也不能在现有食物上'
        while len(self) < self.MAX_FOOD_COUNT:
            f = Food()
            if pygame.sprite.spritecollideany(f, snake) == None \
                    and pygame.sprite.spritecollideany(f, self) == None:
                # 不冲突时，把食物加入组
                self.add(f)
            else:
                f.kill()


##############################################################


# 游戏状态：0 开始，1 游戏，2 失败
state_index = 0
speed = 5
snake = None
foods = Foods()

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
                    if len(foods) < 3:
                        foods.CreateFood(snake)
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
        foods.update()
        snake.Eat(foods)
        snake.draw(screen)
        foods.draw(screen)
        snake.ChangeDirection()
        # 是否碰撞
        if snake.Collide():
            state_index = 2
            screen.blit(fail_img, (0, 0))    # 状态改变时运行一次即可

    # 更新屏幕
    pygame.display.update()     # 更新屏幕
