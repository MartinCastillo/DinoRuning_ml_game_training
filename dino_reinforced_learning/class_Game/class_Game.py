#Clase referente al 'juego' en si , su desarrollo, hace uso de la clase 'Pantalla'
import cv2
import numpy as np
from time import sleep
from random import randint
import csv ; import os
from class_Game.guardar_cargar_datos.guardar_cargar_datos import guardar_datos_csv,cargar_datos_csv
from class_Game.class_Pantalla.class_Pantalla import Pantalla

reescribir_data_entrenamiento = 0
juego_automatico = 1
visualizar = 0
_height = 500;
_width = 800;
#Para el caso de mover el proyecto, obtenemos la ubicación, pues usa archivos externos
csv_file_url = os.getcwd().replace('\\','/') + '/class_Game/data/game_data.txt'
csv_train_file_url = os.getcwd().replace('\\','/') + '/class_Game/data/train_data.txt'
csv_data = []
class Game:
    def __init__(self,*args):
        self.args = args

    def __call__(self,func):
        def wrapper(*args,**kargs):
            """This function include the running game, its a decorator bc its easier to
            include the external training code in"""
            """Lista que contiene informaciónn del juego ,para luego guardarla"""
            data = []
            #Inicializa un objeto pantalla
            pantalla1 = Pantalla(_height,_width)
            while(True):
                visualizar = args[1]
                saltado = False
                csv_data = cargar_datos_csv(csv_file_url)
                pantalla1.record = int(csv_data['Records'][0])
                if(pantalla1.contador_frames%pantalla1.frames_entre_obstaculos == 0)and(randint(0,100)>20):
                    pantalla1.add_obstacle()

                if(visualizar):
                    render = pantalla1.render_screen()
                    cv2.imshow('Salta con espacio',render)

                    k = cv2.waitKey(1)
                    if( (k ==ord('q')) or (k == 27) ):
                        cv2.destroyAllWindows()
                        break
                    #salto
                    if(k == ord(' ')):
                        #print('Salto')
                        #Si no está saltando
                        if(not(pantalla1.get_salto())):
                            saltado = True
                            #El número de esta variable depara el número de frames que toma este salto
                            pantalla1.set_salto(pantalla1.max_salto)
                            """Recopilar informacion juego"""
                            #######Guarda si salta
                            if(len(pantalla1.lista_obstaculos)>0):
                                data.append([pantalla1.lista_obstaculos[0][0],pantalla1.lista_obstaculos[0][1],pantalla1.character_position[0],saltado])

                ###Evalua predicción, si hay obstaculos en lista
                if(len(pantalla1.lista_obstaculos)>0):
                    """Predicción"""
                    """Función del parametro 'fun' es usada como evaludaro de si salta o no"""
                    #Normalizar obstaculo
                    for obst in pantalla1.lista_obstaculos:
                        #Busca el primer obstaculo que no haya pasado
                        if(obst[1]>pantalla1.character_position[1]):
                            #Noramliza obstaculo
                            norm_height = (obst[0]-pantalla1.obstacle_heigth/2)/(1.5*pantalla1.obstacle_heigth)
                            norm_pos=obst[1]/pantalla1.width
                            norm_character_pos = (pantalla1.piso_height-pantalla1.character_position[0])/pantalla1.height
                            obstaculo = [norm_height,norm_pos,norm_character_pos]
                            prediccion = func(args[0],obstaculo)
                            if(not(pantalla1.get_salto()) and (prediccion==True)and(juego_automatico)):
                                saltado = True
                                #El número de esta variable depara el número de frames que toma este salto
                                pantalla1.set_salto(pantalla1.max_salto)
                            break;
                pantalla1.evaluar_saltar()
                ####Sobre el suelo
                #Cambia la posición o el estado de las líneas
                ret = pantalla1.set_lines()

                muerto = pantalla1.evaluar_muerte()
                if(muerto):
                    if(pantalla1.puntaje>pantalla1.record):
                        guardar_datos_csv(csv_file_url,[['Records'],[pantalla1.puntaje]])
                        print("Nuevo record: ".format(pantalla1.puntaje))
                    break

                if(pantalla1.update_obstacles()):
                    pantalla1.puntaje += 1

                """Recopilar informacion juego"""
                ##DATA
                #Guarda data del frame, su distancia altura, altura personaje y si saltó
                if(len(pantalla1.lista_obstaculos)>0)and(pantalla1.contador_frames%30==0):
                    data.append([pantalla1.lista_obstaculos[0][0],pantalla1.lista_obstaculos[0][1],pantalla1.character_position[0],saltado])

            """Guarda informacion juego"""
            if(reescribir_data_entrenamiento):
                guardar = []
                guardar.append(['x_o','x_d','x_h','y'])
                for d in data:
                    guardar.append(d)
                guardar_datos_csv(csv_train_file_url,guardar)
            cv2.destroyAllWindows()
            return pantalla1.puntaje
        return wrapper
