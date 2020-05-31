import numpy as np
from random import uniform
#Local imports
from class_Game.class_Game import Game
from genetic_model import generate_population, over_population
@Game()
def training(*args):
    model = args[0]
    x = np.atleast_2d(np.array(args[1]))
    prediction =  model.predict(x)
    if prediction >= 0.5:
        return 1
    return 0

if(__name__=='__main__'):
    render = False
    min_score = 30
    generations = 1
    gens_to_mutate = 1
    population_size = 2
    gens_to_crossover = 1
    mutate_probability = 0.01
    individuals_to_crossover = population_size * 0.5
    population = generate_population(100,3)
    for _ in range(generations):
        if _%10 == 0:
            render = True
        for p in population:
            p[0] = training(p[1],True)
            render = False
        population = sorted(population,key = lambda x:x[0],reverse=True)
        if(population[0][0] > min_score):
            break
        population = over_population(population,individuals_to_crossover,gens_to_crossover,gens_to_mutate,mutate_probability)
    population[0][1].save('model.h5')
