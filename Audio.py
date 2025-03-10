import pygame as pg
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

pg.init()
pg.mixer.init()


class Audio:
    def __init__(self, path: str):
        self.path = path
        self.sound = pg.mixer.Sound(self.path)

    def play(self):
        self.sound.play()


if __name__ == '__main__':
    audio = Audio('assets/gun_sound.mp3')
    audio.play()
