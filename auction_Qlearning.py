import auction_class as ac
import bidder_class as bc
import os
import numpy as np
import random
import auction_ai_visualizations as av
import log_class as lc
import matplotlib.pyplot as plt
import timeit
np.random.seed(10)
random.seed(a=10)

training_simulations = 5000
convergence_window = 100000
QConvStep = int(convergence_window / 50)
check_convergence = True
mixed_simulations = 0
test_simulations = 0

SigLev = 0.01
alpha = 0.0001
print_trials = False
visualizeQ = True
v_mid_ablock = 100
a_min_price = 0
n_ablocks = 4
n_actions = 2
actions_intervals = 5
n_values = 4
values_intervals = 0.5
write_logs = True
run = True
global_value = False
# possible_values = range(v_mid_ablock - actions_intervals * n_actions,
#                         v_mid_ablock + actions_intervals * (n_actions + 1),
#                         actions_intervals)

# Set path for working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Start timing
time_start = timeit.default_timer()

# Create bidders
bidder_1 = bc.Bidder(fixed_bid = False,
                     fixed_value = True,
                     v_mid_ablock = v_mid_ablock,
                     b_ablock = 60,
                     name = "bidder1",
                     learning = True,
                     alpha = alpha,
                     n_actions = n_actions,
                     actions_intervals = actions_intervals,
                     n_values = n_values,
                     values_intervals = values_intervals
                     )

bidder_2 = bc.Bidder(fixed_bid = False,
                     fixed_value = True,
                     v_mid_ablock = v_mid_ablock,
                     b_ablock = 60,
                     name = "bidder2",
                     learning = True,
                     alpha = alpha,
                     n_actions = n_actions,
                     actions_intervals = actions_intervals,
                     n_values = n_values,
                     values_intervals = values_intervals
                     )

bidder_3 = bc.Bidder(fixed_bid = False,
                     fixed_value = True,
                     v_mid_ablock = v_mid_ablock,
                     b_ablock = 60,
                     name = "bidder3",
                     learning = True,
                     alpha = alpha,
                     n_actions = n_actions,
                     actions_intervals = actions_intervals,
                     n_values = n_values,
                     values_intervals = values_intervals
                     )

bidder_4 = bc.Bidder(fixed_bid = False,
                     fixed_value = True,
                     v_mid_ablock = v_mid_ablock,
                     b_ablock = 60,
                     name = "bidder4",
                     learning = True,
                     alpha = alpha,
                     n_actions = n_actions,
                     actions_intervals = actions_intervals,
                     n_values = n_values,
                     values_intervals = values_intervals
                     )

bidder_5 = bc.Bidder(fixed_bid = False,
                     fixed_value = True,
                     v_mid_ablock = v_mid_ablock,
                     b_ablock = v_mid_ablock,
                     name = "bidder5",
                     learning = True,
                     alpha = alpha,
                     n_actions = n_actions,
                     actions_intervals = actions_intervals,
                     n_values = n_values,
                     values_intervals = values_intervals
                     )

bidders = [bidder_1, bidder_2, bidder_3, bidder_4, bidder_5]
# bidders = [bidder_1, bidder_2, bidder_3, bidder_4]
# bidders = [bidder_1, bidder_2, bidder_3]
n_bidders = len(bidders)

# Set auction up
SpectrumAuction = ac.Auction()
SpectrumAuction.a_min_price = a_min_price
SpectrumAuction.n_ablocks = n_ablocks

# Create auction_log
log = lc.auction_log()

time_setup_complete = timeit.default_timer()

def r1_run(bidders, run):
    bool_abids = []
    b_ablocks = []
    for bidder in bidders:
        state = bidder.build_state()
        bidder.createQ(state)
        bidder.b_ablock = bidder.choose_action(state)
        bool_abid = bidder.b_ablock >= SpectrumAuction.a_min_price
        bool_abids.append(bool_abid)
        if bool_abid:
            b_ablocks.append(bidder.b_ablock)
        else: b_ablocks.append(0)
    n_ablocks, p_ablocks, p_ablock = SpectrumAuction.r1(bool_abids, b_ablocks)

    return b_ablocks, n_ablocks, p_ablocks, p_ablock


