#Game, usada para puntuar modelos de nn y genetic_model con el modelo genetico en si
from Game.Game import Game
from genetic_model import generate_population, over_population

if(__name__=='__main__'):
    game = Game()
    min_score = 30
    generations = 100
    gens_to_mutate = 2
    population_size = 10
    gens_to_swap = 3
    mutate_probability = 0.01
    individuals_to_crossover = 2
    population = generate_population(population_size,3)
    render = False
    for _ in range(generations):
        if _%10 == 0:
            render = True
        #given a list of models return list with pairs [(model,score),...]
        population = game.play([x[0] for x in population])
        population = sorted(population,key = lambda x:x[1],reverse=True)
        if(population[0][1] > min_score):
            break
        population = over_population(population,individuals_to_crossover,gens_to_swap,gens_to_mutate,mutate_probability)
    population[0][1].save('model.h5')
