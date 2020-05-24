#Objetivo: Por médio de un algoritmo genético, buscar una secuencia de letras especificas,
#, la secuencia n , con 4 letras.
from random import randint,uniform
from clint.textui import colored
from pdb import set_trace
n = ['A','B','D','C'] ; letras_posibles = 'ABCDEF' ; numero_letra_dist = len(letras_posibles)
#Contamos la cantidad de letras de cada tipo pues lo requeriremos más adelante
cantidad_cada_letra_n = {x:0 for x in letras_posibles}
for _n in n:
    cantidad_cada_letra_n[_n] += 1
iteraciones = 1000
t_poblacion = 20
#Una porción mínima y máxima que debe quedar de la población luego de la selección,
#Es para evitar que se acaben las poblaciones
porcion_restante = 0.35
porcion_maxima = 1
probabilidad_mutación = 2 # Es un porcentaje
#Máximo valor que puede tomar el puntaje de un elemento
redondeador = 100
#porectaje de eficiencia mínimo, el algoritmo para si alcanza esta proximidad
min_prox = 85
soluciones_diferentes = 0

def info():
    global n
    print('''
    ----------------------------------------------------------------------
    INFORMACIÓN ALGORITMO GENÉTICO::
    -Iteraciones máximas: {}
    -Tamaño inicial de la población: {}
    -Rango de aceptabilidad: {}%
    -Probabilidad de mutación: {}%
    -Porción mínima de supervivencia : {}%
    -porción máxima de supervivencia :{}%
    -Posibles combinaciones: {}
    ----------------------------------------------------------------------
    '''.format(iteraciones,t_poblacion,min_prox,probabilidad_mutación,porcion_restante*100,
    porcion_maxima*100,numero_letra_dist**len(n)
    ))

#Tiene las listas de cuatro números y su puntaje
def generar_poblacion(_t_poblacion,_n):
    global soluciones_diferentes,n,letras_posibles
    #poblacion a retornar
    ret = []
    for _ in range(_t_poblacion):
        #Generar elemento
        e = [letras_posibles[randint(0,numero_letra_dist-1)] for l in _n]
        #Agrega un quinto elemento (indice 4) para el score
        e.append(0)
        ret.append(e)
        soluciones_diferentes +=1
    return(ret)

def puntuar_y_retornar(elemento,_n):
    global letras_posibles
    #Debemos considerar dos cosas, numero de letras correctas en lugar correcto y el número,
    #de letras de ada tipo correcto, ej: si hay 2 letras a correctas, pero en lugar mal, suma un poco
    e = elemento[0:len(elemento)-1]
    puntaje = 0 ; cantidad_cada_letra = {x:0 for x in letras_posibles}
    #Comparamos coincidencias
    for (ix,_e) in enumerate(e):
        cantidad_cada_letra[_e] += 1
        if(_e == _n[ix]):
            puntaje += 100
    #Comparamos cantidad de cada letra
    for k in cantidad_cada_letra:
        if cantidad_cada_letra[k] == cantidad_cada_letra_n[k]:
            puntaje += 25
    #Hay un puntaje máximo de 500, lo normalizamos a 1000 con una regla de 3cl
    e.append((puntaje*redondeador) / (25*len(cantidad_cada_letra)+100*len(_n)))
    return e

def elimincaion(población,porcion):
    '''La lista 'población'debe estar ordenada de menores a mayores puntajes'''
    """INCLUIMOS LA MUTACIÓN EN LA ELIMINACIÓN"""
    #Elimina parte de la población, dejando una porción (de 0 a 1) y luego la retorna
    #la idea es que haya una posibilidad mayor para ser eliminado para menores puntajes,
    #y los mayores menos, sin solo cortar
    ret = []; #poblacion a retornar
    #Valor total de la población, suma de los puntajes
    total = 0
    total = sum( [e[len(e)-1] for e in poblacion] )
    #Nos aseguramos de que la población tenga un tamaño minimo
    while ((len(ret) < len(poblacion)*porcion) or (len(ret) > len(poblacion)*porcion_maxima)):
        #Para hacer la probabilidad, hacemos el precentil de cada valor
        for (ix,elemento) in enumerate(poblacion):
            """Mutación auxiliar-----------"""
            random_mutation_p = uniform(0,100)
            #print(random_mutation_p)
            if (random_mutation_p < probabilidad_mutación):
                elemento = mutacion(elemento)
                print(colored.cyan('Mutación! / '+str(random_mutation_p)))
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
    global soluciones_diferentes
    #Cruza los 'genes' de los padres, y crea un nuevo elemento, TAMBIÉN DEBE TENER SU PUNTAJE
    #POR CONVENCIÓN PODEMOS DEJAR QUE TOME LOS DOS PRIMEROS NÚMEROS DE UNO Y LOS DOS ÚLTIMOS DEL OTRO
    son = (p1[0:2] + p2[2:4])
    son.append(0)
    #print(son)
    son = puntuar_y_retornar(son,n)
    soluciones_diferentes +=1
    return son

