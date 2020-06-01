import pygame
import numpy as np
class Obstacle:
    def __init__(self,coords,size):
        self.coords = np.array(coords)
        self.size = size
        self.sprite = None
    def get_coords(self):
        return self.coords
    def set_coords(self,coords):
        self.coords = np.array(coords)
    def get_rect(self):
        return pygame.Rect(*self.coords,*self.size)

    def render(self,window):
        return window
