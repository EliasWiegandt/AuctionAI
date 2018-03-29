# Create auction class
import random

class combiclock:
    def __init__(self, bidders, ngoods = 1, minprice = 0, pricestep = 1, resprice = 1):
        self.minprice = minprice
        self.ngoods = ngoods
        self.pricestep = pricestep
        self.price = minprice
        self.biddict = {}
        self.pricedict = {}
        self.r = 1 # To be incremented
        self.resprice = resprice
        self.bidders = bidders


    def bidfilter(self, bidder):
        """
        Filters valid actions of bidders by the auction-specific criterias
        In:  bidder (class)
        Out: validbids (list of valid actions of bidder filtered by auction criteria)
        """
        if self.r > 1:
            lastbid = self.biddict[bidder.name][str(self.r - 1)]
            validbids = []
            for posbid in bidder.bidspace:
                if posbid <= lastbid:
                    validbids.append(posbid)
        else:
            validbids = bidder.bidspace
        return validbids


    def findinput(self):
        bidderinput = self.pricedict[str(self.r)]
        return bidderinput


    def resetauction(self):
        self.r = 1
        self.inibiddict(self.bidders)
        self.inipricedict()
        return None


    def inibiddict(self, bidders):
        for bidder in bidders:
            self.biddict[bidder.name] = {}
            self.biddict[bidder.name][str(0)] = 0.0
        return None


    def inipricedict(self):
        self.pricedict[str(0)] = self.resprice
        self.pricedict[str(1)] = self.minprice
        return None


    def incperm(self, perm, base, ciphers):
        perm[-1] += 1
        # perm[ciphers-1] = perm[ciphers-1] + 1
        for ix in reversed(range(ciphers)):
            if perm[ix] > base:
                perm[ix] = 0
                perm[ix - 1] += 1
        # print(perm)
        return perm


    def evaluate(self, bids):
        # Place in dict
        round = str(self.r)
        nbidders = len(self.bidders)
        # print(bids)

        for bid, bidder in zip(bids, self.bidders):
            self.biddict[bidder.name][str(self.r)] = bid

        # Find feasible combinations
        bidslist = []
        for bidder in self.bidders:
            bidlist = []
            for key in range(self.r+1):
                bidlist.append(self.biddict[bidder.name][str(key)])
            bidslist.append(bidlist)
        # print(bidslist)

        permsfound = False
        ciphers = nbidders
        base = self.r
        perm = [0] * ciphers
        permdict = {}
        permdict[str(0)] = perm
        permix = 1
        while permsfound == False:
            perm = self.incperm(perm[:], base, ciphers)
            permdict[permix] = perm
            if sum(perm) == base * ciphers:
                permsfound = True
            permix += 1

        # Find sum of goods in all perms
        # print(permdict)
        sumdict = {}
        ngoodsdict = {}
        for permix, perm in permdict.items():
            sumgoods = 0
            ngoodslist = []
            for ix, n in enumerate(perm):
                ngoods = bidslist[ix][n]
                ngoodslist.append(ngoods)
                sumgoods += ngoods
            sumdict[permix] = sumgoods
            ngoodsdict[permix] = ngoodslist

        # print(sumdict)

        # Select perms where all goods are distributed
        feapermdict = {}
        for permix, ngoods in sumdict.items():
            # print(ngoods)
            if ngoods <= self.ngoods:
                feapermdict[permix] = permdict[permix]

        # Find value of all perms that alot correctly
        # print("Feasible perms:")
        # print(feapermdict)
        valdict = {}
        feapricedict = {}
        for permix, perm in feapermdict.items():
            valbids = 0
            pricelist = []
            for ix, n in enumerate(perm):
                # print(n)
                price = self.pricedict[str(n)]
                pricelist.append(price)
                bid = bidslist[ix][n]
                # print(bid)
                # print(price)
                valbids += bid * price
            valres = (self.ngoods - sumdict[permix]) * self.resprice
            valperm = valbids + valres
            valdict[permix] = valperm
            feapricedict[permix] = pricelist

        # print("values:")
        # print(valdict)
        # Choose perm with highest value, random choice if several perms have the max value
        maxval = max(valdict.values())
        maxvalpermix = random.choice([key for key, val in valdict.items() if val == maxval])

        maxperm = permdict[maxvalpermix]
        maxval = valdict[maxvalpermix]
        maxprices = feapricedict[maxvalpermix]
        maxngoods = ngoodsdict[maxvalpermix]

        # print("Winning combination:")
        # print(maxngoods)
        # print(maxprices)
        # print(maxval)

        # Check if perm with highest value fits with closing criterions
        closingcriterion = True
        for n in maxngoods:
            if n == 0.0:
                closingcriterion = False
        if 0.0 not in bids:
            # print("Is 0.0 in this shit?")
            # print("The bids-------------------------")
            # print(bids)
            closingcriterion = False

        # Unless all bids are zero, in which case the auction just closes
        if sum(bids) == 0 and closingcriterion == False:
            closingcriterion = True
            maxngoods = [0.0] * nbidders
            maxprices = [0.0] * nbidders

        # If not: increase prices, run again
        if closingcriterion == False:
            self.r += 1
            # print("run again")
            self.pricedict[str(self.r)] = self.pricedict[round] + self.pricestep

        return maxngoods, maxprices, closingcriterion
