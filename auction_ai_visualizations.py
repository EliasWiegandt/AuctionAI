import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
import os
# sns.set(style="whitegrid", palette="pastel", color_codes=True)

def visQ(bidders, auction, runtotal):
    nbidders = len(bidders)
    fig, ax = plt.subplots()
    specs = (str(nbidders),
                  str(auction.ngoods),
                  str(runtotal))
    title = "Bidders: %s, goods: %s, simulations: %s." % specs
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)

    for ix, bidder in enumerate(bidders):
        x = []
        y = []
        for state in bidder.Q:
            for action, reward in sorted(bidder.Q[state].items()):
                action = float(action)
                x.append(action)
                y.append(reward)
        plt.subplot(1, nbidders, ix+1, sharex=ax1, sharey=ax1)
        width = (max(bidder.bidspace)-min(bidder.bidspace))/(len(bidder.bidspace))
        bars = plt.bar(x, y, width = width, edgecolor='black')
        # midbar = math.floor(len(bars)/2)
        # bars[midbar].set_color('black')
        plt.title(bidder.name)

    plt.savefig(os.path.join("charts", 'Qfinal.png'), bbox_inches='tight')
    plt.draw()
    return plt


def visconv(bidders):
    nbidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Q developments"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    for ix, bidder in enumerate(bidders):
        Qlogdata = pd.read_csv(bidder.Qlogname,
                                 index_col = 0,
                                 header = 0,
                                 skip_blank_lines = False)

        # Find first instance of new phase
        phases = Qlogdata["phase"].unique()
        ixfirsts = []
        for phase in phases:
            ixfirst = Qlogdata["phase"].eq(phase).idxmax()
            ixfirsts.append(ixfirst)
        Qlogdata.drop(["phase"], axis = 1, inplace = True)
        plt.subplot(1, nbidders, ix+1, sharex = ax1, sharey = ax1)
        plt.plot(Qlogdata)
        plt.legend(list(Qlogdata), loc='best')
        plt.title(bidder.name)
        for ixfirstphase in ixfirsts:
            plt.axvline(x=ixfirstphase)
    plt.savefig(os.path.join("charts", 'Qconv.png'), bbox_inches='tight')
    plt.draw()
    return plt

def vispropreward(runlogname, bidders):
    nbidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Q breakdown"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    chartrow2 = str(nbidders) + '11'
    ax2 = plt.subplot(int(chartrow2))
    logdata = pd.read_csv(runlogname, skip_blank_lines=False)
    for ix, bidder in enumerate(bidders):
        bidderdata = logdata.where(logdata.name == bidder.name).dropna(axis=0, how='any')
        biddergrouped = bidderdata[['bid', 'ngood', 'reward']].groupby(by = "bid", as_index=False).mean().rename(index=str, columns={"ngood": "proprice"})
        rewardgrouped = bidderdata[['bid', 'price', 'reward']].where(bidderdata.ngood == True).groupby(by = "bid", as_index=False).mean().rename(index=str, columns={"reward": "reward_given_win"})
        biddergrouped = pd.merge(biddergrouped, rewardgrouped, on=['bid'], how='outer')

        x = biddergrouped['bid']
        y = biddergrouped['proprice']
        plt.subplot(2, nbidders, ix+1, sharex=ax1, sharey=ax1)
        width = (max(bidder.bidspace)-min(bidder.bidspace))/(len(bidder.bidspace))
        bars = plt.bar(x, y, width=width, edgecolor='black')
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)

        x = biddergrouped['bid']
        y = biddergrouped['reward_given_win']
        plt.subplot(2, nbidders, ix+1+nbidders, sharex=ax2, sharey=ax2)
        width = (max(bidder.bidspace)-min(bidder.bidspace))/(len(bidder.bidspace))
        bars = plt.bar(x, y, width = width, edgecolor='black')
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)
    plt.savefig(os.path.join("charts", 'prop_dev.png'), bbox_inches='tight')
    plt.draw()
    return plt

