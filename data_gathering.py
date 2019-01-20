#!python
# main module for data gathering
import re
import os
import time
import logging
import datetime
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.touch_actions import TouchActions

################
ID = 0
NAME = 1
PUBLISHED_DATE = 2
VIEW_NUM = 3
LIKE = 4
COMMENT_NUM = 5
COMMENT = 6

Y_SCROLL = 500
# TODO change this number
PAGE_OF_COMMENT = 1
LOADING_PAUSE_TIME = 3
SCROLL_PAUSE_TIME = 2
APIKEY = os.environ['APIKEY']
################

logging.basicConfig(filename='spyder.log', level=logging.DEBUG)


def get(driver, video_id: str):
    """Function to send GET with limit on attempts of a given URL
    and return the soup object
    """

    url = 'https://www.youtube.com/watch?v={0}'.format(video_id)

    # catch error when parsing the website
    try:

        driver.get(url)
        time.sleep(LOADING_PAUSE_TIME)

        scroll_down(driver, Y_SCROLL, 1)
        soup = scroll_down(driver, Y_SCROLL * 10, PAGE_OF_COMMENT)

        driver.close()

        return soup

    except Exception:
        # write to log
        logging.warning('[Error] failed to extract {0}'.format(url))
        return None


def scroll_down(driver, y_value=None, times=None):
    """"Procedure to scroll down a web page for n times or
    scroll it till its end if <times> is undefined
    """

    if y_value:
        for _ in range(0, times):
            # scroll down the browser n times to load <comments number>
            TouchActions(driver).scroll(0, y_value).perform()
            time.sleep(SCROLL_PAUSE_TIME)

        return BeautifulSoup(driver.page_source, features='html5lib')

    else:
        # repeating scroll down the window until no more comments are loaded
        soup = BeautifulSoup(driver.page_source, features='html5lib')

        while True:
            all_videos = soup.find_all('a', id='video-title',
                                       class_='yt-simple-endpoint style-scope ytd-grid-video-renderer')
            TouchActions(driver).scroll(0, Y_SCROLL * 10).perform()
            time.sleep(SCROLL_PAUSE_TIME)
            soup = BeautifulSoup(driver.page_source, features='html5lib')
            new_videos = soup.find_all('a', id='video-title',
                                       class_='yt-simple-endpoint style-scope ytd-grid-video-renderer')

            if new_videos == all_videos:
                driver.close()
                return new_videos


def tidy_data(video_id: str, soup):
    """Function to split and categorize raw data from HTTP response
    and package all related information into a list
    """

    # find video name
    name = soup.find('yt-formatted-string', class_='style-scope ytd-video-primary-info-renderer').string

    # find likes
    likes_raw = soup.find_all('yt-formatted-string', class_='style-scope ytd-toggle-button-renderer style-text')
    like = int(likes_raw[0].string)
    # dislike = int(likes_raw[1].string)

    # find views
    view = soup.find('span', class_='view-count style-scope yt-view-count-renderer').string

    # get <comments number>
    no_comments_raw = soup.find('yt-formatted-string', class_='count-text style-scope ytd-comments-header-renderer')
    no_comments = int(*re.findall(r'\d+', no_comments_raw.string))

    # find all comments
    comments_raw = soup.find_all('yt-formatted-string', class_='style-scope ytd-comment-renderer')

    pattern = re.compile(r'\d*,*\d+')
    replace = re.compile(r',')

    tmp = re.search(pattern, view).group()
    view = int(re.sub(replace, '', tmp))

    # print('like: %i dislike: %i' % (like, dislike))
    # print('Total view:', view)

    # Formatting comment
    tidy_comment = []
    for comment in comments_raw:
        text = comment.string
        divide_pattern = re.compile(r'\b\w+\b')
        word_list = re.findall(divide_pattern, text)
        tidy_comment += [word.lower() for word in word_list]

    date = find_published_date(soup)

    single_video_data = [video_id, name, date, view, like, no_comments, tidy_comment]

    return single_video_data


def find_published_date(soup):
    # find date of publish
    date = soup.find('span', class_='date style-scope ytd-video-secondary-info-renderer').string
    tmp = re.search(r'([A-Z][a-z]{2,3})\s(\d+),\s(\d+)', date)
    if not tmp:
        tmp = re.search(r'(\d+)\w(\d+)\w(\d+)', date).groups()
        date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    else:
        date = datetime.date(interpret_published_date(tmp[0]), int(tmp[1]), int(tmp[2]))

    return date


def interpret_published_date(date_raw: str):
    """"Function to match a abbr to month
    """

    return {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
            'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
            'Nov': 11, 'Dec': 12}[date_raw]


def get_all_ids(driver, channel_url: str):
    """"Function to fetch all url, title, and published date of a
    given Youtube channel.
    """

    # collecting all videos in video section
    try:
        driver.get(channel_url)
        soup = scroll_down(driver)
    except Exception:
        logging.debug('[Error] failed to extract {0}'.format(channel_url))
        return None

    ids = []
    for video in soup:
        # search for id of which behind 'v='
        res = re.search(r'(?=v=([A-Za-z0-9-_]+))', video.attrs['href'])
        ids.append(res.groups()[0])

    return ids


def get_all_publish_dates_in_channel(ids):
    """"Function to find all published date of videos in a channel
    """

    urls = ['https://www.youtube.com/watch?v={0}'.format(video_id) for
            video_id in ids]

    all_published_date = []
    for url in urls:
        soup = BeautifulSoup(requests.get(url).text, features='html5lib')
        date_tag = soup.find_all('strong', class_='watch-time-text')

        date = re.search(r'([A-Z][a-z]{2,3})\s(\d+),\s(\d+)', date_tag[0].string).groups()
        all_published_date.append(datetime.date(int(date[2]), interpret_published_date(date[0]), int(date[1])))

    return all_published_date


if __name__ == '__main__':
    video_id = 'YTxYykhQZbI'
    youtube_driver = webdriver.Chrome(r'E:\Utilities\chromedriver.exe')
    youtube_driver.set_page_load_timeout(30)
    response = get(youtube_driver, video_id)
    if response:
        data = tidy_data(video_id, response)
        print(data)
    ids = get_all_ids(youtube_driver, 'https://www.youtube.com/channel/UCHRUAMAzVUS_Szvxn55GXaQ/videos')
