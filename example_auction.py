from auction import Person, Auction
from utils import powerset, create_bundle_allocation_from_item_allocation, get_random_allocation_from_preferences

items = {
   i for i in range(4)
}


#Persons to bid
person_1 = Person(1, {2, 3}, 1)
person_2 = Person(2, {2,3}, 1)

#Highest bid auction
auction = Auction(items, [person_1, person_2])

#An example allocation
allocation_1 = [
    person_2, person_1, person_2, person_1
]

bundle_allocation_1 = create_bundle_allocation_from_item_allocation(allocation_1)


random_allocation = get_random_allocation_from_preferences(auction)
print(random_allocation)
random_bundle_allocation = create_bundle_allocation_from_item_allocation(random_allocation)
print(auction.get_highest_bid_pay(random_bundle_allocation))