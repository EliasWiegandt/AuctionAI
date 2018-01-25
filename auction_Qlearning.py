import auction_class as ac
import bidder_class as bc
import log_class as lc
import simulation_env_class as se
import os
import numpy as np
import random

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname) # Set path to working directory

np.random.seed(10)
random.seed(a=10)

printruns = False
visualize = True
convtest = False

ngoods = 2
minprice = 90

alpha = 0.0001
ntrain = 1000
nmix = 0
ntest = 0
logsuf = ""
bidspace = [80.0, 90.0, 100.0]
valspace = [90.0]
convtest = True
convwin = 1000000
convstep = int(convwin / 50)
convsig = 0.01

bidder1 = bc.Bidder(name = "bidder1",
                     bidspace = bidspace,
                     valspace = valspace,
                     learning = True,
                     alpha = alpha,
                     logsuf = logsuf)

bidder2 = bc.Bidder(name = "bidder2",
                     bidspace = bidspace,
                     valspace = valspace,
                     learning = True,
                     alpha = alpha,
                     logsuf = logsuf)

bidder3 = bc.Bidder(name = "bidder3",
                     bidspace = bidspace,
                     valspace = valspace,
                     learning = True,
                     alpha = alpha,
                     logsuf = logsuf)

bidders = [bidder1, bidder2, bidder3]

auction = ac.secondpriceauction(ngoods = ngoods, minprice = minprice)

log = lc.auctionlog()

simulator = se.auctionsimulator(auction = auction,
                             bidders = bidders,
                             log = log,
                             ntrain = ntrain,
                             nmix = nmix,
                             ntest = ntest,
                             convtest = convtest,
                             convwin = convwin,
                             convstep = convstep,
                             convsig = convsig,
                             printruns = printruns,
                             visualize = visualize)

simulator.simulateauction()
