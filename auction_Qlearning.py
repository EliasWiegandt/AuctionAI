import secondprice_class as sc
import payasyoubid_class as pc
import combinatorial_class as cc
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
os.chdir(dname)  # Set path to working directory

np.random.seed(10)
random.seed(a=10)
printruns = False
visualize = False
convtest = False

ngoods = 4
minprice = 25
resprice = 20
pricestep = 5

alpha = 0.01
ntrain = 1000
nmix = 1000
ntest = 1000
logsuf = ""
bidspace = [0.0, 1.0, 2.0]
fixbidspace = [2.0, 1.0, 1.0, 0.0]
valspace = [35]
convtest = False
convwin = 10000
convstep = int(convwin / 100)
convsig = 0.01

# Convert bids and values to floats
bidspace = [float(i) for i in bidspace]
valspace = [float(i) for i in valspace]

bidder1 = bc.Bidder(
    name="bidder1",
    fixbid=False,
    bidspace=bidspace,
    valspace=valspace,
    learning=True,
    alpha=alpha,
    logsuf=logsuf)

bidder2 = bc.Bidder(
    name="bidder2",
    fixbid=True,
    bidspace=fixbidspace,
    valspace=valspace,
    learning=True,
    alpha=alpha,
    logsuf=logsuf)

bidder3 = bc.Bidder(
    name="bidder3",
    bidspace=fixbidspace,
    fixbid=True,
    valspace=valspace,
    learning=True,
    alpha=alpha,
    logsuf=logsuf)

bidders = [bidder1, bidder2, bidder3]

# auction = pc.payasyoubidauction(bidders, ngoods = ngoods, minprice = minprice)
# auction = sc.secondpriceauction(bidders, ngoods = ngoods, minprice = minprice)
auction = cc.combiclock(
    ngoods=ngoods,
    minprice=minprice,
    pricestep=pricestep,
    resprice=resprice,
    bidders=bidders)

log = lc.auctionlog()

simulator = se.auctionsimulator(
    auction=auction,
    bidders=bidders,
    log=log,
    ntrain=ntrain,
    nmix=nmix,
    ntest=ntest,
    convtest=convtest,
    convwin=convwin,
    convstep=convstep,
    convsig=convsig,
    printruns=printruns,
    visualize=visualize)

setupend = t.default_timer()

simulator.simulateauction()

progend = t.default_timer()
setuptime = '{0:.{1}f}'.format(setupend - progstart, 1)
progtime = '{0:.{1}f}'.format(progend - setupend, 1)

print("Time spent on setup: ", setuptime, " seconds")
print("Time spent on program: ", progtime, " seconds")
