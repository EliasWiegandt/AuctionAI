import os
import csv

class auction_log():
    def __init__(self):
        self.run_log_filename = os.path.join("logs", "auction_run_log" + ".csv")
        self.run_log_fields = ['run_number',
                           'name',
                           'phase',
                           'v_ablock',
                           'b_ablock',
                           'n_ablock',
                           'p_ablock',
                           'reward']
        self.run_log_file = open(self.run_log_filename, 'w', newline='')
        self.run_log_writer = csv.DictWriter(self.run_log_file, fieldnames=self.run_log_fields)
        self.run_log_writer.writeheader()

        return None


    def write_run_log(self, bidders, run, phase, n_ablocks, p_ablocks, p_ablock):
        for ix, bidder in enumerate(bidders):
            self.run_log_writer.writerow({
                'run_number': run,
                'name': bidder.name,
                'phase': phase,
                'v_ablock': bidder.v_ablock,
                'b_ablock': bidder.b_ablock,
                'n_ablock': n_ablocks[ix],
                'p_ablock': p_ablock,
                'reward': bidder.reward})

        return None
