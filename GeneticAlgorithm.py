import numpy as np
from utils import get_random_allocation, create_bundle_allocation_from_item_allocation


class GeneticAlgorithm():
    def __init__(self, auction, max_iter=1, pop_size=5, mutation_rate=0.05):
        self.auction = auction
        self.max_iter = max_iter
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

    def fitness(self, alloc):
        # Fitness score is equal to the social welfare
        return self.auction.get_highest_bid_pay(create_bundle_allocation_from_item_allocation(alloc))

    def calculate(self):
        # Create first population
        population = [
            get_random_allocation(self.auction)
            for _ in range(self.pop_size)
        ]

        iter = 0
        while iter < self.max_iter:
            # Calculate fitness of population
            fitness_scores = [self.fitness(alloc) for alloc in population]

            # Probability to be chosen for breeding is proportional to fitness score
            reproduce_probs = np.array(fitness_scores) / sum(fitness_scores)

            # Create new population by repeatedly choosing two parents using
            # these probabilities and breeding them
            indices = [i for i in range(len(fitness_scores))]
            new_pop = []
            for _ in range(self.pop_size):
                parents = np.random.choice(indices, 2, p=reproduce_probs, replace=True)
                new_pop.append(self.breed(population[parents[0]], population[parents[1]]))
            iter += 1
        
            # TODO: convergence condition to break out of loop?

        # Calculate fitness of each member of final population
        fitness_scores = [self.fitness(alloc) for alloc in population]
        max_val = max(fitness_scores)

        # Return member with highest fitness
        return population[fitness_scores.index(max_val)]

    def breed(self, p1, p2):
        # Each person gets randomly (50/50) allocated the allocation of parent 1 or parent 2
        child = [
            np.random.choice([p1[i], p2[i]]) 
            for i in range(len(p1))
        ]
        return self.mutate(child)
     

    def mutate(self, alloc):
        # Each item allocation gets mutated with probability mutation_rate
        # A mutation is a random allocation to a person (including the one
        # it was already allocated to)
        for i in range(len(alloc)):
            if np.random.uniform() < self.mutation_rate:
                alloc[i] = np.random.choice(self.auction.persons)
        return alloc

    