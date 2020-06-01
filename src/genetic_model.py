import numpy as np
from random import randint,uniform
from keras.models import Sequential
from keras.layers import Dense,Activation

def create_model(n_inputs):
    model = Sequential()
    model.add(Dense(n_inputs,input_shape = (n_inputs,)))
    model.add(Activation('relu'))
    model.add(Dense(12,input_shape = (n_inputs,)))
    model.add(Activation('relu'))
    model.add(Dense(1,input_shape = (n_inputs,)))
    model.add(Activation('sigmoid'))

    model.compile(loss='mse',optimizer='adam')
    return model

def generate_population(size,n_inputs):
    p = []
    for _ in range(size):
        p.append(create_model(n_inputs))
    return p

def model_crossover(parent1,parent2,gens_to_swap):
    model1 = parent1[1]
    model2 = parent2[1]
    weight1 = model1.get_weights()
    weight2 = model2.get_weights()
    new_weight1=weight1
    new_weight2=weight1
    for _ in range(gens_to_swap):
        gen = randint(0,len(new_weight1)-1)
        new_weight1[gen] = weight2[gen]
        new_weight2[gen] = weight1[gen]
    model1.set_weights(new_weight1)
    model2.set_weights(new_weight2)
    parent1[1] = model1
    parent1[1] = model2
    return parent1,parent2

def model_mutate(individual,mutate_probability,gens_to_mutate):
    modified = 0
    model = individual[1]
    weights = model.get_weights()
    for i in range(len(weights)-1):
        if (uniform(0,1)<mutate_probability) and gens_to_mutate:
            weights[i] = weights[i]*uniform(0,2)
            modified += 1
    model.set_weights(weights)
    individual[1] = model
    return individual

def over_population(population,individuals_to_crossover,gens_to_swap,gens_to_mutate,mutate_probability):
    for ix1,p1 in enumerate(population):
        for ix2,p2 in enumerate(population):
            if individuals_to_crossover == 0:
                return population
            if (ix1 != ix2):
                individuals_to_crossover -= 1
                parent1,parent2 = model_crossover(p1,p2,gens_to_swap)
                parent1 = model_mutate(parent1,mutate_probability,gens_to_mutate)
                parent2 = model_mutate(parent2,mutate_probability,gens_to_mutate)
                population[ix1] = parent2
                population[ix2] = parent2
    print("Not enought individuals to crossover")
