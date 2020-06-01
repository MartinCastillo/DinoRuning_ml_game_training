#Clase referente al 'juego' en si , su desarrollo, hace uso de la clase 'Pantalla'
import pygame
import numpy as np
from random import uniform,randint
from Game.Agent.Agent import Agent
from Game.Obstacle.Obstacle import Obstacle

class Game:
    def __init__(self,**kargs):
        self.set_all(**kargs)

    def set_all(self,**kargs):
        self.width = kargs.get("width",700)
        self.heigth = kargs.get("heigth",700)
        self.speed = kargs.get("speed",10)
        self.agent_size = kargs.get("agent_size",10)
        self.obstacle_spaw_probability = kargs.get("obstacle_spaw_probability",0.1)

        self.obstacle_width_max = kargs.get("obstacle_width_max",30)
        self.obstacle_heigth_max = kargs.get("obstacle_heigth_max",70)
        self.obstacle_width_variation = kargs.get("obstacle_width_variation",70)
        self.obstacle_heigth_variation = kargs.get("obstacle_heigth_variation",70)

        #Position from the left where the character stands in the x axis
        self.character_x_position = kargs.get("speed",self.width//3)
        self.ground_y_position = kargs.get("ground_y_position",self.heigth//2)
        self._global_score = 0#Este score se suma y los agentes vivos actualizan su score segun este
        self.last_len_obstacles = 0#Usado para ver si se pasaron obstaculos, si hay menos obstaculos que antes los pasó

    def update_obstacles(self,obstacle_list):
        #Mueve todos los obstaculos cierta cantidad a la izquierda, agrega obstaculos y actualiza score
        active_obstacles = []
        if(len(obstacle_list)>0):
            for o in obstacle_list:
                #Mueve obstaculo a la izquierda
                coords = o.get_coords()-[self.speed,0]
                o.set_coords(coords)
                if coords[0] < -self.agent_size:
                    obstacle_list.remove(o)
                elif coords[0] > self.character_x_position:
                    active_obstacles.append(o)
            #Actualizar score
            if(self.last_len_obstacles!=len(active_obstacles)):
                self.last_len_obstacles = len(active_obstacles)
                self._global_score+=1
        #añade obstaculos con pribabilidad aleatoria
        if(uniform(0,1)<=self.obstacle_spaw_probability):
            obstacle_width = randint(self.obstacle_width_max-self.obstacle_width_variation,self.obstacle_width_max)
            obstacle_heigth = randint(self.obstacle_heigth_max-self.obstacle_heigth_variation,self.obstacle_heigth_max)
            obstacle = Obstacle((self.width,self.ground_y_position-obstacle_width),(obstacle_width,obstacle_heigth))
            obstacle_list.append(obstacle)
            active_obstacles.append(obstacle)
        return obstacle_list , active_obstacles

    def normalize_obtacle(self,obstacle):
        """#given an obstacle object return 1x3 vector with the position from the character
        #in x axis, width and heigth all from 0 to 1"""
        normalized = obstacle
        return normalized

    def render_game(self,window,agents,obstacles):
        """#Render background and floor

        #Render agents

        #Render obstacles"""
        pass

    def play(self,models,render = False):
        self._global_score = 0
        obstacles = [] #Si el obstaculo no se sale de la pantalla
        agents_models_score = []
        active_obstacles = [] #If in x axis is greater od self.character_x_position
        for m in models:
            agents_models_score.append([Agent(),m,0])
        if(render):
            window = pygame.display.set_mode((width,heigth))
            pygame.display.get_caption(" ")
            pass
        while(True):
            obstacles,active_obstacles = self.update_obstacles(obstacles)
            for ax,agent_model in enumerate(agents_models_score):
                agent = agent_model[0]
                model = agent_model[1]
                if len(active_obstacles)>0:
                    """###Evalua predicción, si hay obstaculos en lista
                    norm_obstacle = self.normalize_obtacle(obstacles[0])
                    prediction = model.predict(norm_obstacle)
                    if prediction >= 0.5:
                        agent.jump()"""
                    agent.update_collision(active_obstacles)
                    #Si está vivo actualiza score al global
                    if(agent.is_alive):
                        agents_models_score[ax][2] = self._global_score
                agent.update_jump()
            if(render):
                #Solo renderiza agentes vivos
                active_agents = []
                for a in agents_models_score:
                    agent = a[0]
                    if(agent.is_alive()):
                        active_agents.append(agent)
                self.render_game(window,agents,obstacles)
        return [models_score[1:] for models_score in agents_models_score]
