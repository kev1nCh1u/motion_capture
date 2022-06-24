import pygame
import pygame.camera
from pygame.locals import *

pygame.init()
pygame.camera.init()

cam = pygame.camera.Camera("/dev/video0",(640,480))
cam.start()

image = cam.get_image()

import pygame
pygame.init()
w = 640
h = 480
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('cam')
TPImage = image
# coordinates of the image
x = 0
y = 0
screen.blit(TPImage, (x, y))
# paint screen one time
pygame.display.flip()
running = True
while (running): # loop listening for end of game
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
# loop over, quite pygame
pygame.quit()