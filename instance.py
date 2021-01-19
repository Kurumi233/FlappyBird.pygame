import pygame
import random


class Bird(object):
    def __init__(self, init_pos, screen_size):
        self.pos_x, self.pos_y = init_pos
        self.right, self.bottom = screen_size
        self.right -= 50
        self.bottom -= 50

        self.status = 0
        self.status_img = [pygame.image.load('src/%d.png' % x) for x in range(8)]

        # 飞行变量
        self.is_flapped = False
        self.upspeed = 10
        self.downspeed = 10

        # 游戏结束
        self.dead = False

    def update(self):
        if self.is_flapped:
            self.pos_y -= self.upspeed
            self.upspeed -= 1
        else:
            self.pos_y += self.downspeed
            self.downspeed += 0.2

        self.collision_detection()

    def collision_detection(self):
        if self.pos_y < 0 or self.pos_y > self.bottom:
            self.dead = True
        else:
            self.dead = False

    def reset_speed(self):
        self.upspeed = 10
        self.downspeed = 10


class PipeLine(object):
    def __init__(self, screen_size, passageway=180):
        self.max_w, self.max_h = screen_size
        self.pos_x = self.max_w
        self.passageway = passageway
        self.rand_pos_y()

        self.speed = 2
        self.top = pygame.image.load('src2/top.png')
        self.bottom = pygame.image.load('src2/bottom.png')

    def update(self):
        self.pos_x -= self.speed
        if self.pos_x < -80:
            self.pos_x = 400
            self.rand_pos_y()

    def rand_pos_y(self):
        self.bottom_pos_y = random.randint(self.passageway + 60, self.max_h - 60)
        self.top_pos_y = self.bottom_pos_y - self.passageway - 500