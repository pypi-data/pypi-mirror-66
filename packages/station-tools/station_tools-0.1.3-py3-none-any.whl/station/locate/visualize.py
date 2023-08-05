import pandas as pd
import matplotlib.pyplot as plt
from . import nodedataset

class Visualize:
    def __init__(self, pickle_filename):
        print('loading data')
        self.df = pd.read_pickle(pickle_filename)
        print('done')
        self.figsize = (20,20)
        self.channels = self.df.RadioId.unique()

    def chart_hist(self, freq, filename):
        fig = plt.figure(figsize=(self.figsize))
        for n, channel in enumerate(self.channels):
            n += 1
            dataset = self.df[self.df.RadioId==channel]
            rs = dataset.resample(freq)
            #nodes = rs.NodeId.nunique()
            beeps = rs.TagId.count()

            ax = fig.add_subplot(len(self.channels), 1, n)
            ax.set_title('Channel {}'.format(channel))
            ax.bar(beeps.index, beeps, width=0.01)
            ax.grid()
        fig.savefig(filename)
    
    def node_hists(self, freq):
        for node_id in self.df.NodeId.unique():
            fig = plt.figure(figsize=(self.figsize))
            fig.suptitle('Node {}'.format(node_id))
            for n, channel in enumerate(self.channels):
                dataset = self.df[(self.df.NodeId==node_id) & (self.df.RadioId==channel)]
                count_data = dataset.resample(freq).TagId.count()
                n += 1
                ax = fig.add_subplot(len(self.channels), 1, n)
                ax.set_title('Channel {}'.format(channel))
                ax.bar(count_data.index, count_data, width=0.03)
                ax.grid()
            filename = 'node_{}_info.png'.format(node_id)
            print('saving file', filename)
            fig.savefig(filename)
