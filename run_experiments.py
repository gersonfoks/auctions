from GeneticAlgorithm import *
from generate_auctions import *
from utils import count_numbers_below_zero
import csv


settings_genetic = {
    "max_iter": 100,
    "pop_size": 25
}


settings_random = {
    "max_iter": settings_genetic["max_iter"] * settings_genetic["pop_size"],
}

n_rounds = 10
cont_prices_results = []
discreet_results = []
mixed_results = []
random_results = []

auction_types = {
    (5,5): [
        create_random_auction(5, 5) for i in range(n_rounds)
    ],
    (10, 5): [
        create_random_auction(10, 5) for i in range(n_rounds)
    ],
    (20, 5): [
        create_random_auction(20, 5) for i in range(n_rounds)
    ],
    (5, 10): [
        create_random_auction(5, 10) for i in range(n_rounds)
    ],
    (5, 20): [
        create_random_auction(5, 20) for i in range(n_rounds)
    ],

}


to_try = [
    (GeneticAlgorithmDiscreet, settings_genetic),
   (GeneticAlgorithmContinuous, settings_genetic),
   (GeneticAlgorithmMixed, settings_genetic),
   (RandomSearch, settings_random),
]


def run_auctions(auctions, alg, settings):
    allocations = []
    prices = []
    sws = []
    for auc in auctions:
        al, pr, sw = run_experiment(auc, alg, settings)

        allocations.append(al)
        prices.append(pr)
        sws.append(sw)

    return allocations, prices, sws


allocation_results = []
prices_results = []
sws_results = []
for alg, settings in to_try:
    with open("{}_results.csv".format(alg.get_name()), "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["items", "bidders", "name" ,"below 0", "mean", "std"])
        for name, auctions in auction_types.items():
            allocations, prices, sws = run_auctions(auctions, alg, settings)
            print(name)
            below_zero = sum([count_numbers_below_zero(pr) for pr in prices])
            print(below_zero)
            print(np.mean(sws))
            print(sws)
            print(np.std(sws))
            writer.writerow([name[0], name[1],  "{}".format(name) ,below_zero, np.mean(sws), np.std(sws)])

