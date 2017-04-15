# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from crawler.espn_crawler.data_crawler import EspnCrawler


class NumberOfPitch:
    def __init__(self, interval):
        self.interval = interval
        self.crawler = EspnCrawler(self.interval)
        self.game_list = None
        self.mined_data = dict()

    def _data_preparation(self):
        # FIXME: what if interval is too big to fit in memory?
        self.game_list = self.crawler.run(game_type="pitch-by-pitch")

    def _data_miner(self):
        for one_game in self.game_list:
            for one_inning in one_game:
                for one_at_bat in one_inning:
                    number_of_pitches = self._pitch_counter(one_at_bat[1])
                    result = self._result_parser(one_at_bat[1])
                    if number_of_pitches in self.mined_data:
                        if result in self.mined_data[number_of_pitches]:
                            self.mined_data[number_of_pitches][result] += 1
                        else:
                            self.mined_data[number_of_pitches] = 1
                    else:
                        self.mined_data[number_of_pitches] = dict(result=1)

    def _pitch_counter(self, one_batter):
        return

    def _result_parser(self, one_batter):
        return

    def _covariance(self, number_of_pitches, results):
        """
        
        :param number_of_pitches: 
        :param results: should contain (all raw result and average, obp, and slg)
        :return: 
        """
        pass


if __name__ == '__main__':
    pass
