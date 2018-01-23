import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import seaborn as sns
import os
# sns.set(style="whitegrid", palette="pastel", color_codes=True)

def visualizeQ(bidders,
               auction,
               training_simulations,
               test_simulations,
               alpha
               ):
    n_bidders = len(bidders)
    fig, ax = plt.subplots()
    specs_list = (str(n_bidders),
                  str(auction.n_ablocks),
                  str(training_simulations+ test_simulations),
                  str(alpha))
    title = "Bidders: %s, ablocks: %s, simulations: %s, alpha: %s"% specs_list
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)

    for index, bidder in enumerate(bidders):
        x = []
        y = []
        for state in bidder.Q:
            for action, reward in sorted(bidder.Q[state].items()):
                action = int(action)
                x.append(action)
                y.append(reward)
        plt.subplot(1, n_bidders, index+1, sharex=ax1, sharey=ax1)
        bars = plt.bar(x, y, width=bidder.actions_intervals, edgecolor='black')
        mid_bar = math.floor(len(bars)/2)
        mid_bar = 1
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)

    plt.savefig(os.path.join("charts", 'Q_final.png'))
    plt.draw()

    return plt

def visualize_Convergence(bidders):
    n_bidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Q developments"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    for index, bidder in enumerate(bidders):
        # Q_log_data = pd.read_csv(bidder.Q_log_filename, skip_blank_lines=False)
        Q_log_data = pd.read_csv(bidder.Q_log_filename, index_col=0)
        plt.subplot(1, n_bidders, index+1, sharex=ax1, sharey=ax1)
        plot = plt.plot(Q_log_data)
        plt.title(bidder.name)
    # filename = os.path.join("charts", )
    plt.savefig(os.path.join("charts", 'Q_convergence.png'))
    plt.draw()
    return plt

def visualize_prop_reward(run_log_filename, bidders):
    print("In prop")
    n_bidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Q breakdown"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    chart_row_2 = str(n_bidders) + '11'
    ax2 = plt.subplot(int(chart_row_2))
    log_data = pd.read_csv(run_log_filename, skip_blank_lines=False)
    for index, bidder in enumerate(bidders):
        bidder_data = log_data.where(log_data.name == bidder.name).dropna(axis=0, how='any')
        bidder_grouped = bidder_data[['b_ablock', 'n_ablock', 'reward']].groupby(by = "b_ablock", as_index=False).mean().rename(index=str, columns={"n_ablock": "prop_ablock"})
        reward_grouped = bidder_data[['b_ablock', 'p_ablock', 'reward']].where(bidder_data.n_ablock == True).groupby(by = "b_ablock", as_index=False).mean().rename(index=str, columns={"reward": "reward_given_win"})
        bidder_grouped = pd.merge(bidder_grouped, reward_grouped, on=['b_ablock'], how='outer')

        x = bidder_grouped['b_ablock']
        y = bidder_grouped['prop_ablock']
        plt.subplot(2, n_bidders, index+1, sharex=ax1, sharey=ax1)
        bars = plt.bar(x, y, width=bidder.actions_intervals, edgecolor='black')
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)

        x = bidder_grouped['b_ablock']
        y = bidder_grouped['reward_given_win']
        plt.subplot(2, n_bidders, index+1+n_bidders, sharex=ax2, sharey=ax2)
        bars = plt.bar(x, y, width=bidder.actions_intervals, edgecolor='black')
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)
    plt.savefig(os.path.join("charts", 'prop_dev.png'))
    plt.draw()
    return plt

