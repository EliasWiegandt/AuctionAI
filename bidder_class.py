import random
import math
import os
import csv
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

class Bidder:
    def __init__(self,
                 name,
                 bidspace,
                 valspace,
                 learning = False,
                 alpha = 0.5,
                 logsuf = ""
                 ):

        self.learning = learning
        self.Q = dict()
        self.alpha = alpha
        self.bidspace = bidspace
        self.valspace = valspace
        self.name = name
        self.logsuf = logsuf

        self.history = []
        self.epsilon = 1.0
        self.input = []

        self.tblname = os.path.join("logs",self.name + self.logsuf + ".txt")
        self.tblfile = open(self.tblname, 'w')
        self.Qlogname = os.path.join("logs", self.name + "_Qlog" + self.logsuf + ".csv")
        self.Qlogfields = [str(bid) for bid in sorted(self.bidspace)]
        self.Qlogfields.insert(0, "runtotal")
        self.Qlogfields.insert(1, "phase")
        self.Qlogfile = open(self.Qlogname, 'w', newline='')
        self.Qlogwriter = csv.DictWriter(self.Qlogfile, fieldnames=self.Qlogfields)
        self.Qlogwriter.writeheader()


    def reset(self, phase, runphase = 0, maxrun = 1):
        if phase == "testing":
            self.epsilon = 0
        elif phase == "mixing":
            # self.epsilon = 0.5
            self.epsilon=self.epsilon - 1 / maxrun  # linear epsilon
        elif phase == "training":
            self.epsilon = 1.0
        return None


    def buildstate(self, inputs):
        state = ("valspace: " + str(self.valspace),
                 "history: " + str(self.history),
                 "inputs: " + str(inputs))
        return state


    def learn(self, state, action, reward):
        if self.learning == True:
            self.Q[state][str(action)] += self.alpha * (reward - self.Q[state][str(action)])
        return None


    def createQ(self, state, validbids):
        if not state in self.Q:
            self.Q[state] = {}
            for action in validbids:
                self.Q[state][str(action)] = 0
        return


    def chooseaction(self, phase, state, filteredbidspace):
        if phase == "training" or \
        (phase == "mixing" and random.uniform(0, 1) < self.epsilon):
            bid = random.choice(filteredbidspace)
        else:
            maxval = max(self.Q[state].values())
            bid = float(random.choice([key for key, val in self.Q[state].items() if val == maxval]))
        return bid


    def writeQtable(self):
        f = self.tblfile
        f.write("/-----------------------------------------\n")
        f.write("| State-action rewards from Q-Learning\n")
        f.write("\-----------------------------------------\n\n")

        for state in self.Q:
            f.write("{}\n".format(state))
            for action, reward in sorted(self.Q[state].items()):
                f.write(" -- {} : {:.2f}\n".format(action, reward))
            f.write("\n")
        f.close()


    def writeQlog(self, runtotal, phase):
        for state in self.Q:
            self.Qlogwriter.writerow(dict({"runtotal": runtotal,
                                           "phase": phase},
                                           **self.Q[state]))
        return None


    def Qconv(self, window, sig = 0.05, step = 1000):
        """
        This functions cheks if Q-database has converged.
        In: window (defines how far back the program should look)
        Out: boolean
        """
        Qlogdata = pd.read_csv(self.Qlogname,
                                 skip_blank_lines = False,
                                 index_col = 0,
                                 header = 0,
                                 skiprows = lambda x: np.fmod(x, step) != 0)
        Qlogdata = Qlogdata.tail(int( window / step ))
        Qlogdata.drop(["phase"], axis = 1, inplace = True)
        Qconvdict = {}
        Qconv = False
        if self.name == "bidder1":
            plot = Qlogdata.plot(kind = 'line')
            plt.show()
        for name, series in Qlogdata.items():
            adf = adfuller(x = series.values,
                           maxlag=0,
                           regression='nc',
                           autolag=None,
                           store=False,
                           regresults=False)
            print("p-value: ", adf[1])
            # print("sig level: ", sig)
            Qconvdict[name] = adf[1]
        nunconv = 0
        for action, pvalue in Qconvdict.items():
            # print("looping through")
            # print(pvalue >= sig)
            if pvalue >= sig:
                nunconv += 1
        if nunconv == 0:
            Qconv = True
        # print(nunconv)
        # print(Qconv)
        return Qconv


    def valdraw(self):
        valgood = random.choice(self.valspace)
        return valgood


    def rewardfunc(self, ngood, price, valgood):
        reward = ngood * (valgood - price)
        return reward


    def updatehistory(self, state, bid):
        entry = ("bid: ", bid)
        self.history.append(entry)
        return None
