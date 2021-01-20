import pygame
import random


class Bird(object):
    def __init__(self, init_pos, scene):
        self.init_pos = init_pos
        self.x, self.y = init_pos
        self.scene = scene
        self.right, self.bottom = self.scene.get_size()

        self.size = pygame.image.load('src/0.png').get_size()

        self.status = 0
        self.status_img = [pygame.image.load('src/%d.png' % x) for x in range(8)]

        # 飞行变量
        self.is_flapped = False
        self.upspeed = 10
        self.downspeed = 10
        self.times = 0

    def update(self):
        if self.is_flapped:
            self.y -= self.upspeed
            self.upspeed -= 1
        else:
            self.y += self.downspeed
            self.downspeed += 0.2

        self.times += 1
        if self.times % 5 == 0:
            self.status = (self.status + 1) % 8

        self.collision_detection()

    def collision_detection(self):
        if self.y < 0:
            self.y = 0
        if self.y > self.bottom - self.size[1]:
            self.y = self.bottom - self.size[1]

    def reset_speed(self):
        self.upspeed = 10
        self.downspeed = 10

    def reset(self):
        self.x, self.y = self.init_pos
        self.status = 0
        self.times = 0

    def draw(self):
        self.scene.blit(self.status_img[self.status], (self.x, self.y))


class PipeLine(object):
    def __init__(self, scene, passageway=180, speed=2):
        self.scene = scene
        self.max_w, self.max_h = self.scene.get_size()
        self.passageway = passageway

        self.top = pygame.image.load('src/top.png')
        self.bottom = pygame.image.load('src/bottom.png')

        self.size1 = self.top.get_size()
        self.size2 = self.bottom.get_size()

        self.x = self.max_w
        self.y1, self.y2 = 0, 0
        self.rand_pos_y()

        self.speed = speed
        self.score = 0

    def update(self):
        self.x -= self.speed
        if self.x < -self.size1[0]:
            self.x = self.max_w
            self.rand_pos_y()
            self.score += 1

    def rand_pos_y(self):
        self.y2 = random.randint(self.passageway + 60, self.max_h - 60)
        self.y1 = self.y2 - self.passageway - self.size1[1]

    def reset(self):
        self.x = self.max_w
        self.rand_pos_y()
        self.score = 0

    def draw(self):
        self.scene.blit(self.top, (self.x, self.y1))
        self.scene.blit(self.bottom, (self.x, self.y2))


class GameBackGround(object):
    def __init__(self, scene, speed=2):
        self.scene = scene
        self.max_w, self.max_h = self.scene.get_size()

        self.bg1 = pygame.image.load('src/bg.png')
        self.bg2 = pygame.image.load('src/bg.png')

        self.x1 = 0
        self.x2 = self.max_w
        self.speed = speed

    def update(self):
        self.x1 = self.x1 - self.speed
        self.x2 = self.x2 - self.speed
        if self.x1 <= -self.max_w:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = self.max_w

    def reset(self):
        self.x1 = 0
        self.x2 = self.max_w

    def draw(self):
        self.scene.blit(self.bg1, (self.x1, 0))
        self.scene.blit(self.bg2, (self.x2, 0))


class Button(object):
    def __init__(self, scene, font, text, pos, color=(255, 255, 255)):
        self.scene = scene
        self.x, self.y = pos
        self.button = font.render(text, True, color)
        self.width, self.height = self.button.get_size()

    def is_clicked(self, mouse_pos):
        x_match = mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width
        y_match = mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height

        return x_match and y_match

    def draw(self):
        self.scene.blit(self.button, (self.x, self.y))
