#!python
# Server side script

import time
import webwork
import datetime
import threading
import feature
import data_gathering
from queue import Queue
from selenium import webdriver

NUM_OF_THREAD = 5


def get_channel_data(driver, channel_url, begin=None, end=None):
    """"Function to get data list of videos within given
    time interval"""

    if begin and end:
        begin_date = datetime.date(begin[0], begin[1], begin[2])
        end_date = datetime.date(end[0], end[1], end[2])

    # fetch all id of videos in the given channel_url
    ids = data_gathering.get_all_ids(driver, channel_url)
    # fetch all published date of videos in the given channel_url
    dates = data_gathering.get_all_publish_dates_in_channel(ids)

    ids_to_explore = []

    # iterate through and pick valid videos
    for id, date in zip(ids, dates):
        if begin and end:
            if begin_date <= date <= end_date:
                ids_to_explore.append(id)
        else:
            ids_to_explore.append(id)

    for id in ids_to_explore:
        q.put(id)

    return ids_to_explore


def main(j_command):
    """Main"""

    command = webwork.parse_json(j_command)

    youtube_driver = webdriver.Chrome(r'E:\Utilities\chromedriver.exe')
    youtube_driver.set_page_load_timeout(30)

    video_url = command['url']
    video_data = data_gathering.get(youtube_driver, video_url)

    feature.generate_wordcloud(video_data)



if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=L8HEN7JZ4r4'
    youtube_driver = webdriver.Chrome(r'E:\Utilities\chromedriver.exe')
    youtube_driver.set_page_load_timeout(30)
    # works = get_channel_data(youtube_driver, url)
