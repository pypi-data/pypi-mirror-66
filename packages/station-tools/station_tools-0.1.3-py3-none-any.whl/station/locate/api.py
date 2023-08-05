import logging
import utm
import pandas as pd
import math

from . import nodedataset

class LocationApi:
    """utility for localizing tags in merged beep/node dataset"""
    def __init__(self, beep_filename, node_filename, max_nodes=None):
        """filenames of raw beep data and node location data"""
        self.nodedata = nodedataset.NodeDataset(beep_filename, node_filename) 
        # ez reference
        self.merged_df = self.nodedata.df

        # assume utm zone, letter from first record
        self.zone = self.merged_df.iloc[0].zone
        self.letter = self.merged_df.iloc[0].letter

        #self.MAX_NODES = 8
        self.MAX_NODES = max_nodes
        self.alpha = 1
        self.MAX_RSSI = -40
        self.DEFAULT_PATH_LOSS_COEFFICIENT = 5  

        self.buffer = []

    def get_top_tag_count(self, n_tags):
        # get the top tag ids by beep count from the full dataset
        tags = self.merged_df.groupby('TagId').RadioId.count().sort_values(ascending=False)
        if n_tags is not None:
            tags = tags[0:n_tags]
        return tags.index

    def get_path_loss_coefficient(self, records):
        # later fill this with better way to get coefficient
        return self.DEFAULT_PATH_LOSS_COEFFICIENT

    def get_radius_from_rssi(self, rssi, path_loss_coefficient):
        delta_rssi = 0-(self.MAX_RSSI + rssi)
        exponent = delta_rssi / (10*path_loss_coefficient)
        radius = self.alpha * math.pow(10, exponent)
        return radius

    def custom_agg(self, records):
        """custom aggregation function for resampled period"""
        info = {
            'nodes': [],
            'avg_x': 0,
            'avg_y': 0
        }

        # check to make sure there is at least 1 record
        if records.shape[0] > 0:
            grouped_nodes = records.groupby('NodeId')
            # get description stats for each column - max, min, mean, count, 25,50,75
            nodes_df = grouped_nodes.describe()

            path_loss_coefficient = self.get_path_loss_coefficient(records)
            if self.MAX_NODES is not None:
                top_nodes = nodes_df.sort_values(('TagRSSI','max'), ascending=False).iloc[0:self.MAX_NODES]
            else:
                top_nodes = nodes_df.sort_values(('TagRSSI','max'), ascending=False)


            total = 0
            for node_id, row in top_nodes.iterrows():
                max_rssi = row.TagRSSI['max']
                radius = self.get_radius_from_rssi(max_rssi, path_loss_coefficient)
                beep_count = row.TagRSSI['count']
                info['avg_x'] = row.node_x['max'] * beep_count
                info['avg_y'] = row.node_y['max'] * beep_count
                total += beep_count
                info['nodes'].append({
                    'max_rssi': max_rssi,
                    'min_rssi': row.TagRSSI['min'],
                    'std_rssi': row.TagRSSI['std'],
                    'count': beep_count,
                    'radius': radius,
                    'node_id': node_id
                })
            if total != 0:
                info['avg_x'] = info['avg_x'] / total
                info['avg_y'] = info['avg_y'] / total

        self.buffer.append(info)
        return 0

    def advanced_resampled_stats(self, freq, tag_id, channel):
        """generate weighted average location dataset for given channel, tag_id and frequency
        return a dataframe
        """
        self.buffer = []
        filtered_df = self.merged_df[self.merged_df.TagId==tag_id]
        filtered_df = filtered_df[filtered_df.RadioId==channel]

        # resample to given frequency
        rs = filtered_df.resample(freq)
        resampled_custom_mean_dataframe = rs.apply(self.custom_agg)
        for i, record in enumerate(self.buffer):
            record['date'] = resampled_custom_mean_dataframe.index[i].strftime('%Y-%m-%dT%H:%M:%S')
        return self.buffer

    def weighted_average(self, freq, tag_id, channel):
        """generate weighted average location dataset for given channel, tag_id and frequency
        return a dataframe
        """
        filtered_df = self.merged_df[self.merged_df.TagId==tag_id]
        filtered_df = filtered_df[filtered_df.RadioId==channel]

        # resample to given frequency
        rs = filtered_df.resample(freq)
        mean_df = rs.mean()
        nunique_df = rs.nunique()
        count_df = rs.count()

        lats = []
        lngs = []
        for i, record in mean_df.iterrows():
            try:
                lat,lng = utm.to_latlon(record.node_x, record.node_y, self.zone, self.letter)
                lats.append(lat)
                lngs.append(lng)
            except:
                lats.append(None)
                lngs.append(None)

        out_df = pd.DataFrame({
            'lat': lats,
            'lng': lngs,
            'easting': mean_df.node_x,
            'northing': mean_df.node_y,
            'count': count_df.TagRSSI,
            'unique_nodex': nunique_df.NodeId,
        }, index=mean_df.index)

        # mean x,y from weighted node_x, node_y dataframe
        return out_df