def mutacion(elemento):
    global soluciones_diferentes,letras_posibles
    #Cambia un elemento aleatorio de la lista, por otro aleatorio, independiente de
    #la probabilidad de que la mutación surja,debe incluir puntaje
    #OJO que auntque deba ser en una posición aleatoria, no puede incluir el puntaje
    ix = randint(0,len(elemento)-2)
    elemento[ix] = letras_posibles[randint(0,numero_letra_dist-1)]
    elemento = puntuar_y_retornar(elemento,n)
    soluciones_diferentes += 1
    return(elemento)

def puntaje_promedio(_poblacion):
    #Hace un promedio de los puntajes en la poblacion
    return(sum( [e[len(e)-1] for e in _poblacion] )/len(_poblacion))

if(__name__=='__main__'):
    puntuacion_promedio = 0 ; solucion = [] ; ciclos = 0 ; iters = 0
    while (not(solucion)):
        ciclos += 1 ;
        "Genera población"
        poblacion = generar_poblacion(t_poblacion,n)
        "Puntua población"
        for (eix,e) in enumerate(poblacion):
            poblacion[eix] = puntuar_y_retornar(e,n)
            #Ordena lista segun puntuación, acendentemente
            poblacion.sort(key = lambda e:e[len(e)-1])
        for _ in range(iteraciones):
            if(puntuacion_promedio>redondeador*(min_prox/100)):
                solucion = poblacion[len(poblacion)-1]
                break
            if(len(poblacion)==1):
                print(colored.red('Reinicio, solo queda un elemento superviviente'))
                break
            #print('Población inicial: {}'.format(len(poblacion)))
            """Elimincaion sobre población"""
            poblacion = elimincaion(poblacion,porcion_restante)
            #print(len(poblacion))
            #print('Población luego de la selección'.format(len(poblacion)))
            """Cruce de población"""
            #Hace un cruce cada dos elementos
            #Usamos este valor para elegir los padres con probabilidad
            total = sum( [e[len(e)-1] for e in poblacion] )

            #Los reproducimos la cantidad de veces que requiere para alcanzar la población inicial
            d = t_poblacion-len(poblacion) ; desviacion = 0
            if(d>0):
                desviacion = d
            else:
                desviacion = len(poblacion)//2
            for _r in range(desviacion):
                #####elige dos elementos, basandonos en el mismo sistena que en la eliminación
                padres = []
                for r in range(2):
                    for (ix,posible_padre) in enumerate(poblacion):
                        percentil = sum([l[len(l)-1] for l in poblacion[0:ix+1]])
                        numero = uniform(0,total)
                        #Evaluamos
                        if(percentil>numero):
                            padres.append(posible_padre)
                            break
                #####Los padres fueron elegidos
                #HAcemos los cruces y los agregamos a la poblacion
                poblacion.append(cruce(padres[0],padres[1]))
            #print(len(poblacion))
            puntuacion_promedio = puntaje_promedio(poblacion)
            print(colored.white('Promedio , tamaño e iteración : {}% / {} elementos / {}'.format(int(puntuacion_promedio),len(poblacion),_)))
        iters += _
    info()
    print(colored.green('Posible solución encontrada, en {} iteraciones y {} ciclos: {}'.format(_,ciclos,solucion[0:len(solucion)-1])))
    print(colored.green('Movimientos totales: {}'.format(iters)))
    print(colored.green('Soluciones generadas en total: {}'.format(soluciones_diferentes)))
    print(colored.green('solucion real: {}'.format(n)))
    pass
