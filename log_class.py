import os
import csv

class auctionlog():
    def __init__(self):
        self.logpath = os.path.join("logs", "auction_run_log" + ".csv")
        self.logfields = ['runtotal',
                          'name',
                          'phase',
                          'valspace',
                          'bid',
                          'ngood',
                          'price',
                          'valgood',
                          'reward']
        self.logfile = open(self.logpath, 'w', newline='')
        self.logwriter = csv.DictWriter(self.logfile, fieldnames=self.logfields)
        self.logwriter.writeheader()

        return None


    def writerunlog(self,
                    bidders,
                    runtotal,
                    phase,
                    ngoods,
                    prices,
                    valgoods,
                    rewards):

        for ix, bidder in enumerate(bidders):
            self.logwriter.writerow({
                'runtotal': runtotal,
                'name': bidder.name,
                'phase': phase,
                'valspace': bidder.valspace,
                'bid': bidder.bidhistory,
                'ngood': ngoods[ix],
                'price': prices[ix],
                'valgood': valgoods[ix],
                'reward': rewards[ix]})

        return None
