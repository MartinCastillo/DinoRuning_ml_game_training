import numpy as np
import pygame

class Agent:
    def __init__(self,coords,shape):
        self.coords = np.array(coords)
        self.shape = shape
        self.alive = True
        self.jump_counter = 0
        self.max_jump_counter = 12
        self.jump_height = 5
        self.sprites = [
            pygame.image.load("Game/assets/0.png"),
            pygame.image.load("Game/assets/1.png"),
            pygame.image.load("Game/assets/2.png")
            ]
        for sx,sprite in enumerate(self.sprites):
            self.sprites[sx] = pygame.transform.scale(sprite,self.shape)
            self.sprites[sx].set_colorkey((255,255,255))
        self.sprite_animation_conunter = 0
        self.sprite_number = 3
        self.sprite_speed = 2

    def render(self,window):
        sprite = self.sprites[self.sprite_animation_conunter].convert_alpha()
        window.blit(sprite,self.get_rect())

    def get_rect(self):
        return pygame.Rect(*self.coords,*self.shape)

    def jump(self):
        if(self.jump_counter==0):
            self.jump_counter = self.max_jump_counter

    def update_jump(self):
        #Check position based on jump counter, with parabolic ecuation
        if(self.jump_counter):
            neg = 1
            if(self.jump_counter>self.max_jump_counter//2):
                neg = -1
            delta = np.array([0,neg*self.jump_height**2])
            self.coords += delta
            self.jump_counter -= 1

    def update_collision(self,obstacle_list):
        #Given a list of  collidable, Obstacle  instances, if hit an obstacle self.alive = False
        if(len(obstacle_list)>0):
            self_rect = self.get_rect()
            for obstacle in obstacle_list:
                if self_rect.colliderect(obstacle.get_rect()):
                    self.alive = False

    def update_sprite(self,sprite_counter):
        if (sprite_counter%self.sprite_speed)==0:
            self.sprite_animation_conunter = (self.sprite_animation_conunter + 1)%self.sprite_number

    def update_agent(self,obstacle_list,sprite_counter):
        #Update collision a sprite and jump
        self.update_collision(obstacle_list)
        self.update_sprite(sprite_counter)
        self.update_jump()

    def is_alive(self):
        return self.alive
