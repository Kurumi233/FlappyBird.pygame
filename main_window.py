import sys
import pygame
from utils.utils import load_config
from instance import Bird, PipeLine, GameBackGround, Button


class MainScene(object):
    def __init__(self, args):
        # 初始化环境
        self._init_env()
        # 创建场景实例
        self.width, self.height = args['width'], args['height']
        self.size = (self.width, self.height)
        self.scene = pygame.display.set_mode(self.size)
        self.font = pygame.font.SysFont(args['font'], args['font_size'])
        pygame.display.set_caption(args['caption'])
        # fps
        self.clock = pygame.time.Clock()
        self.fps = args['fps']
        # 暂停
        self.pause = False
        self.pause_button = Button(scene=self.scene, font=self.font, text='PAUSE', pos=(300, 10))
        # 创建实例对象
        self.map = GameBackGround(scene=self.scene, speed=args['speed'])
        self.pipe = PipeLine(scene=self.scene, speed=args['speed'])
        self.bird = Bird(init_pos=(120, 350), scene=self.scene)
        # Start
        self.ready = False
        self.ready_scene = pygame.image.load('src/start.png')
        # GameOver
        self.gg = False
        self.gg_scene = pygame.image.load('src/gameover.png')

    def _init_env(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

    def draw_elements(self):
        self.map.draw()
        self.pipe.draw()
        self.bird.draw()
        self.pause_button.draw()
        self.scene.blit(self.font.render('Score: {}   FPS: {}'.format(self.pipe.score, self.fps), True, (255, 255, 255)), (10, 10))
        if self.gg:
            self.scene.blit(self.gg_scene, (0, 0))

    def action(self):
        self.map.update()
        self.pipe.update()
        self.bird.update()
        if self.collision_detection():
            self.gg = True
            self.ready = False

    def collision_detection(self):
        rect1 = pygame.Rect(self.pipe.x, self.pipe.y1, self.pipe.top.get_width(), self.pipe.top.get_height())
        rect2 = pygame.Rect(self.pipe.x, self.pipe.y2, self.pipe.bottom.get_width(), self.pipe.bottom.get_height())
        birdrect = pygame.Rect(self.bird.x, self.bird.y, self.bird.status_img[self.bird.status].get_width(), self.bird.status_img[self.bird.status].get_height())

        if rect1.colliderect(birdrect) or rect2.colliderect(birdrect):
            return True
        return False

    def _reset(self):
        self.map.reset()
        self.pipe.reset()
        self.bird.reset()

    def _handle_event(self):
        if not self.ready or self.gg:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ready = True
                    self.gg = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.is_clicked(pygame.mouse.get_pos()):
                        self.pause = not self.pause
                    else:
                        self.bird.is_flapped = True
                        self.bird.reset_speed()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.pause = not self.pause
                    elif event.key in [pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT]:
                        self.bird.is_flapped = True
                        self.bird.reset_speed()

    def start(self):
        while not self.ready:
            self.map.draw()
            self.scene.blit(self.ready_scene, (0, 0))
            self._handle_event()
            pygame.display.update()
            self.clock.tick(self.fps)
        self.run()

    def end(self):
        while not self.ready:
            self.map.draw()
            self.scene.blit(self.gg_scene, (0, 0))
            self._handle_event()
            pygame.display.update()
            self.clock.tick(self.fps)
        self._reset()
        self.start()

    def run(self):
        while not self.gg:
            self.draw_elements()
            self._handle_event()
            if not self.pause:
                self.action()
            pygame.display.update()
            self.clock.tick(self.fps)
        self.ready = False
        self.end()


if __name__ == '__main__':
    args = load_config()
    mainScene = MainScene(args)
    mainScene.start()
