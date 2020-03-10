from itertools import chain, combinations
import numpy as np


def powerset(iterable):
    # https://stackoverflow.com/questions/18035595/powersets-in-python-using-itertools
    s = list(iterable)
    return chain.from_iterable([set(x) for x in combinations(s, r)] for r in range(len(s) + 1))


def create_bundle_allocation_from_item_allocation(item_allocation):
    result = dict()
    for i, person in enumerate(item_allocation):
        if person not in result:
            result[person] = {i}
        else:
            result[person].add(i)

    # Make sure the bundles are tuples are tuples
    return result


def get_random_allocation_from_preferences(auction):
    # Creates a random allocation, in which random persons get exactly what they want.
    items_to_select = auction.items.copy()  # Copy the items to a new set
    persons_to_select = auction.persons.copy()

    allocation = [None for i in range(len(auction.items))]
    while len(persons_to_select):
        person = np.random.choice(persons_to_select)
        persons_to_select.remove(person)
        bundle = person.bundle
        for item in bundle:
            if item in items_to_select:
                allocation[item] = person
                items_to_select.remove(item)
    for item in items_to_select:
        allocation[item] = np.random.choice(auction.persons)
    return allocation


def get_random_allocation(auction):
    # Creates a random allocation, in which random persons get exactly what they want.

    persons_to_select = auction.persons.copy()

    allocation = [np.random.choice(persons_to_select) for i in range(len(auction.items))]

    return allocation


def count_numbers_below_zero(array):
    return len([i for i in array if i < 0])
