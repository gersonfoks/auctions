from GeneticAlgorithm import *
from auction_list import *
from generate_auctions import *
from utils import create_bundle_allocation_from_item_allocation

auction = random_auction

settings_genetic = {
    "max_iter": 10,
    "pop_size": 5
}
#allocation = algorithm.calculate()
#bundle_allocation = create_bundle_allocation_from_item_allocation(allocation)

settings_random = {
 "max_iter": settings_genetic["max_iter"] * settings_genetic["pop_size"],
}

n_rounds = 10
cont_results = []
discreet_results = []
random_results = []
for i in range(n_rounds):
    print("start round: {}".format(i))
    random_auction = create_random_auction(5, 5)
    cont_results.append(sum(get_prices(random_auction, GeneticAlgorithmContinuous, settings_genetic)))
    discreet_results.append(sum(get_prices(random_auction, GeneticAlgorithmDiscreet, settings_genetic)))
    random_results.append(sum(get_prices(random_auction, RandomSearch, settings_random)))

print(np.mean(cont_results))
print(np.mean(discreet_results))
print(np.mean(random_results))
