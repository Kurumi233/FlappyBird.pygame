import sys
import pygame
import random
from utils.utils import load_config
from instance import Bird, PipeLine


def handle_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not bird.dead:
            bird.is_flapped = True
            bird.reset_speed()


def CheckGameOver():
    upRect = pygame.Rect(pipe.pos_x, pipe.top_pos_y, pipe.top.get_width() - 10, pipe.top.get_height())
    downRect = pygame.Rect(pipe.pos_x, pipe.bottom_pos_y, pipe.bottom.get_width() - 10, pipe.bottom.get_height())
    birdRect = pygame.Rect(bird.pos_x, bird.pos_y, bird.status_img[bird.status].get_width(), bird.status_img[bird.status].get_height())

    if upRect.colliderect(birdRect) or downRect.colliderect(birdRect):
        bird.dead = True
        return True

    return bird.dead


def createScene():
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    # PipeLine
    screen.blit(pipe.top, (pipe.pos_x, pipe.top_pos_y))
    screen.blit(pipe.bottom, (pipe.pos_x, pipe.bottom_pos_y))
    pipe.update()
    # Bird
    if bird.dead:
        bird.status = 2
    elif bird.is_flapped:
        bird.status = 1
    screen.blit(bird.status_img[bird.status], (bird.pos_x, bird.pos_y))
    bird.update()

    screen.blit(font.render('score: {}'.format(score), True, (255, 255, 255)), (10, 10))

    pygame.display.update()  # 更新显示


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    score = 0
    fps = 60

    SIZE = (400, 640)
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Flappy Bird')

    bird = Bird(init_pos=(120, 350), screen_size=SIZE)
    pipe = PipeLine(screen_size=SIZE)
    background = pygame.image.load('src/bg.png')

    clock = pygame.time.Clock()

    while True:
        clock.tick(fps)
        handle_event()

        if CheckGameOver():
            print('hint')
        createScene()





