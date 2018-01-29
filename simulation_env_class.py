import random
import matplotlib.pyplot as plt
import timeit as t
import numpy as np
import pandas as pd
import auction_ai_visualizations as av

class auctionsimulator:
    def __init__(self,
                 auction,
                 bidders,
                 log,
                 ntrain,
                 nmix,
                 ntest,
                 convtest,
                 convwin,
                 convstep,
                 convsig,
                 printruns = False,
                 visualize = False,
                 globalvalgood = False,
                 globalbidspace = []
                 ):
        self.auction = auction
        self.bidders = bidders
        self.log = log
        self.ntrain = ntrain
        self.nmix = nmix
        self.ntest = ntest
        self.convtest = convtest
        self.convwin = convwin
        self.convstep = convstep
        self.convsig = convsig
        self.printruns = printruns
        self.visualize = visualize
        self.globalvalgood = globalvalgood
        self.globalbidspace = globalbidspace


    def findstates(self, input = []):
        states = []
        for bidder in self.bidders:
            state = bidder.buildstate(input)
            states.append(state)
        return states


    def findbids(self, phase, states):
        bids = []
        for bidder, state in zip(self.bidders, states):
            filteredbidspace = self.auction.bidfilter(bidder)
            bidder.createQ(state, filteredbidspace)
            bid = bidder.chooseaction(phase, state, filteredbidspace)
            bids.append(bid)
        return bids


    def auctionrun(self, bids):
        ngoods, prices, auctionclose = self.auction.evaluate(bids)
        return ngoods, prices, auctionclose


    def findrewards(self, ngoods, prices, valgoods):
        rewards = []
        for bidder, ngood, price, valgood in zip(self.bidders, ngoods, prices, valgoods):
            reward = bidder.rewardfunc(ngood, price, valgood)
            rewards.append(reward)
        return rewards


    def learn(self, states, bids, rewards):
        for bidder, state, bid, reward in zip(self.bidders, states, bids, rewards):
            bidder.learn(state, bid, reward)
        return None


    def writeroundlog(self, runtotal, phase, bids, ngoods, prices, valgoods, rewards):
        self.log.writerunlog(self.bidders,
                             runtotal,
                             phase,
                             bids,
                             ngoods,
                             prices,
                             valgoods,
                             rewards)
        for bidder in self.bidders:
            bidder.writeQlog(runtotal, phase)
        return None


    def checkconv(self, runtotal):
        trainconv = False
        print("Testing for convergence")
        adfstart = t.default_timer()
        unconverged = 0
        for bidder in self.bidders:
            booQconv = bidder.Qconv(window = self.convwin,
                                    sig = self.convsig,
                                    step = self.convstep)
            # print(booQconv)
            if booQconv == False:
                unconverged += 1
        if unconverged == 0:
            trainconv = True
            print("Value of strategies have converged after ", runtotal + 1, " trials.")
        else:
            print(unconverged, " bidders still needs to converge.")
        adfend = t.default_timer()
        adftime = adfend - adfstart
        print("Time spent on ADF: ", '{0:.{1}f}'.format(adftime,1), " seconds")
        return trainconv


    def bidderreset(self, phase, runphase, maxrun):
        for bidder in self.bidders:
            bidder.reset(phase, runphase, maxrun)
        return None


    def printinfo(self, runtotal, phase, bids, ngoods, prices, vgoods, rewards):
        if self.printruns:
            print("Trial ", runtotal)
            print("Phase: ", phase)
            print("Bids: ", bids)
            print("Goods awarded: ", ngoods)
            print("Prices: ", prices)
            print("Values of goods:", vgoods)
            print("Rewards: ", rewards)
            print("")
        return None


    def visualizeauctions(self, runtotal):
        if self.visualize:
            # plt1 = av.visQ(self.bidders, self.auction, runtotal)
            plt2 = av.visconv(self.bidders)
            # plt3 = av.vispropreward(self.log.logpath, self.bidders)
            # plt4 = av.visrewards(self.log.logpath, self.bidders)
            # plt5 = av.visuncertainrewards(self.log.logpath, self.bidders)
            # plt6 = av.visviolin(self.log.logpath)

            # plt1.show()
            plt2.show()
            # plt3.show()
            # plt4.show()
            # plt5.show()
            # plt6.show()
        return None


    def updatehistories(self, states, bids):
        for bidder, state, bid in zip(self.bidders, states, bids):
            bidder.updatehistory(state, bid)
        return None


    def resethistories(self):
        for bidder in self.bidders:
            bidder.history = []
        return None


    def findvalues(self):
        valgoods = []
        if self.globalvalgood:
            valgood = random.choice(globalbidspace)
            valgoods = len(self.bidders) * valgood
        else:
            for bidder in self.bidders:
                valgoods.append(bidder.valdraw())
        return valgoods


    def writeQtables(self):
        for bidder in self.bidders:
            bidder.writeQtable()
        return None


    def simulateauction(self):
        maxruns = [self.ntrain, self.nmix, self.ntest]
        phases = ["training", "mixing", "testing"]
        runtotal = 0
        for phase, maxrun in zip(phases, maxruns):
            phasestart = t.default_timer()
            runphase = 0
            trainconv = False
            while runphase < maxrun \
                  and (trainconv == False or phase != "training"):
                auctionclose = False
                self.resethistories()
                self.bidderreset(phase, runphase, maxrun)
                self.auction.resetauction()
                while auctionclose == False:
                    states = self.findstates()
                    bids = self.findbids(phase, states)
                    ngoods, prices, auctionclose = self.auctionrun(bids)
                    self.updatehistories(states, bids)
                valgoods = self.findvalues()
                rewards = self.findrewards(ngoods, prices, valgoods)
                self.learn(states, bids, rewards)
                self.writeroundlog(runtotal, phase, bids, ngoods, prices, valgoods, rewards)
                if phase == "training" \
                   and self.convtest == True \
                   and np.fmod(runphase + 1, self.convwin) == 0:
                    trainconv = self.checkconv(runtotal)
                runphase += 1
                runtotal += 1
                self.printinfo(runtotal, phase, bids, ngoods, prices, valgoods, rewards)
            phaseend = t.default_timer()
            phasetime = '{0:.{1}f}'.format(phaseend - phasestart, 1)
            print("Time used on ", phase,": ", phasetime, " seconds")
        self.writeQtables()
        self.visualizeauctions(runtotal)
        return None
