#!python
# main module for data gathering
import re
import os
import time
import logging
import datetime
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
youtube_driver = webdriver.Chrome(r'E:\Utilities\chromedriver.exe')
youtube_driver.set_page_load_timeout(30)


def get(video_id: str):
    """Function to send GET with limit on attempts of a given URL
    and return the soup object
    """

    url = 'https://www.youtube.com/watch?v={0}'.format(video_id)

    # catch error when parsing the website
    try:
        youtube_driver.get(url)
        time.sleep(LOADING_PAUSE_TIME)

        # scroll down the browser to load <comments number>
        TouchActions(youtube_driver).scroll(0, Y_SCROLL).perform()
        time.sleep(SCROLL_PAUSE_TIME)

        # repeating scroll down the window until all comments are captured
        for _ in range(0, PAGE_OF_COMMENT):
            TouchActions(youtube_driver).scroll(0, Y_SCROLL * 10).perform()
            time.sleep(SCROLL_PAUSE_TIME)

        soup = BeautifulSoup(youtube_driver.page_source, features='html5lib')

        # # loading the web page
        # time.sleep(LOADING_PAUSE_TIME)

        youtube_driver.close()

        return soup

    except Exception:
        # write to log
        logging.warning('[Error] failed to extract {0}'.format(url))
        return None


def tidy_data(video_id: str, soup):
    """Function to split and categorize raw data from HTTP response
    and package all related information into a list
    """

    # find video name
    name = soup.find('yt-formatted-string', class_='style-scope ytd-video-primary-info-renderer').string

    # find date of publish
    date = soup.find('span', class_='date style-scope ytd-video-secondary-info-renderer').string
    tmp = re.search(r'([A-Z][a-z]{2,3})\s(\d+),\s(\d+)', date)
    if not tmp:
        tmp = re.search(r'(\d+)\w(\d+)\w(\d+)', date).groups()
        date = datetime.date(int(tmp[0]), int(tmp[1]), int(tmp[2]))
    else:
        date = datetime.date(interpret_published_date(tmp[1]), int(tmp[2]), int(tmp[3]))

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
        tidy_comment += [*word_list]

    single_video_data = [video_id, name, date, view, like, no_comments, tidy_comment]

    return single_video_data


def interpret_published_date(date_raw: str):
    """"Function to match a abbr to month
    """

    return {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
            'June': 6, 'July': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10,
            'Nov': 11, 'Dec': 12}[date_raw]


def get_all_ids(channel_url: str):
    """"Function to fetch all url, title, and published date of a
    given Youtube channel.
    """

    if not re.search('www.youtube.com/channel/\w+', channel_url):
        return 1
    elif channel_url[-1] != '/':
        channel_url += '/videos'
    else:
        channel_url += 'videos'




if __name__ == '__main__':
    video_id = 'YTxYykhQZbI'
    response = get(video_id)
    if response:
        data = tidy_data(video_id, response)
        print(data)
