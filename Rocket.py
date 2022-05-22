import math
from random import randint

import pygame


def drawStyleRect(win, color, borderColor, x, y, width, height):
    pygame.draw.rect(win, color, (x, y, width, height), 0)
    for i in range(4):
        pygame.draw.rect(win, borderColor, (x - i, y - i, width, height), 1)


class Rocket:
    fuelPercentage = 1
    fuelConsumption = 0.00005
    tankWidth = 40
    tankHeight = 200
    score = 0
    started = False

    def __init__(self, win, stageCount):
        self.win = win

        self.score = 0

        self.clock = pygame.time.Clock()

        self.rocketImg = pygame.image.load('assets/Rocket.png')
        self.flameImg = pygame.image.load('assets/Flame.png')
        self.fuelImg = pygame.image.load('assets/Fuel.png')
        self.asteroidImg = pygame.image.load('assets/Asteroid.png')

        self.winSize = list(self.win.get_size())
        self.rocketSize = list(self.rocketImg.get_size())
        self.flameSize = list(self.flameImg.get_size())
        self.fuelSize = list(self.fuelImg.get_size())
        self.asteroidSize = list(self.asteroidImg.get_size())

        self.fuelPosition = list((-self.asteroidSize[0], -self.asteroidSize[1]))
        self.asteroidPosition = list((-self.fuelSize[0], -self.fuelSize[1]))
        self.tankPosition = list(
            (self.winSize[0] - self.tankWidth - 10,
             (self.winSize[1] - self.tankHeight) / 2)
        )
        self.rocketPosition = list(
            ((self.winSize[0] - self.rocketSize[0]) / 2,
             (self.winSize[1] - self.rocketSize[1]) / 2)
        )
        self.flamePosition = list(
            ((self.winSize[0] - self.flameSize[0]) / 2,
             self.rocketPosition[1] + self.rocketSize[1] - 10)
        )

    def restart(self):
        self.fuelPosition = list((-self.fuelSize[0], -self.fuelSize[1]))
        self.asteroidPosition = (-self.asteroidSize[0], -self.asteroidSize[1])
        self.score = 0
        self.started = False
        self.clock = pygame.time.Clock()
        self.fuelPercentage = 1
        self.fuelConsumption = 0.00005

    def update(self):
        if self.score != 0:
            self.fuelConsumption = (self.score ** 0.2) / 10000

        if self.fuelConsumption >= 0.01:
            self.fuelConsumption = 0.01

        self.fuelPercentage -= self.fuelConsumption

        if self.fuelPercentage <= 0:
            self.started = False
            self.fuelPercentage = 0
            return False
        return True

    def addFuel(self):
        self.fuelPercentage += 10 / math.sqrt(self.clock.tick())
        self.fuelPosition = list((-self.fuelSize[0], -self.fuelSize[1]))

        if self.fuelPercentage >= 1:
            self.fuelPercentage = 1
        self.score += 3

    def removeFuel(self):
        self.asteroidPosition = list((-self.asteroidSize[0], -self.asteroidSize[1]))

        self.fuelPercentage -= 0.15

    def click(self, pos):
        if self.fuelPosition[0] < pos[0] < self.fuelPosition[0] + self.fuelSize[0]:
            if self.fuelPosition[1] < pos[1] < self.fuelPosition[1] + self.fuelSize[1]:
                self.addFuel()

        if self.asteroidPosition[0] < pos[0] < self.asteroidPosition[0] + self.asteroidSize[0]:
            if self.asteroidPosition[1] < pos[1] < self.asteroidPosition[1] + self.asteroidSize[1]:
                self.removeFuel()

    def setAsteroid(self):
        self.asteroidPosition = (
            randint(10, self.rocketPosition[0] - self.asteroidSize[0] - 10),
            randint(20, self.winSize[1] - self.asteroidSize[1] - 20))

        if (self.fuelPosition[0] - self.asteroidPosition[0]) ** 2 + (
                self.fuelPosition[1] - self.asteroidPosition[1]) ** 2 < self.fuelSize[0] ** 2 + self.fuelSize[1] ** 2:
            self.setAsteroid()

    def setFuel(self):
        self.clock.tick()

        self.fuelPosition = (
            randint(10, self.rocketPosition[0] - self.fuelSize[0] - 10),
            randint(20, self.winSize[1] - self.fuelSize[1] - 20))

        if (self.fuelPosition[0] - self.asteroidPosition[0]) ** 2 + (
                self.fuelPosition[1] - self.asteroidPosition[1]) ** 2 < self.fuelSize[0] ** 2 + self.fuelSize[1] ** 2:
            self.setFuel()

    def drawFuelTank(self):
        if self.fuelPercentage == 1:
            shortage = 0
        else:
            shortage = self.tankHeight * (1 - self.fuelPercentage)

        color = (255, 0, 0)

        if self.fuelPercentage > 0.33:
            color = (255, 255, 0)

        if self.fuelPercentage > 0.66:
            color = (0, 200, 0)

        pygame.draw.rect(self.win, color,
                         (self.tankPosition[0], self.tankPosition[1], self.tankWidth,
                          self.tankHeight))

        pygame.draw.rect(self.win, (150, 150, 150),
                         (self.tankPosition[0], self.tankPosition[1], self.tankWidth, shortage))

        pygame.draw.rect(self.win,
                         (100, 100, 100),
                         (self.tankPosition[0], self.tankPosition[1], self.tankWidth, self.tankHeight), 3)

    def drawButton(self):
        self.win.blit(self.fuelImg, self.fuelPosition)
        self.win.blit(self.asteroidImg, self.asteroidPosition)

    def draw(self):
        self.win.blit(self.rocketImg, self.rocketPosition)
        if self.started:
            self.win.blit(self.flameImg, self.flamePosition)
        # for i in range(1, self.stageCount):
        #     drawStyleRect(self.win,
        #                   (150, 150, 150),
        #                   (100, 100, 100),
        #                   (self.winWidth - self.stageWidth) / 2,
        #                   (self.win.get_height() - self.height) / 2 + self.stageHeight * i,
        #                   self.stageWidth,
        #                   self.stageHeight)
