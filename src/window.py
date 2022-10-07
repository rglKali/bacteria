import pygame as pg
from .engine import Engine
from .config import *


class Window:
    def __init__(self):
        self.screen = pg.display.set_mode(res)
        self.clock = pg.time.Clock()
        self.engine = Engine(self.screen)
        self.fps = list()

    def run(self):
        while True:
            self.screen.fill('black')
            self.engine.run()
            pg.display.flip()

            self.fps.append(round(self.clock.get_fps(), 2))
            pg.display.set_caption(f'FPS: {self.fps[-1]}')

            [self.exit() for ev in pg.event.get() if ev.type == pg.QUIT]

            if fps:
                self.clock.tick(fps)
            else:
                self.clock.tick()

    def exit(self):
        print(f'Average FPS: {round(sum(self.fps) / len(self.fps), 2)}')
        exit()
