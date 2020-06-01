import numpy as np
import pygame

class Agent:
    def __init__(self,size = (80,80),coords=(0,0)):
        self.coords = np.array(coords)
        self.size = size
        self.alive = True
        self.jump_counter = 0
        self.max_jump_counter = 10
        self.jump_speed = 3
        self.sprites = []
        self.sprite_animation_conunter = 0
        self.sprite_number = 5
        self.sprite_speed = 1
        pass

    def render(self,window):
        #render sprite with rect (*self.coords,*self.size) in window
        pass

    def get_rect(self):
        return pygame.Rect(*self.coords,*self.size)

    def jump(self):
        self.jump_counter = self.max_jump_counter

    def update_jump(self):
        #Check position based on jump counter, with parabolic ecuation
        if(self.jump_counter):
            neg = 1
            if(self.jump_counter>self.max_jump_counter//2):
                neg = -1
            delta = np.array([neg*self.jump_speed**2//3 ,0])
            self.coords += delta
            self.jump_counter -= 1

    def update_collision(self,obstacle_list):
        #List of active or collidable, Obstacle  instances, if hit an obstacle self.alive = False
        self_rect = self.get_rect()
        for obstacle in obstacle_list:
            if self_rect.colliderect(obstacle.get_rect()):
                self.alive = False

    def update_sprite(self):
        #self.sprite_animation_conunter betwen 0 and self.sprite_number
        self.sprite_animation_conunter = (self.sprite_animation_conunter + 1)%self.sprite_number

    def is_alive(self):
        return self.alive
