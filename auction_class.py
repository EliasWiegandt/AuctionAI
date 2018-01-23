# Create auction class
import numpy as np
from scipy.stats import rankdata

class Auction:
    def __init__(self):
        self.a_min_price = 50
        self.n_ablocks = 1
        self.ablocks_size = 10

        self.b_min_price = 25
        self.bblocks_number = 7
        self.bblocks_size = 5

        self.C1_min_price = 0
        self.C2_min_price = 0
        self.C3_min_price = 0

    def r1(self, bool_abids, b_ablocks):
        """
        Runs the first round of the auction, the allotment of A-blocks
        Input: list of boolean indicator of bid, list of A-block bids
        Output: list of awarded blocks, list of prices
        """
        n_ablocks = [None] * len(bool_abids)
        p_ablocks = []
        p_ablock = None

        if sum(bool_abids) > self.n_ablocks: # More bidders than blocks
            # Find price of auction
            ordered_indices = list(range(len(b_ablocks)))
            ordered_bids = sorted(ordered_indices, key=lambda k: b_ablocks[k], reverse=True)
            p_ablock = b_ablocks[ordered_bids[self.n_ablocks]]

            ranks = rankdata(b_ablocks, method='max') - 1
            ranks = np.ones_like(ranks)*(len(ranks)-1) - ranks

            # Check if a random choice is needed between bidders
            in_auction = sum(ranks < self.n_ablocks)
            random_choice_needed = False
            if in_auction > self.n_ablocks:
                random_choice_needed = True
                rank_at_risk = max(ranks[ranks < self.n_ablocks])
                bidders_to_kick = in_auction - self.n_ablocks
                rank_at_risk_number = sum(ranks == rank_at_risk)
                kick_space = np.arange(start = 1,
                                       stop = rank_at_risk_number + 1,
                                       step = 1)
                kick_numbers = np.random.choice(kick_space,
                                                size=bidders_to_kick,
                                                replace=False,
                                                p=None)

            # Determine who gets blocks
            kick_counter = 1
            for index, rank in enumerate(ranks):
                if random_choice_needed:
                    if rank < rank_at_risk:
                        n_ablocks[index] = True
                    elif rank == rank_at_risk:
                        if not(kick_counter in kick_numbers):
                            n_ablocks[index] = True
                            kick_counter += 1
                        else:
                            n_ablocks[index] = False
                            kick_counter += 1
                    else:
                        n_ablocks[index] = False
                else:
                    n_ablocks[index] = rank < self.n_ablocks

            # Write array with prices
            for n in n_ablocks:
                if n:
                    p_ablocks.append(p_ablock)
                else:
                    p_ablocks.append(n)

        else: # This is activated when there are more or equal blocks than bidders
            n_ablocks = bool_abids
            for n in n_ablocks:
                if n:
                    p_ablocks.append(self.a_min_price)
                    p_ablock=self.a_min_price
                else:
                    p_ablocks.append(n)

        return n_ablocks, p_ablocks, p_ablock


    def round_two(self):
        str_desc = "Allotment of cover duty."
        return str_desc

    def round_three(self):
        str_desc = "Allotment of B-blocks."
        return str_desc

    def auction_result(self):
        str_desc = "Allotment of A-blocks."
        return str_desc
