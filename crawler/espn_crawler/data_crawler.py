# -*- coding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet
from crawler.espn_crawler.schedule_parser import ScheduleParser


class EspnCrawler:
    def __init__(self, interval):
        self.interval = ScheduleParser(interval[0], interval[1]).interval
        self.base_url_for_schedule = 'http://espn.go.com/mlb/schedule/_/date/'
        self.base_game_url = 'http://espn.go.com/mlb/playbyplay?gameId='
        
    def run(self, game_type="play-by-play"):
        game_list = []
        for date in self.interval:
            game_list += self.schedule_parser(date)
        all_game_in_interval = []
        for one_game in game_list:
            if game_type.lower() == "play-by-play":
                all_game_in_interval.append(self.play_by_play_parser(one_game))
            elif game_type.lower() == "pitch-by-pitch":
                all_game_in_interval.append(self.pitch_by_pitch_parser(one_game))
            else:
                raise NotImplementedError()
        return all_game_in_interval
        
    def schedule_parser(self, date):
        date_url = self.base_url_for_schedule + str(date)
        url_data = self.url_parser(date_url)
        soup = BeautifulSoup(url_data, 'lxml')
        valid_list = soup.find_all('table')
        game_id_list = []
        row_lists = valid_list[0].find_all('tr')  # The first list is current date (other two are next 2 days)
        for row in row_lists:
            hyper_link = row.find_all('a')
            for links in hyper_link:
                if 'gameId' in str(links):
                    game_id = str(links).split('gameId=')[1].split('"')[0]
                    game_id_list.append(game_id)
            row = str(row)
        return game_id_list\
    
    # make url as string
    def url_parser(self, url):
        urldata = urlopen(url)
        # this encoding should be checked automatically
        data = urldata.read()
        encoding = chardet.detect(data)
        new_url_data = str(data.decode(encoding['encoding']))
        return new_url_data

    def one_game_parser(self, url):
        url_data = self.url_parser(url)
        soup = BeautifulSoup(url_data, 'lxml')
        valid_list = soup.find_all('table')
        is_valid = False
        valid_data = []
        # table parser
        for elm in valid_list:
            row_lists = elm.find_all('tr')
            one_inning = []
            for row in row_lists:
                new_row = list(row.find_all('td'))
                if len(new_row) != 0:
                    if 'Play-By-Play' in str(new_row[0]):
                        is_valid = True
                if is_valid:
                    if len(new_row) != 0:
                        one_inning.append(new_row)
                    else:
                        if len(one_inning) != 0:
                            valid_data.append(one_inning)
                            one_inning = []
        # parser each cell
        html_return = []
        for inning in valid_data:
            inn = []
            for data in inning:
                row = []
                for column in data:
                    column = str(column)
                    parsed_column = column.split('<')
                    real_data = ""
                    for elm in parsed_column:
                        if not elm.endswith('>') and elm != '':
                            real_data += elm.split('>')[1]
                    row.append(real_data)
                inn.append(row)
            html_return.append(inn)
        return html_return
    
    def play_by_play_parser(self, game_id):
        url = self.base_game_url + str(game_id)
        return self.one_game_parser(url)

    def pitch_by_pitch_parser(self, game_id):
        url = self.base_game_url + str(game_id) + "&full=1"
        return self.one_game_parser(url)
        
       
if __name__ == '__main__':
    mm = EspnCrawler([{'year': 2015, 'month': 5, 'day': 10},
                      {'year': 2015, 'month': 5, 'day': 10}])
    mm.schedule_parser(mm.interval[0])