def visrewards(run_log_filename, bidders):
    nbidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Reward breakdown by mean and sem"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    logdata = pd.read_csv(run_log_filename, skip_blank_lines=False)
    for ix, bidder in enumerate(bidders):
        bidderdata = logdata.where(logdata.name == bidder.name).dropna(axis=0, how='any')
        bidderdata['reward_std']=bidderdata['reward']
        bidderdata['reward_n']=bidderdata['reward']
        biddergrouped = bidderdata[['bid', 'reward', 'reward_std', 'reward_n']].groupby(by = "bid", as_index=False).agg({'reward': np.mean, 'reward_std': np.std, 'reward_n': 'count'})
        biddergrouped['reward_sem'] =  biddergrouped['reward_std'] / np.sqrt(biddergrouped['reward_n'])
        x = biddergrouped['bid']
        y = biddergrouped['reward']
        sey = biddergrouped['reward_sem']*1.96
        plt.subplot(1, nbidders, ix+1, sharex=ax1, sharey=ax1)
        width = (max(bidder.bidspace) - min(bidder.bidspace)) / (len(bidder.bidspace))
        bars = plt.bar(x, y, yerr=sey, width = width, edgecolor='black', ecolor='red',)
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)
        quantiles=bidderdata['reward'].quantile([0.025, 0.975])
    plt.savefig(os.path.join("charts", 'rew_est.png'), bbox_inches='tight')
    plt.draw()
    return plt

def visuncertainrewards(run_log_filename, bidders):
    logdata = pd.read_csv(run_log_filename, skip_blank_lines=False)
    bidder = bidders[0]

    bidderdata = logdata.where(logdata.name == bidder.name).dropna(axis=0, how='any')
    bidderdata['reward_std']=bidderdata['reward']
    bidderdata['reward_n']=bidderdata['reward']
    univals = sorted(bidder.valspace)
    columns = 5.0
    rows = math.ceil(len(univals)/columns)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(111)
    title = bidder.name + ": reward given value of good"
    fig.suptitle(title, fontsize=12)

    for ix, value in enumerate(univals):
        plt.subplot(rows, columns, ix+1, sharex=ax1, sharey=ax1)
        bidderval = bidderdata[['valgood', 'bid', 'reward', 'reward_std', 'reward_n']].where(bidderdata['valgood'] == value).dropna(axis=0, how='any')
        biddergrouped = bidderval[['valgood', 'bid', 'reward', 'reward_std', 'reward_n']].groupby(by = ["bid"], as_index=False).agg({'valgood': np.mean, 'reward': np.mean, 'reward_std': np.std, 'reward_n': 'count'})
        biddergrouped['reward_sem'] =  biddergrouped['reward_std'] / np.sqrt(biddergrouped['reward_n'])
        x = biddergrouped['bid']
        y = biddergrouped['reward']
        sey = biddergrouped['reward_sem']*1.96
        width = (max(bidder.bidspace) - min(bidder.bidspace)) / (len(bidder.bidspace))
        bars = plt.bar(x, y, yerr=sey, width = width, edgecolor='black', ecolor='red',)
        plt.title("value of good: " + str(value))
    plt.savefig(os.path.join("charts", 'state_rew_est.png'), bbox_inches='tight')
    plt.show()
    return plt

def visualize_rewards_violin_by_bidder(run_log_filename, bidders):
    nbidders = len(bidders)
    fig, axes = plt.subplots(1, nbidders)
    title = "Reward distribution"
    fig.suptitle(title, fontsize=12)
    logdata = pd.read_csv(run_log_filename, skip_blank_lines=False)
    for ix, bidder in enumerate(bidders):
        bidderdata = logdata.where(logdata.name == bidder.name).dropna(axis=0, how='any')
        ax = sns.violinplot(x="bid",
                       y="reward",
                       data=bidderdata,
                       ax = axes[ix])
    plt.savefig(os.path.join("charts", 'rew_bybidder_violin.png'), bbox_inches='tight')
    plt.draw()
    return plt

def visviolin(logpath):
    fig, axes = plt.subplots(1, 1)
    title = "Reward distribution"
    fig.suptitle(title, fontsize=12)
    logdata = pd.read_csv(logpath, skip_blank_lines=False)
    ax = sns.violinplot(x="bid",
                   y="reward",
                   data=logdata,
                   inner="box",
                   )
    plt.savefig(os.path.join("charts", 'rew_violin.png'), bbox_inches='tight')
    plt.draw()
    return plt
