#Es un módulo hecho solo para cargar y guardar datos en la clase 'Game', del módulo
#'class_Game', es para guardar información de juego, posiblemente útil y el record
#del juego más alto

import csv
def cargar_datos_csv(file_url):
    #Para guardar información de juegos anteriores
    with open(file_url) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        pil = {}
        for row in csv_reader:
            if line_count == 0:
                for r in row:
                    pil[r] = []
                line_count += 1
            else:
                for (ix,element) in enumerate(row):
                    pil[list(pil)[ix]].append(element)
                line_count += 1
    return pil
def guardar_datos_csv(file_url,datos,mode):
    if(len(datos)>0):
        #Guarda los datos en csv, toma una lista para las lineas, donde los elementos
        #son las palabras
        with open(file_url, mode=mode) as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in datos:
                writer.writerow(row)
        return True
    return False
