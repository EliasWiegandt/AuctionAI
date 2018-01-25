import auction_class as ac
import bidder_class as bc
import log_class as lc
import simulation_env_class as se
import os
import numpy as np
import random
import timeit as t
import matplotlib.pyplot as plt

progstart = t.default_timer()

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname) # Set path to working directory
# manager = plt.get_current_fig_manager()
# manager.window.showMaximized()



np.random.seed(10)
random.seed(a=10)
printruns = False
visualize = False
convtest = False

ngoods = 2
minprice = 0

alpha = 0.0001
ntrain = 1000000
nmix = 0
ntest = 0
logsuf = ""
bidspace = [80.0, 90.0, 100.0]
valspace = [94.0]
convtest = True
convwin = 50000
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

setupend = t.default_timer()

simulator.simulateauction()

progend = t.default_timer()

print("Time spent on setup: ", setupend - progstart, " seconds")
print("Time spent on program: ", progend - setupend, " seconds")
