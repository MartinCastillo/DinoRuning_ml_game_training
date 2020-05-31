#Clase referente al 'juego' en si , su desarrollo, hace uso de la clase 'Pantalla'
import cv2
import numpy as np
from random import randint
import csv ; import os
from class_Game.guardar_cargar_datos.guardar_cargar_datos import guardar_datos_csv,cargar_datos_csv
from class_Game.class_Pantalla.class_Pantalla import Pantalla

juego_automatico = 1
_height = 500;
_width = 800;
#Para el caso de mover el proyecto, obtenemos la ubicación, pues usa archivos externos
csv_file_url = os.getcwd().replace('\\','/') + '/class_Game/game_data.csv'
class Game:
    def __init__(self,*args):
        self.args = args
    def normalizate_obstacle_info(self,obst):
        norm_height = (obst[0]-self.pantalla.obstacle_heigth/2)/(1.5*self.pantalla.obstacle_heigth)
        norm_pos=obst[1]/self.pantalla.width
        norm_character_pos = (self.pantalla.piso_height-self.pantalla.character_position[0])/self.pantalla.height
        obstaculo = [norm_height,norm_pos,norm_character_pos]
        return obstaculo

    def __call__(self,func):
        def wrapper(*args,**kargs):
            """This function include the running game, its a decorator bc its easier to
            include the external training code in"""
            """Lista que contiene informaciónn del juego ,para luego guardarla"""
            data = []
            #Inicializa un objeto pantalla, que esta vinculado con este juego especìfico
            self.pantalla = Pantalla(_height,_width)
            while(True):
                visualizar = args[1]
                saltado = False
                csv_data = cargar_datos_csv(csv_file_url)
                self.pantalla.record = int(csv_data['Records'][0])
                if(self.pantalla.contador_frames%self.pantalla.frames_entre_obstaculos == 0)and(randint(0,100)>20):
                    self.pantalla.add_obstacle()
                if(visualizar):
                    render = self.pantalla.render_screen()
                    cv2.imshow('Salta con espacio',render)
                    k = cv2.waitKey(1)
                    if( (k ==ord('q')) or (k == 27) ):
                        cv2.destroyAllWindows()
                        break
                    #salto
                    if(k == ord(' ')):
                        #Si no está saltando
                        if(not(self.pantalla.get_salto())):
                            saltado = True
                            #El número de esta variable depara el número de frames que toma este salto
                            self.pantalla.set_salto(self.pantalla.max_salto)
                            """Recopilar informacion juego"""
                            #######Guarda si salta
                            if(len(self.pantalla.lista_obstaculos)>0):
                                for o in self.pantalla.lista_obstaculos:
                                    if(o[1]>self.pantalla.character_position[1]):
                                        norm_obst = self.normalizate_obstacle_info(o)
                                        norm_obst.append(True)
                                        data.append(norm_obst)
                ###Evalua predicción, si hay obstaculos en lista
                if(len(self.pantalla.lista_obstaculos)>0):
                    """Predicción, función del parametro 'fun' es usada como evaludaro de si salta o no"""
                    #Normalizar obstaculo
                    for obst in self.pantalla.lista_obstaculos:
                        #Busca el primer obstaculo que no haya pasado
                        if(obst[1]>self.pantalla.character_position[1]):
                            obstaculo = self.normalizate_obstacle_info(obst)
                            prediccion = func(args[0],obstaculo)
                            if(not(self.pantalla.get_salto()) and (prediccion==True)and(juego_automatico)):
                                saltado = True
                                #El número de esta variable depara el número de frames que toma este salto
                                self.pantalla.set_salto(self.pantalla.max_salto)
                            break;
                self.pantalla.evaluar_saltar()
                ####Sobre el suelo
                #Cambia la posición o el estado de las líneas
                ret = self.pantalla.set_lines()
                muerto = self.pantalla.evaluar_muerte()
                if(muerto):
                    if(self.pantalla.puntaje>self.pantalla.record):
                        guardar_datos_csv(csv_file_url,[['Records'],[self.pantalla.puntaje]],mode='w')
                        print("Nuevo record: ".format(self.pantalla.puntaje))
                    break
                if(self.pantalla.update_obstacles()):
                    self.pantalla.puntaje += 1

                """Recopilar informacion juego"""
                ##DATA
                #Guarda data del frame, su distancia altura, altura personaje y si saltó
                if(len(self.pantalla.lista_obstaculos)>0)and(self.pantalla.contador_frames%30==0):
                    for obst in self.pantalla.lista_obstaculos:
                        #Busca el primer obstaculo que no haya pasado
                        if(obst[1]>self.pantalla.character_position[1]):
                            norm_obst = self.normalizate_obstacle_info(obst)
                            norm_obst.append(saltado)
                            data.append(norm_obst)
            cv2.destroyAllWindows()
            return self.pantalla.puntaje
        return wrapper
