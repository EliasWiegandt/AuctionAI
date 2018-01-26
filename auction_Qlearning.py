import auction_class as ac
import payasyoubid_class as pc
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
visualize = True
convtest = False

ngoods = 2
minprice = 0

alpha  = 0.0001
ntrain = 1000
nmix   = 1000
ntest  = 1000
logsuf = ""
bidspace = [90.0, 95.0, 100.0, 110.0]
valspace = [100.0]
convtest = False
convwin = 10000
convstep = int(convwin / 100)
convsig = 0.01

# Convert bids to floats, to be certain
bidspace = [float(i) for i in bidspace]

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

auction = pc.payasyoubid(ngoods = ngoods, minprice = minprice)
# auction = ac.secondpriceauction(ngoods = ngoods, minprice = minprice)
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
setuptime = '{0:.{1}f}'.format(setupend - progstart, 1)
progtime = '{0:.{1}f}'.format(progend - setupend, 1)

print("Time spent on setup: ", setuptime, " seconds")
print("Time spent on program: ", progtime, " seconds")
