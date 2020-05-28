#Clase referente a la estructura y visualizacion del juego, es el marco del
#que la clase Game depende

import cv2
import numpy as np
from random import randint
import os

class Pantalla:
    #Todo lo necesario para ejecutar el juego en pantalla
    def __init__(self,height,width):
        ##REFERENTE A PANTALLA
        self.height = height;
        self.width = width
        self.piso_height = width//3
        self.puntaje = 0
        self.contador_size = 70
        self.contador_frames = 0
        self.record = None

        ##REFERENTE AL SALTO
        self.salto = 0
        #Número de frames que toma un salto
        self.max_salto = 70
        self.velocidad_salto = 3

        ##SOBRE LAS LÍNEAS DEL SUELO
        #Recorran la base segun una progresión(cuando llega a 6 vuelve a 1)
        self.progresion_suelo = 1
        self.numero_lineas = 6
        self.lines =[]
        self.line_width = self.width//self.numero_lineas
        self.ubicacion_linea = self.width - self.line_width
        #Para que cambie la línea cada x cantidad de frames
        self.contador_x_frames  = 0
        #delay entre lineas del suelo (Cuanto menor es, mayor es la velocidad)
        self.cada_x_frames = 40

        ##REFERENTE A PERSONAJE
        self.character_position = [self.height-self.piso_height,self.width//3]
        self.character_shape = [50,50]
        ##SPRITES
        self.character_sprite_url = os.getcwd().replace('\\','/') + '/class_Game/class_Pantalla/main_sprites/'
        #Conteo de sprite
        self.sprite_number = 0
        self.character_image_url = self.character_sprite_url+str(self.sprite_number)+'.png'
        self.sprite_animation_length = 2
        #Velocidad de animacion de correr
        self.frames_por_sprite = self.cada_x_frames

        #Lista de los obstaculos con formato [ubicación(En altura),(distancia del o en x)]
        self.lista_obstaculos = []
        #El movimiento de cada paso por frame de los obstaculos a la derecha
        self.decremento_a_izquierda = self.line_width//self.cada_x_frames
        self.obstacle_width = 20
        self.obstacle_heigth = 30
        self.frames_entre_obstaculos = 100

    def update_sprite(self):
        #Cambia el sprite al siguiente, si llega al 5 vuelve al 0
        if(self.sprite_number!=self.sprite_animation_length):
            self.sprite_number+=1
        else:
            self.sprite_number=1
        self.character_image_url = self.character_sprite_url+str(self.sprite_number)+'.png'
        return True

    def set_piso(self,_piso_height):
        self.piso_height = _piso_height
    def set_character_position(self,y,x):
        self.character_position = [y,x]
    def set_salto(self,new_salto):
        self.salto = new_salto
    def get_salto(self):
        return self.salto

    def set_lines(self):
        #La idea de esta función es que devuelva unal lista con las posiciones de las
        #líneas listas para renderizar (su posición varía en el eje x)
        if(self.contador_x_frames%self.cada_x_frames == 0):
            self.ubicacion_linea = self.width - self.progresion_suelo*self.line_width
            if(self.progresion_suelo != self.numero_lineas):
                self.progresion_suelo +=1
            else:
                self.progresion_suelo = 1
        self.contador_x_frames +=1
        return True

    def evaluar_saltar(self):
        #Realiza los cambios a la posición del personaje de manera de que 'salte'
        #Necesita una variable global que indica la información del salto (el
        #momento de este),si es 0, es por que no salta, por lo que esta función
        #debe estar constantemente monitoreando
        if(self.salto):
            neg = 1
            if(self.salto>self.max_salto//2):
                neg = -1
            self.set_character_position(self.character_position[0]+neg*self.velocidad_salto**2//3,self.character_position[1])
            self.salto -= 1


    ##OBSTACULOS
    def add_obstacle(self):
        self.lista_obstaculos.append([randint(self.obstacle_heigth//2,self.obstacle_heigth*2),self.width])
    def update_obstacles(self):
        #Adapta  la 'lista_obstaculos', con su formato adecuado, para luego renderizalos,
        #mueve todos los objetos a la izquierda o le resta un mismo valor a todos los segundos
        #valores de los obstaculos de la lista 'lista_obstaculos', también evalua si sobrepasa
        #algún obstaculo
        pil = []; sobrepasa_obstaculo = False
        for o in self.lista_obstaculos:
            if(o[1]-self.decremento_a_izquierda>0):
                pil.append([o[0],o[1]-self.decremento_a_izquierda])
            if(o[1]//self.decremento_a_izquierda == self.character_position[1]//self.decremento_a_izquierda):
                sobrepasa_obstaculo=True
        self.lista_obstaculos = pil
        if(sobrepasa_obstaculo):
            return True
        return False
    def evaluar_muerte(self):
        #Evalua si colisiona con un obstaculo, si es así retorna True si no False
        for (obstacle_h,obstacle_pos) in self.lista_obstaculos:
            if(self.character_position[0] >= self.height - self.piso_height - obstacle_h):
                if(self.character_position[1]+self.character_shape[1]>= obstacle_pos)and\
                (self.character_position[1]+self.character_shape[1]< obstacle_pos+self.obstacle_width*2):
                        return True
        return False

    def render_screen(self):
        self.contador_frames +=1
        self.frames_por_sprite = self.cada_x_frames
        self.decremento_a_izquierda = self.line_width//self.cada_x_frames
        render =  np.ones((self.height,self.width),np.uint8)*255
        #Renderiza suelo
        render[render.shape[0]-self.piso_height:render.shape[0],0:render.shape[1]] = 150
        ##CAMBIO DE SPRITE
        if(self.contador_frames%self.frames_por_sprite==0):
            self.update_sprite()
        #Renderiza personaje en su posición actual
        render[self.character_position[0]-self.character_shape[0]:self.character_position[0] ,
            self.character_position[1]:self.character_position[1]+self.character_shape[1]] =   \
            cv2.resize(cv2.imread(self.character_image_url,0), (self.character_shape[1],self.character_shape[0])
            )
        ##Render Líneas del suelo cambiantes
        render[render.shape[0]-self.piso_height:render.shape[0] , self.ubicacion_linea:self.ubicacion_linea+self.line_width] = 100
        #Renderizar obstaculos
        for obstacle in self.lista_obstaculos:
            render[render.shape[0]-self.piso_height-obstacle[0]:render.shape[0]-self.piso_height ,obstacle[1]:obstacle[1]+self.obstacle_width] = 60
        #Texto
        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(render,'Puntaje: {} // Record: {}'.format(self.puntaje,self.record),
            (0,self.contador_size), font, 2,(0,0,0),2,cv2.LINE_AA)
        return render

if(__name__=='__main__'):
    pass
