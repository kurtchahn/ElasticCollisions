## Kurt Hahn
## 17 November 2023
## PHYS 225 Introduction to Computational Physics and Programming
## Final Project - Elastic Collisions


import pygame
import math
import numpy as np
import random


## You can change these:

TITLE = "Elastic Collisions"
MUSIC = True
SOUNDEFFECTS = True
EPILEPSY = True

ACCELERATIONFACTOR = 1


## Source Code:

WINDOWWIDTH, WINDOWHEIGHT = 1200, 600
TIMEDELAY = 1 #milliseconds
DELTAT = 0.001
COLORCHANGEFRAMEDELAY = 400

G = 9.8 * ACCELERATIONFACTOR
DAMPINGCOEFF = 1

WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (240, 240, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
PURPLE = (75, 0, 130)
BLACK = (0, 0, 0)
MAGENTA = (180, 29, 245)

CENTER = (WINDOWWIDTH // 2, WINDOWHEIGHT // 2)
YMARGIN = 0
XMARGIN = 0

MUSIC = "nyan_cat.mp3"
SOUNDEFFECT = "oof.mp3"


class Ball():

    def __init__(self, window, x0, y0, vx0, vy0, radius, mass, color):

        self.window = window
        self.xPos = x0 #meters
        self.yPos = y0

        self.xVel = vx0 #meters per second
        self.yVel = vy0

        self.COLOR = color
        self.MASS = mass #kilograms
        self.RADIUS = radius

    def draw_ball(self):

        pygame.draw.circle(self.window, self.COLOR,
                           (self.xPos, WINDOWHEIGHT - self.yPos),
                           self.RADIUS)

    def set_next_frame_velocities(self):

        if self.yPos < YMARGIN + self.RADIUS:
            self.yVel *= -DAMPINGCOEFF
            self.yPos = YMARGIN + self.RADIUS
        elif self.yPos > (WINDOWHEIGHT - YMARGIN - self.RADIUS):
            self.yVel *= -DAMPINGCOEFF
            self.yPos = WINDOWHEIGHT - YMARGIN - self.RADIUS
        else:
            self.yVel -= G * DELTAT

        if self.xPos < XMARGIN + self.RADIUS:
            self.xVel *= -DAMPINGCOEFF
            self.xPos = XMARGIN + self.RADIUS
        elif self.xPos > (WINDOWWIDTH - XMARGIN - self.RADIUS):
            self.xVel *= -DAMPINGCOEFF
            self.xPos = WINDOWWIDTH - XMARGIN - self.RADIUS
        else:
            self.xVel += 0

    def set_next_frame_positions(self):
        self.xPos += self.xVel * DELTAT
        self.yPos += self.yVel * DELTAT

    def update_graphic(self):
        self.set_next_frame_velocities()
        self.set_next_frame_positions()
        self.draw_ball()

    def find_distance(ball1, ball2):
        return math.sqrt((ball1.xPos - ball2.xPos)**2 + (ball1.yPos - ball2.yPos)**2)

    def check_for_collision(ball1, ball2):
        if Ball.find_distance(ball1, ball2) < (ball1.RADIUS + ball2.RADIUS):
            return True
        else:
            return False

    ## I pulled this load of garbage from Wikipedia
    ## https://en.wikipedia.org/wiki/Elastic_collision
    def calculate_velocities_after_collision(ball1, ball2):
        m1 = ball1.MASS
        m2 = ball2.MASS

        v1 = math.sqrt(ball1.xVel**2 + ball1.yVel**2)
        v2 = math.sqrt(ball2.xVel**2 + ball2.yVel**2)

        # Movement Angles
        theta1 = math.atan2(ball1.yVel, ball1.xVel)
        theta2 = math.atan2(ball2.yVel, ball2.xVel)

        # Contact Angle
        phi = math.atan2(ball2.yPos - ball1.yPos, ball2.xPos - ball1.xPos)

        v1LargeCalc = (v1*math.cos(theta1-phi)*(m1-m2)+2*m2*v2*math.cos(theta2-phi))/(m1+m2)
        v1SmallCalc = v1*math.sin(theta1-phi)

        new_xVel1 = v1LargeCalc*math.cos(phi) + v1SmallCalc*math.cos(phi+np.pi/2)
        new_yVel1 = v1LargeCalc*math.sin(phi) + v1SmallCalc*math.sin(phi+np.pi/2)

        v2LargeCalc = (v2*math.cos(theta2-phi)*(m2-m1)+2*m1*v1*math.cos(theta1-phi))/(m2+m1)
        v2SmallCalc = v2*math.sin(theta2-phi)

        new_xVel2 = v2LargeCalc * math.cos(phi) + v2SmallCalc * math.cos(phi + np.pi / 2)
        new_yVel2 = v2LargeCalc * math.sin(phi) + v2SmallCalc * math.sin(phi + np.pi / 2)

        ball1.xVel = new_xVel1 * DAMPINGCOEFF
        ball1.yVel = new_yVel1 * DAMPINGCOEFF
        ball2.xVel = new_xVel2 * DAMPINGCOEFF
        ball2.yVel = new_yVel2 * DAMPINGCOEFF


class Main():
    
    def main():

        pygame.init()

        WINDOW = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption(TITLE)

        icon = pygame.image.load('image1.png')
        pygame.display.set_icon(icon)

        collisionSound = pygame.mixer.Sound(SOUNDEFFECT)
        collisionSound.set_volume(1)
        pygame.mixer.music.load(MUSIC)
        pygame.mixer.music.set_volume(1)

        if MUSIC:
            pygame.mixer.music.play(-1)

        ball1 = Ball(WINDOW, CENTER[0], CENTER[1], 100, 100, 15, 15, RED)
        ball2 = Ball(WINDOW, 200, 200, -1000, 1000, 5, 5, BLUE)
        ball3 = Ball(WINDOW, 100, 100, -50, 50, 30, 30, GREEN)
        ball4 = Ball(WINDOW, 700, 600, 500, 500, 10, 10, WHITE)
        ball5 = Ball(WINDOW, 350, 350, 600, -600, 10, 10, PURPLE)
        ball6 = Ball(WINDOW, 400, 400, 700, -700, 50, 50, ORANGE)
        ball7 = Ball(WINDOW, 550, 500, 0, 0, 100, 100, MAGENTA)
        ball8 = Ball(WINDOW, 100, 800, -20, 20, 70, 70, BLACK)

        ballSet = [ball1, ball2, ball3, ball4, ball5, ball6, ball7, ball8]

        frameCount = 0
        frameWindowColor = (100, 100, 100)

        run = True
        while run:
            pygame.time.delay(TIMEDELAY)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            for i in range(len(ballSet)):
                for j in range(i+1, len(ballSet)):
                    if Ball.check_for_collision(ballSet[i], ballSet[j]):
                        if EPILEPSY:
                            color1 = ballSet[i].COLOR
                            ballSet[i].COLOR = ballSet[j].COLOR
                            ballSet[j].COLOR = color1
                        if SOUNDEFFECTS:
                            pygame.mixer.Sound.play(collisionSound)
                        Ball.calculate_velocities_after_collision(ballSet[i], ballSet[j])

            if frameCount % COLORCHANGEFRAMEDELAY == 0 and EPILEPSY:
                frameWindowColor = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

            WINDOW.fill(frameWindowColor)

            for ball in ballSet:
                ball.update_graphic()

            pygame.display.update()
            frameCount += 1

        pygame.quit()


if __name__ == "__main__":
    Main.main()