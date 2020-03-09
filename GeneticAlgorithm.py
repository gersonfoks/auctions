from abc import abstractmethod

import numpy as np
from utils import get_random_allocation, create_bundle_allocation_from_item_allocation


class AuctionSearch:
    def __init__(self, auction, max_iter=1):
        self.auction = auction
        self.max_iter = max_iter

    def calculate(self):
        '''
        Calculates the best allocation
        :return:
        '''
        pass


class RandomSearch(AuctionSearch):

    def calculate(self):
        solutions = [
            get_random_allocation(self.auction) for _ in range(self.max_iter)
        ]
        fitness_scores = [self.auction.get_highest_bid_pay(
            create_bundle_allocation_from_item_allocation(alloc)) for alloc in solutions]
        max_val = max(fitness_scores)
        return solutions[fitness_scores.index(max_val)]


class GeneticAlgorithm(AuctionSearch):
    def __init__(self, auction, max_iter=1, pop_size=5, mutation_rate=0.1):
        super().__init__(auction, max_iter)
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate

    @abstractmethod
    def fitness(self, allocation):
        raise NotImplementedError("Define your fitness function")

    def calculate(self):
        # Create first population
        population = []

        iter = 0

        best = None
        best_score = -np.math.inf
        while iter < self.max_iter:
            fresh_pop = [get_random_allocation(self.auction) for _ in range(self.pop_size)]
            population = population + fresh_pop
            # Calculate fitness of population
            fitness_scores = [self.fitness(alloc) for alloc in population]

            max_val = max(fitness_scores)
            if best_score < max_val:
                best_score = max_val
                best = population[fitness_scores.index(max_val)]

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

        # Return member with highest fitness
        return best

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


class GeneticAlgorithmContinuous(GeneticAlgorithm):
    def __init__(self, auction, max_iter=1, pop_size=5, mutation_rate=0.1):
        super().__init__(auction, max_iter, pop_size, mutation_rate)

    def fitness(self, alloc):
        # Fitness score is equal to the social welfare
        return self.auction.get_approximate_price(create_bundle_allocation_from_item_allocation(alloc))


class GeneticAlgorithmDiscreet(GeneticAlgorithm):
    def fitness(self, alloc):
        # Fitness score is equal to the social welfare
        return self.auction.get_highest_bid_pay(create_bundle_allocation_from_item_allocation(alloc))


def get_prices(auction, algorithm=GeneticAlgorithmContinuous, settings=None):
    sub_auctions = auction.get_sub_auctions()
    main_alg = algorithm(auction, **settings)

    main_allocation = main_alg.calculate()

    sub_allocations = []
    for auc in sub_auctions:
        alg = algorithm(auc, **settings)
        sub_allocations.append(alg.calculate())

    return prices_from_allocations(auction, main_allocation, sub_auctions, sub_allocations)


def prices_from_allocations(auction, main_allocation, sub_auctions, sub_allocation):
    main_bundles = create_bundle_allocation_from_item_allocation(main_allocation)
    prices = []
    for person, sub_auction, alloc in zip(auction.persons, sub_auctions, sub_allocation):
        sub_bundle = create_bundle_allocation_from_item_allocation(alloc)
        sub_welfare = sub_auction.get_highest_bid_pay(sub_bundle)
        main_welfare = auction.get_price_for_person(main_bundles, person)
        prices.append(sub_welfare - main_welfare)
    return prices