def learning_phase(bidders, n_ablocks, p_ablocks, p_ablock):
    if global_value:
        v_ablock_global = np.random.uniform(low = v_mid_ablock - actions_intervals * n_actions,
                                          high = v_mid_ablock + actions_intervals * (n_actions + 1),
                                          size = None)
    for index, bidder in enumerate(bidders):
        if n_ablocks[index]:
            if not(bidder.fixed_value):
                bidder.draw_value()
            if global_value:
                bidder.v_ablock = v_ablock_global
            bidder.reward = bidder.v_ablock - p_ablocks[index]
        else:
            bidder.reward = 0
        bidder.learn(bidder.state, bidder.b_ablock, bidder.reward)

    return None


def run(bidders, trainruns, mixedruns, testruns):
    max_runs = [trainruns, mixedruns, testruns]
    phases = ["Training", "Mixing", "Testing"]

    for phase, max_run in enumerate(max_runs):
        run = 0
        if phase == 0:
            training = True
            mixing = False
            testing = False
            training_converged = False
        elif phase == 1:
            training = False
            mixing = True
            testing = False
            training_converged = False
        elif phase == 2:
            training = False
            mixing = False
            testing = True
            training_converged = False
        else:
            print("Problems with phases!")

        while run < max_run and training_converged == False:
            # Run round 1
            b_ablocks, n_ablocks, p_ablocks, p_ablock = r1_run(bidders, run)

            # Learning phase
            learning_phase(bidders, n_ablocks, p_ablocks, p_ablock)

            # Reset bidders' parameters
            for bidder in bidders:
                bidder.reset(testing = testing, mixing = mixing)

            # Write logs
            if write_logs:
                log.write_run_log(bidders, run, phases[phase], n_ablocks, p_ablocks, p_ablock)
                for bidder in bidders:
                    bidder.write_Q_log(run)

            # Finish training, if converged
            if training == True and check_convergence == True:
                if np.fmod(run + 1, convergence_window) == 0:
                    print("About to ADF")
                    time_start_adf = timeit.default_timer()
                    unconverged = 0
                    for bidder in bidders:
                        booQconv, dictQconv = bidder.Q_conv(convergence_window,
                                                            significance_level = SigLev,
                                                            step = QConvStep)
                        if booQconv == False:
                            unconverged += 1
                    if unconverged == 0:
                        training_converged = True
                        print("Value of strategies have converged.")
                    else:
                        print(unconverged, " bidders still needs to converge.")
                    time_complete_adf = timeit.default_timer()
                    time_adf = time_complete_adf - time_start_adf
                    print("Time spent on ADF: ", time_adf, " seconds")

            # Print results
            if print_trials:
                print("Trial ", run)
                print("A-block bids: ", str(b_ablocks))
                print(" A-block awarded: ", str(n_ablocks))
                print("A-block price: ", str(p_ablock))
                rewards = []
                v_ablocks = []
                for bidder in bidders:
                    rewards.append(bidder.reward)
                    v_ablocks.append(bidder.v_ablock)
                print("Values of A-block:")
                print(v_ablocks)
                print("Rewards:")
                print(rewards)
                print("")

            # Increment run
            run += 1

    # Write the Q tables to a file, close other logs
    log.run_log_file.close()
    for bidder in bidders:
        bidder.write_Qtable()
        bidder.Q_log_file.close()
    return None

if run:
    run(bidders, training_simulations, mixed_simulations, test_simulations)

time_runs_complete = timeit.default_timer()

print("Total run time: ", time_runs_complete - time_start)

if visualizeQ:
    plt1 = av.visualizeQ(bidders,
                         SpectrumAuction,
                         training_simulations,
                         test_simulations,
                         alpha)
    plt2 = av.visualize_Convergence(bidders)
    # plt3 = av.visualize_prop_reward(log.run_log_filename, bidders)
    # plt4 = av.visualize_rewards(log.run_log_filename, bidders)
    # plt5 = av.visualize_rewards_violin(log.run_log_filename, bidders)
    # plt6 = av.visualize_uncertain_rewards(log.run_log_filename, bidders)
    
    plt1.show()
    plt2.show()
    # plt3.show()
    # plt4.show()
    # plt5.show()
    # plt6.show()

time_complete = timeit.default_timer()
