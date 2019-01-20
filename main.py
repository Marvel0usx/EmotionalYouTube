#!python
# Server side script

import time
import json
import datetime
import threading
# import feature
import data_gathering
from queue import Queue
from selenium import webdriver


get_lock = threading.RLock()


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

    works = []

    # iterate through and pick valid videos
    for id, date in zip(ids, dates):
        if begin and end:
            if begin_date <= date <= end_date:
                works.append('https://www.youtube.com/watch?v=' + id)
        else:
            works.append('https://www.youtube.com/watch?v=' + id)

    return works


if __name__ == '__main__':
    url = 'https://www.youtube.com/channel/UCHRUAMAzVUS_Szvxn55GXaQ/'
    youtube_driver = webdriver.Chrome(r'E:\Utilities\chromedriver.exe')
    youtube_driver.set_page_load_timeout(30)
    works = get_channel_data(youtube_driver, url)
