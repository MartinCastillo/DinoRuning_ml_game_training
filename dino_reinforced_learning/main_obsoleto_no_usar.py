#Este archivo incluye lo referente a ´juntarlo todo',realizar el aprendizaje en si
"""Todo este desastre se resume en un modelo evolutivo, en alguna parte hay una función training(p,visible)
esta toma cierta matriz y un boleano que determina si se muestra en pantalla o no el juego, la matriz determina
si va o no a saltar con cierta matriz de obstaculo, la funciòn retorna el puntaje que obtinie la matriz luego de
un juego sorry si hay demasiados comentarois, pero son para mi, que quizà olvide como funciona esto."""
#Imports
import numpy as np
from random import randint,uniform
#Local imports
from class_Game.class_Game import Game
visible = True
"""FORMATO DE ELEMENTO DE POBLACIÒN, UNA MATRIZ CON
CARACTERÌSTICAS ESPECÌFICAS"""
t_poblacion = 20
probabilidad_mutacion = 10#Percent
min_puntaje = 100#Puntaje mínimo
porcion_restante = 0.4

min_max = [0,1]
nn_deep = 0
freatures = 3
desviacion_min = 0.05

#Tiene las matrixs de pesos de (nxf) y su puntaje
def generar_poblacion(_t_poblacion,n):
    """-----------------------"""
    #poblacion a retornar
    ret = []
    for _ in range(_t_poblacion):
        #Generar elemento
        e = [np.matrix(np.random.uniform(min_max[0],min_max[1],(n,freatures+1)))]
        #Agrega un segundo elemento (indice 1) para el score
        e.append(0)
        ret.append(e)
    return(ret)

def elimincaion(población,porcion):
    '''La lista 'población'debe estar ordenada de menores a mayores puntajes'''
    #Elimina parte de la población, dejando una porción (de 0 a 1) y luego la retorna
    #la idea es que haya una posibilidad mayor para ser eliminado para menores puntajes,
    #y los mayores menos, sin solo cortar
    ret = []; #poblacion a retornar
    #Valor total de la población, suma de los puntajes
    total = 0
    total = sum( [e[len(e)-1] for e in poblacion] )
    #Nos aseguramos de que la población tenga un tamaño minimo
    while ((len(ret) < len(poblacion)*porcion)):
        #Para hacer la probabilidad, hacemos el precentil de cada valor
        for (ix,elemento) in enumerate(poblacion):
            #Suma de los valores menores al actual
            percentil = sum([ l[len(l)-1] for l in poblacion[0:ix+1]] )
            #para ver si el elemento queda hacemos un numero aleatorio de o al total
            #(menos un factor de ajuste), si el número es mayor al percenti, no queda
            numero = uniform(0,total)
            #Evaluamos
            if(percentil>numero):
                #Queda
                ret.append(elemento)
    return(ret)

def cruce(p1,p2):
    """-----------------------"""
    #Cruza los 'genes' de los padres, y crea un nuevo elemento, TAMBIÉN DEBE TENER SU PUNTAJE
    #Puede Promediar los elementos homologos de cada uno
    #Elige la dominancia de uno alazar
    dom = uniform(0,1)
    dom = 0.5
    ret = [(p1[0]*dom + p2[0]*(1-dom)),0]
    return ret

def mutacion(elemento):
    #Cambia una capa o columna aleatoria de la matriz, por otra aleatorio,independiente
    #de la probabilidad de que la mutación surja,debe incluir puntaje
    #OJO que auntque deba ser en una posición aleatoria, no puede incluir el puntaje
    e = elemento[0]
    #FILA O COLUMNA
    f_o_c = randint(0,1)
    if(f_o_c):
        e[randint(0,e.shape[0])-1,:] = np.matrix(np.random.uniform(min_max[0],min_max[1],(1,freatures+1)))
        print('MUTA COLUMNA')
    else:
        e[:,randint(0,e.shape[1]-1)] = np.matrix(np.random.uniform(min_max[0],min_max[1],(e.shape[0],1)))
        print('MUTA FILA')
    return([e,0])

