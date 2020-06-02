import pygame
import numpy as np

class Obstacle:
    def __init__(self,coords,shape,sprite = None):
        self.coords = np.array(coords)
        self.shape = shape
        self.sprite = pygame.image.load("Game/assets/wall.jpg")
    def get_coords(self):
        return self.coords
    def set_coords(self,coords):
        self.coords = np.array(coords)
    def get_shape(self):
        return self.shape
    def get_rect(self):
        return pygame.Rect(*self.coords,*self.shape)

    def render(self,window):
        window.blit(pygame.transform.scale(self.sprite,self.shape),self.get_rect())
