# A list of auctions which we can use to test our algorithm on


# Creates an auction in which every person wants exactly one item (with no overlap)
from auction import Person, Auction
import numpy as np

fixed_price_function = lambda x: 1
size_price_function = lambda x: len(x)

random_price_function = lambda x: np.random.rand()
random_size_price_function = lambda x: len(x) * np.random.rand()

# An auction in which every person exactly wants one item for price of 1
def create_different_minded_auction(n_items, price_function=fixed_price_function):
    items = set([])
    persons = []
    for i in range(n_items):
        bundle = {i, }
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    return Auction(items, persons)

# def random_auction(n_items, n_persons):
#     items = set([i for i in range(n_items)])
#     for i in range(n_persons):
#         bundle = np.random
