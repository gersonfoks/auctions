from auction import Auction, Person
import numpy as np
from utils import powerset

constant_price_function = lambda x: 1
random_prize_function_zero_to_ten = lambda x: np.random.randint(11)
random_prize_function_zero_to_hundred = lambda x: np.random.randint(101)
random_prize_function_uniform = lambda x: np.random.rand()
linear_prize_function = lambda x: max(x)
sum_prize_function = lambda x: sum(x)


def create_non_overlapping_auction(n_items, price_function=constant_price_function):
    items = set([])
    persons = []
    for i in range(n_items):
        bundle = {i, }
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    return Auction(items, persons)


def create_overlapping_auction(n_items, price_function=random_prize_function_zero_to_ten):
    items = set([])
    persons = []
    for i in range(n_items - 1):
        bundle = {i, i + 1}
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    return Auction(items, persons)


def create_monopolist_bidder_auction(n_items, n_persons=None, price_function=constant_price_function):
    items = set([])
    persons = []
    if n_persons:
        n_persons = n_items
    for i in range(n_persons - 1):
        bundle = {i, }
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    persons.append(Person(n_persons, {i for i in range(n_items)}, 100))
    return Auction(items, persons)


def create_n_olist_bidder_auction(n_items, n_olisten_prices, n_persons, price_function=constant_price_function):
    items = set([i for i in range(n_items)])
    persons = []
    if n_persons:
        n_persons = n_items
    for i in range(n_persons - len(n_olisten_prices)):
        bundle = {i, }
        persons.append(Person(i, bundle, price_function(bundle)))

    for i in range(len(n_olisten_prices)):
        persons.append(Person(n_persons + i, {i for i in range(n_items)}, n_olisten_prices[i]))
    return Auction(items, persons)


def create_random_crazy_high_bidder_auction(n_items, n_persons=None, price_function=constant_price_function):
    if n_persons == None:
        n_persons = n_items
    items = set([i for i in range(n_items)])
    bundles = [*powerset(items)]
    persons = []
    for i in range(n_persons):
        bundle = np.random.choice(bundles)
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    persons[np.random.randint(n_persons)].price = max([p.price for p in persons]) * 100
    return Auction(items, persons)


def create_overlapping_with_crazy_high_bidder_auction(n_items, price_function=random_prize_function_zero_to_ten):
    items = set([])
    persons = []
    for i in range(n_items - 1):
        bundle = {i, i + 1}
        persons.append(Person(i, bundle, price_function(bundle)))
        items.add(i)
    # Pick one random person and set his price to 10 times the highest bid
    persons[np.random.randint(n_items - 1)].price = max([p.price for p in persons]) * 10
    return Auction(items, persons)


def create_random_auction(n_items, n_persons, price_function=random_prize_function_zero_to_ten):
    items = set([i for i in range(n_items)])
    persons = []
    p_set = list(powerset(items))
    for i in range(n_persons):
        # Don't allow an empty bundle
        while True:
            bundle = set(np.random.choice(p_set))
            if bundle:
                break
        persons.append(Person(i, bundle, price_function(bundle)))
    return Auction(items, persons)
