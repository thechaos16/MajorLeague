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
                    number_of_pitches, result = self._pitch_counter_and_result(one_at_bat[1])
                    # reliever in the beginning of an inning
                    if number_of_pitches == 0:
                        continue
                    if number_of_pitches in self.mined_data:
                        if result in self.mined_data[number_of_pitches]:
                            self.mined_data[number_of_pitches][result] += 1
                        else:
                            self.mined_data[number_of_pitches][result] = 1
                    else:
                        self.mined_data[number_of_pitches] = {result: 1}

    @staticmethod
    def _pitch_counter_and_result(one_batter):
        # hit first pitch
        if len(one_batter) == 1:
            # reliever
            if 'relieved' in one_batter[0]:
                return 0, None
            # pinch fielder
            if ' in ' in one_batter[0]:
                return 0, None
            # pinch hitter
            if 'hit for' in one_batter[0]:
                return 0, None
            # pick off
            if 'picked off' in one_batter[0]:
                return 0, None
            number_of_pitches = 1
            result = one_batter[0]
        else:
            pitches = one_batter[0].split(',')
            number_of_pitches = len(pitches)
            result = one_batter[1]
        res = 'O'
        if 'struck' in result:
            res = 'SO'
            number_of_pitches -= 1
        elif 'hit' in result:
            res = 'HBP'
            # FIXME: it should be clarified if hit-by-pitched-ball counts as a ball
            # number_of_pitches -= 1
        elif 'singled' in result:
            res = 'H'
        elif 'walk' in result:
            res = 'BB'
            number_of_pitches -= 1
        elif 'doubled' in result:  # NOTE: use 'doubled' because 'double play' can be interpreted as 'double'
            res = 'D'
        elif 'tripled' in result:
            res = 'T'
        elif 'homerun' in result or 'homer' in result:
            res = 'HR'
        return number_of_pitches, res

    def _covariance(self, number_of_pitches, results):
        """
        
        :param number_of_pitches: 
        :param results: should contain (all raw result and average, obp, and slg)
        :return: 
        """
        pass


if __name__ == '__main__':
    pass
