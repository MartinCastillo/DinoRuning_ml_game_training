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
        self.window_size = kargs.get("window_size",(1000,700))
        self.obstacle_speed = kargs.get("speed",20)
        self.agent_shape = kargs.get("agent_shape",(70,70))
        #Each self.cycles_betwen_obstacle_spawn there is a random probability to spawn an obstacle
        self.cycles_betwen_obstacle_spawn = kargs.get("cycles_betwen_obstacle_spawn",25)
        self.obstacle_spaw_probability = kargs.get("obstacle_spaw_probability",0.5)
        self.obstacle_width_max = kargs.get("obstacle_width_max",20)
        self.obstacle_heigth_max = kargs.get("obstacle_heigth_max",70)
        self.obstacle_width_variation = kargs.get("obstacle_width_variation",10)
        self.obstacle_heigth_variation = kargs.get("obstacle_heigth_variation",10)

        self._background_x_position = self.window_size[0];
        self._background_sprite = pygame.image.load("Game/assets/background1.jpg")
        self._background_sprite_shape = self._background_sprite.get_size()

        #Position from the left where the character stands in the x axis
        self.character_x_position = self.window_size[0]//3
        self.ground_y_position = 558
        self._global_score = 0#Este score se suma y los agentes vivos actualizan su score segun este
        self._last_len_obstacles = 0#Usado para ver si se pasaron obstaculos, si hay menos obstaculos que antes los pasó
        self._run_counter = 1
        pygame.font.init()
        self._font = pygame.font.SysFont(None, 100)


    def update_obstacles(self,obstacle_list):
        #Mueve todos los obstaculos cierta cantidad a la izquierda, agrega obstaculos y actualiza score
        active_obstacles = []
        if(len(obstacle_list)>0):
            for o in obstacle_list:
                #Mueve obstaculo a la izquierda
                coords = o.get_coords()-[self.obstacle_speed,0]
                o.set_coords(coords)
                if coords[0] < -o.get_shape()[0]:
                    obstacle_list.remove(o)
                elif coords[0] > self.character_x_position:
                    active_obstacles.append(o)
            #Actualizar score
            if(self._last_len_obstacles>len(active_obstacles)):
                self._global_score+=1
            self._last_len_obstacles = len(active_obstacles)
        #añade obstaculos con pribabilidad aleatoria
        if (uniform(0,1)<=self.obstacle_spaw_probability)and(self._run_counter%self.cycles_betwen_obstacle_spawn==0):
            obstacle_width = randint(self.obstacle_width_max-self.obstacle_width_variation,self.obstacle_width_max)
            obstacle_heigth = randint(self.obstacle_heigth_max-self.obstacle_heigth_variation,self.obstacle_heigth_max)
            obstacle = Obstacle((self.window_size[0],self.ground_y_position-obstacle_heigth),(obstacle_width,obstacle_heigth))
            obstacle_list.append(obstacle)
            active_obstacles.append(obstacle)
        return obstacle_list , active_obstacles

    def update_background_position(self):
        self._background_x_position = self._background_x_position % self._background_sprite_shape[0]
        self._background_x_position -= self.obstacle_speed
    def render_background(self,window):
        window.blit(self._background_sprite,(self._background_x_position-self._background_sprite_shape[0],0))
        window.blit(self._background_sprite,(self._background_x_position,0))
        self.update_background_position()

    def render_game(self,window,agents,obstacles,text):
        window.fill((0,0,0))
        self.render_background(window)
        #Render agents
        for agent in agents:
            agent.render(window)
        #Render obstacles
        for obstacle in obstacles:
            obstacle.render(window)
        #Evalua si debe sacar el juego y setea framerate
        text = self._font.render(str(self._global_score),True,(0,78,56))
        window.blit(text,(0,0))

        pygame.time.Clock().tick(27)
        pygame.display.update()
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self._run_counter = 0

    def normalize_obtacle(self,obstacle):
        #given an obstacle object return 1x3 vector with the position from the character
        #in x axis, width and heigth all from 0 to 1
        obstacle = obstacle.get_rect()
        width = self.window_size[0]
        x_distance = obstacle[0] - self.character_x_position
        x_distance //= width
        shape = obstacle[-2:]
        shape = [shape[0]//width,shape[1]//width]
        return np.atleast_2d(np.array([x_distance,*shape]))

    def play(self,models,render = True,controllable = False):
        #given a list of keras models, return pair of (keras model, socre)
        self._global_score = 0
        obstacles = [] #Si el obstaculo no se sale de la pantalla
        agents_models_score = []
        active_obstacles = [] #If in x axis is greater od self.character_x_position
        if(render):
            window = pygame.display.set_mode(self.window_size)
            pygame.display.set_caption(" ")
            pygame.time.Clock()
            pygame.init()
        for m in models:
            agents_models_score.append([Agent((self.character_x_position,self.ground_y_position-self.agent_shape[1]),self.agent_shape),m,0])
        self._run_counter = 1
        while self._run_counter:
            self._run_counter += 1
            obstacles,active_obstacles = self.update_obstacles(obstacles)
            for ax,agent_model in enumerate(agents_models_score):
                agent = agent_model[0]
                model = agent_model[1]
                agent.update_agent(active_obstacles,self._run_counter)
                #Controllable
                if(render)and(controllable):
                    if(pygame.key.get_pressed()[pygame.K_UP]):
                        agent.jump()
                if (len(active_obstacles)>0) and (agent.is_alive):
                    #Evalua predicción
                    norm_obstacle = self.normalize_obtacle(active_obstacles[0])
                    prediction = model.predict(norm_obstacle)
                    if prediction >= 0.5:
                        agent.jump()
                    #Si está vivo actualiza score al global
                    agents_models_score[ax][2] = self._global_score
            if(render):
                #Selecciona solo agentes vivos para renderizar
                active_agents = []
                for a in agents_models_score:
                    agent = a[0]
                    if(agent.is_alive()):
                        active_agents.append(agent)
                self.render_game(window,active_agents,obstacles,self._global_score)
        return [models_score[1:] for models_score in agents_models_score]
