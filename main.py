import pygame

from Rocket import Rocket
from Space import Space

pygame.init()

width = 550
height = 650

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space flight")

isRunning = True

FPS = 60
fpsClock = pygame.time.Clock()
started = False

rocket = Rocket(win, 4)
space = Space(win, 300)

delay = 0

fuelUpdateEvent = pygame.USEREVENT + 1
fuelSetupEvent = pygame.USEREVENT + 2
asteroidSetupEvent = pygame.USEREVENT + 3
scoreUpdateEvent = pygame.USEREVENT + 4

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)


def start():
    global started
    started = True

    rocket.restart()

    rocket.started = True

    pygame.time.set_timer(fuelUpdateEvent, 1)
    pygame.time.set_timer(fuelSetupEvent, 2000)
    pygame.time.set_timer(asteroidSetupEvent, 1500)
    pygame.time.set_timer(scoreUpdateEvent, 1000)


while isRunning:
    pygame.time.delay((1000 // FPS) - delay)

    win.fill((0, 0, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYUP:
            if not started:
                start()
        elif event.type == pygame.MOUSEBUTTONUP:
            if not started:
                start()
            else:
                rocket.click(pygame.mouse.get_pos())
                # if result:
                #     pygame.time.set_timer(timerSetupEvent, 4000)
        elif not started:
            pass
        elif event.type == fuelUpdateEvent:
            status = rocket.update()
            if not status:
                rocket.fuelPosition = (-rocket.fuelSize[0], -rocket.fuelSize[1])
                rocket.asteroidPosition = (-rocket.asteroidSize[0], -rocket.asteroidSize[1])
                started = False
        elif event.type == fuelSetupEvent:
            rocket.setFuel()
        elif event.type == asteroidSetupEvent:
            rocket.setAsteroid()
        elif event.type == scoreUpdateEvent:
            rocket.score += 1

    scoreSurface = font.render(str(rocket.score), False, (255, 255, 255))

    space.draw()

    rocket.drawFuelTank()
    rocket.draw()
    rocket.drawButton()

    win.blit(scoreSurface, ((width - scoreSurface.get_width())/2, 5))

    pygame.display.update()
    delay = fpsClock.tick(FPS)

pygame.quit()
