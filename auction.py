from numpy import argmax


class Auction:

    def __init__(self, items, persons):
        self.items = items
        self.persons = persons

    def get_highest_bid_pay(self, bundle_allocation):
        return sum([person.get_price(bundle) for (person, bundle) in bundle_allocation.items()])


    def get_sub_auctions(self):
        sub_auctions = []
        for person in self.persons:
            new_persons = self.persons.copy()
            new_persons.remove(person)
            sub_auctions.append(Auction(self.items, new_persons))
        return sub_auctions

    def get_bundles(self):
        return [(person.bundle, person.price) for person in self.persons]

    def get_highest_bidder(self):
        i = argmax([person.price for person in self.persons])
        return self.persons[i]

    def get_price_for_person(self, bundles, excluded_person):
        return sum([person.get_price(bundle) for (person, bundle) in bundles.items() if person != excluded_person])

    def get_approximate_price(self, bundle_allocation):
        return sum([person.get_approximate_price(bundle) for (person, bundle) in bundle_allocation.items()])

    def get_social_welfare(self, bundles, prices):
        return self.get_highest_bid_pay(bundles) - sum(prices)

class Person:
    def __init__(self, id, bundle, price):
        self.id = id
        self.bundle = bundle
        self.price = price

    def get_price(self, bundle):
        return self.price if self.bundle.issubset(bundle) else 0

    def get_approximate_price(self, bundle):
        if self.bundle == {}:
            return 0
        return self.price * (len(self.bundle.intersection(bundle))/ len(self.bundle))


    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)