def visualize_rewards(run_log_filename, bidders):
    n_bidders = len(bidders)
    fig, ax = plt.subplots()
    title = "Reward breakdown by mean and sem"
    fig.suptitle(title, fontsize=12)
    ax1 = plt.subplot(111)
    chart_row_2 = str(n_bidders) + '11'
    ax2 = plt.subplot(int(chart_row_2))
    log_data = pd.read_csv(run_log_filename, skip_blank_lines=False)
    for index, bidder in enumerate(bidders):
        bidder_data = log_data.where(log_data.name == bidder.name).dropna(axis=0, how='any')
        bidder_data['reward_std']=bidder_data['reward']
        bidder_data['reward_n']=bidder_data['reward']
        bidder_grouped = bidder_data[['b_ablock', 'reward', 'reward_std', 'reward_n']].groupby(by = "b_ablock", as_index=False).agg({'reward': np.mean, 'reward_std': np.std, 'reward_n': 'count'})
        bidder_grouped['reward_sem'] =  bidder_grouped['reward_std'] / np.sqrt(bidder_grouped['reward_n'])
        x = bidder_grouped['b_ablock']
        y = bidder_grouped['reward']
        ste_y = bidder_grouped['reward_sem']*1.96
        # ste_y = bidder_grouped['reward_std']
        plt.subplot(1, n_bidders, index+1, sharex=ax1, sharey=ax1)
        bars = plt.bar(x, y, yerr=ste_y, width=bidder.actions_intervals, edgecolor='black', ecolor='red',)
        mid_bar = math.floor(len(bars)/2)
        bars[mid_bar].set_color('black')
        plt.title(bidder.name)
        quantiles=bidder_data['reward'].quantile([0.025, 0.975])
    plt.savefig(os.path.join("charts", 'rew_est.png'))
    plt.draw()
    return plt

def visualize_uncertain_rewards(run_log_filename, bidders):
    log_data = pd.read_csv(run_log_filename, skip_blank_lines=False)
    bidder = bidders[0]

    bidder_data = log_data.where(log_data.name == bidder.name).dropna(axis=0, how='any')
    bidder_data['reward_std']=bidder_data['reward']
    bidder_data['reward_n']=bidder_data['reward']
    unique_v_ablocks = sorted(bidder_data["v_ablock"].unique())
    columns = 5.0
    rows = math.ceil(len(unique_v_ablocks)/columns)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(111)
    title = bidder.name + ": reward given v_ablock"
    fig.suptitle(title, fontsize=12)

    for index, v_ablock in enumerate(unique_v_ablocks):
        # row = math.ceil((index+1)/columns)
        # column = math.fmod(index, columns)+1
        plt.subplot(rows, columns, index+1, sharex=ax1, sharey=ax1)
        bidder_v_ablock = bidder_data[['v_ablock', 'b_ablock', 'reward', 'reward_std', 'reward_n']].where(bidder_data['v_ablock'] == v_ablock).dropna(axis=0, how='any')
        bidder_grouped = bidder_v_ablock[['v_ablock', 'b_ablock', 'reward', 'reward_std', 'reward_n']].groupby(by = ["b_ablock"], as_index=False).agg({'v_ablock': np.mean, 'reward': np.mean, 'reward_std': np.std, 'reward_n': 'count'})
        bidder_grouped['reward_sem'] =  bidder_grouped['reward_std'] / np.sqrt(bidder_grouped['reward_n'])
        x = bidder_grouped['b_ablock']
        y = bidder_grouped['reward']
        ste_y = bidder_grouped['reward_sem']*1.96
        bars = plt.bar(x, y, yerr=ste_y, width=bidder.actions_intervals, edgecolor='black', ecolor='red',)
        plt.title("v_ablock: " + str(v_ablock))
    plt.savefig(os.path.join("charts", 'state_rew_est.png'))
    plt.show()
    return plt

def visualize_rewards_violin_by_bidder(run_log_filename, bidders):
    print("In violin")
    n_bidders = len(bidders)
    fig, axes = plt.subplots(1, n_bidders)
    title = "Reward distribution"
    fig.suptitle(title, fontsize=12)
    log_data = pd.read_csv(run_log_filename, skip_blank_lines=False)
    for ix, bidder in enumerate(bidders):
        bidder_data = log_data.where(log_data.name == bidder.name).dropna(axis=0, how='any')
        ax = sns.violinplot(x="b_ablock",
                       y="reward",
                       data=bidder_data,
                       ax = axes[ix])
    plt.savefig(os.path.join("charts", 'rew_bybidder_violin.png'))
    plt.draw()
    return plt

def visualize_rewards_violin(run_log_filename, bidders):
    print("In violin")
    n_bidders = len(bidders)
    fig, axes = plt.subplots(1, 1)
    title = "Reward distribution"
    fig.suptitle(title, fontsize=12)
    log_data = pd.read_csv(run_log_filename, skip_blank_lines=False)
    ax = sns.violinplot(x="b_ablock",
                   y="reward",
                   data=log_data,
                   inner="box",
                   )
    plt.savefig(os.path.join("charts", 'rew_violin.png'))
    plt.draw()
    return plt
