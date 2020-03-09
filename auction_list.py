# A list of auctions which we can use to test our algorithm on
from generate_auctions import *

#List of auctions that we know the right answer to

#Every persons wants a different item
# Person 1 want item 0 and 1, person 2 wants 1 and 2, person 3 wants 2 and 3 etc...
non_overlapping = create_non_overlapping_auction(10)
non_overlapping_util = 10
non_overlapping_price = [0 for i in range(10)]





overlapping = create_overlapping_auction(10)

# Monopolist There is one crazy high bidder who wants all the items
mono_auction = create_n_olist_bidder_auction(100, [100], 100)
highest_bider = mono_auction.get_highest_bidder()


#Duo list
duo_auction = create_n_olist_bidder_auction(50, [100, 102], 50)

# Competing crazy. There are two or more competing crazy high bidders who want all the items

random_auction = create_random_auction(10, 50)