from auction_list import create_different_minded_auction, random_price_function
from utils import get_random_allocation, create_bundle_allocation_from_item_allocation


auction = create_different_minded_auction(10**3, random_price_function)

allocation = get_random_allocation(auction)

bundle_allocation = create_bundle_allocation_from_item_allocation(allocation)

print(auction.get_highest_bid_pay(bundle_allocation))