def get_puntaje_promedio(_poblacion):
    #Hace un promedio de los puntajes en la poblacion
    return(sum( [e[len(e)-1] for e in _poblacion] )//len(_poblacion))

#Game toma parametros cuando se crea que pueden que pueden ser usados por training,
#como primeros parametros, si no, se deja vacio
@Game()
def training(*args):
    #import pdb; pdb.set_trace()
    #Hacemos la prediccion
    w = args[0][0]#Los pesos correspondientes al modelo actual
    #Considera que args[1] contiene tres parametros, la altura, ancho y distancia del obstaculo más cercano
    x = np.matrix(args[1]).T
    #Predice una salida boleana, si el valor cumple la condición de ser mayor que 0,
    #salta si no no, ESTO ES VARIABLE Y EXPERIMENTAL, liego retorna el valor al juego
    prediccion = (w[:,0:freatures]@x)
    #El umbral es 0
    if prediccion >= 0.5:
        return 1
    return 0

if(__name__=='__main__'):
    iter = 1 ; puntuacion_promedio = 0 ; last_prom_punt = 0
    """Genera Población"""
    poblacion = generar_poblacion(t_poblacion,nn_deep+1)
    """Empieza entrenamiento"""
    while(puntuacion_promedio < min_puntaje):
        for (ix,p) in enumerate(poblacion):
            """Puntuar"""
            #Tenemos una funcion que hace el juego y que incorpora adentro una de entrenamiento
            #Podemos usar Un bucle aquí para las iteraciones del entrenamiento, para la evaluación
            #ocupamos training que primero pasa por Game, y para orgainzar usamos training para
            #la evaluación dentro del juego
            poblacion[ix][1] = training(p,visible)
        #Luego de que puntua ordena según puntaje
        poblacion.sort(key = lambda e: e[len(e)-1])
        #Saca puntaje promedio, para ver el avance de la población
        puntuacion_promedio = get_puntaje_promedio(poblacion)
        if(((puntuacion_promedio - last_prom_punt)*100)/min_puntaje < desviacion_min):
            print('Estancado')
            t_poblacion += 10
            probabilidad_mutacion += 3
        last_prom_punt = puntuacion_promedio
        """elimincaion"""
        poblacion = elimincaion(poblacion,porcion_restante)
        """Cruce"""
        #Hace un cruce cada dos elementos
        #Usamos este valor para elegir los padres con probabilidad
        total = 0
        total = sum( [e[len(e)-1] for e in poblacion] )
        #Los reproducimos la cantidad de veces que requiere para alcanzar la población inicial
        #Si sobra lo hace a un mínimo(la mitad)
        d = t_poblacion-len(poblacion) ; desviacion = 0
        if(d>0):
            desviacion = d
        else:
            desviacion = len(poblacion)//2
        #Por cada hijo que se formarán
        for n_hijo in range(desviacion):
            #####elige dos elementos, bas-andonos en el mismo sistena que en la eliminación
            padres = []
            for r in range(2):
                for (ix,posible_padre) in enumerate(poblacion):
                    percentil = sum([l[len(l)-1] for l in poblacion[0:ix+1]])
                    r_numero = uniform(0,total)
                    #Evaluamos
                    if(percentil>r_numero):
                        padres.append(posible_padre)
                        break
            #####Los padres fueron elegidos
            #HAcemos los cruces y los agregamos a la poblacion
            """Mutaciones serán sobre el hijo"""
            p_mutacion = randint(0,100)
            if(p_mutacion>probabilidad_mutacion):
                #No Muta
                poblacion.append(cruce(padres[0],padres[1]))
            else:
                poblacion.append(mutacion(cruce(padres[0],padres[1])))

        print('Promedio, miembros e iteración, {} / {} / {}'.format(puntuacion_promedio,len(poblacion),iter))
    #Si consigue la solución
    solucion = poblacion[0]
    training(solucion,False)
    print('Solución!!'+str(solucion))
    pass
