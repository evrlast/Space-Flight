import pygame
from random import randrange, randint


class Space:
    stars = []
    speed = 1

    def __init__(self, win, starsCount):
        self.win = win

        self.starsCount = starsCount

        self.width, self.height = self.win.get_size()
        self.starsSpawner()

    def starsSpawner(self):
        for x in range(self.starsCount):
            self.stars.append([randint(0, self.width), randint(0, self.height)])

    def draw(self):
        for star in self.stars:
            pygame.draw.line(self.win,
                             (255, 255, 255),
                             (star[0], star[1]), (star[0], star[1]))
            star[1] = star[1] + self.speed * (abs(randrange(10) - 5) + 5)/10
            if star[1] > self.height:
                star[1] = 0
                star[0] = randint(0, self.width)
