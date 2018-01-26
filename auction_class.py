# Create auction class
import numpy as np
from scipy.stats import rankdata

class secondprice:
    def __init__(self, ngoods = 1, minprice = 0):
        self.minprice = minprice
        self.ngoods = ngoods


    def bidfilter(self, bidder):
        """
        Filters valid actions of bidders by the auction-specific criterias
        In:  bidder (class)
        Out: validbids (list of valid actions of bidder filtered by auction criteria)
        """
        validbids = bidder.bidspace
        return validbids


    def evaluate(self, bids):
        """
        Runs second-price auction where max one good can be awarded to each bidder
        In: list of boolean indicator of bid, list of A-block bids
        Out: list of awarded blocks, list of prices
        """
        boolbids = []
        for bid in bids:

            boolbids.append(bid >= self.minprice)
        ngoods = [None] * len(bids)
        prices = []
        price = None
        auctionclose = False

        if sum(boolbids) > self.ngoods: # More bidders than blocks
            ordixs = list(range(len(bids)))
            ordbids = sorted(ordixs, key=lambda k: bids[k], reverse=True)
            price = bids[ordbids[self.ngoods]]
            ranks = rankdata(bids, method='max') - 1
            ranks = np.ones_like(ranks)*(len(ranks)-1) - ranks # Reverse ranks

            # Check if a random choice is needed between bidders
            ranchoice = False
            inauc = sum(ranks < self.ngoods)
            if inauc > self.ngoods:
                ranchoice = True
                kickrank = max(ranks[ranks < self.ngoods])
                nkick = inauc - self.ngoods
                nkickrank = sum(ranks == kickrank)
                kickspace = np.arange(start = 1,
                                      stop = nkickrank + 1,
                                      step = 1)
                kickchoice = np.random.choice(kickspace,
                                              size=nkick,
                                              replace=False,
                                              p=None)

            # Determine who gets blocks
            nkicked = 1
            for index, rank in enumerate(ranks):
                if ranchoice:
                    if rank < kickrank:
                        ngoods[index] = True
                    elif rank == kickrank:
                        if not(nkicked in kickchoice):
                            ngoods[index] = True
                            nkicked += 1
                        else:
                            ngoods[index] = False
                            nkicked += 1
                    else:
                        ngoods[index] = False
                else:
                    ngoods[index] = rank < self.ngoods

            # Write array with prices
            for n in ngoods:
                if n:
                    prices.append(price)
                else:
                    prices.append(n)

        else: # This is activated when there are more or equal blocks than bidders
            ngoods = boolbids
            for n in ngoods:
                if n:
                    prices.append(self.minprice)
                    price=self.minprice
                else:
                    prices.append(n)
        auctionclose = True
        return ngoods, prices, auctionclose

class payasyoubid:
    def __init__(self, ngoods = 1, minprice = 0):
        self.minprice = minprice
        self.ngoods = ngoods


    def bidfilter(self, bidder):
        """
        Filters valid actions of bidders by the auction-specific criterias
        In:  bidder (class)
        Out: validbids (list of valid actions of bidder filtered by auction criteria)
        """
        validbids = bidder.bidspace
        return validbids


    def evaluate(self, bids):
        """
        Runs second-price auction where max one good can be awarded to each bidder
        In: list of boolean indicator of bid, list of A-block bids
        Out: list of awarded blocks, list of prices
        """
        boolbids = []
        for bid in bids:

            boolbids.append(bid >= self.minprice)
        ngoods = [None] * len(bids)
        prices = []
        price = None
        auctionclose = False

        if sum(boolbids) > self.ngoods: # More bidders than blocks
            ordixs = list(range(len(bids)))
            ordbids = sorted(ordixs, key=lambda k: bids[k], reverse=True)
            price = bids[ordbids[self.ngoods]]
            ranks = rankdata(bids, method='max') - 1
            ranks = np.ones_like(ranks)*(len(ranks)-1) - ranks # Reverse ranks

            # Check if a random choice is needed between bidders
            ranchoice = False
            inauc = sum(ranks < self.ngoods)
            if inauc > self.ngoods:
                ranchoice = True
                kickrank = max(ranks[ranks < self.ngoods])
                nkick = inauc - self.ngoods
                nkickrank = sum(ranks == kickrank)
                kickspace = np.arange(start = 1,
                                      stop = nkickrank + 1,
                                      step = 1)
                kickchoice = np.random.choice(kickspace,
                                              size=nkick,
                                              replace=False,
                                              p=None)

            # Determine who gets blocks
            nkicked = 1
            for index, rank in enumerate(ranks):
                if ranchoice:
                    if rank < kickrank:
                        ngoods[index] = True
                    elif rank == kickrank:
                        if not(nkicked in kickchoice):
                            ngoods[index] = True
                            nkicked += 1
                        else:
                            ngoods[index] = False
                            nkicked += 1
                    else:
                        ngoods[index] = False
                else:
                    ngoods[index] = rank < self.ngoods

            # Write array with prices
            for n in ngoods:
                if n:
                    prices.append(price)
                else:
                    prices.append(n)

        else: # This is activated when there are more or equal blocks than bidders
            ngoods = boolbids
            for n in ngoods:
                if n:
                    prices.append(self.minprice)
                    price=self.minprice
                else:
                    prices.append(n)
        auctionclose = True
        return ngoods, prices, auctionclose
