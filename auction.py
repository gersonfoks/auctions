class Auction:

    def __init__(self, items, persons):
        self.items = items
        self.persons = persons

    def get_highest_bid_pay(self, bundle_allocation):
        return sum([person.get_price(bundle) for (person, bundle) in bundle_allocation.items()])


class Person:
    def __init__(self, id, bundle, price):
        self.id = id
        self.bundle = bundle
        self.price = price

    def get_price(self, bundle):
        return self.price if self.bundle.issubset(bundle) else 0


    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)