# -*- coding: utf-8 -*-
"""
EmotionalYouTube Project Main Interface of Backend
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

# use packages
import os
from backend import utils
from typing import Tuple, Optional
from apiclient.discovery import build
from googleapiclient.errors import HttpError
from backend.data import UrlError

# the service name has to be correspond to the service name in the documentation
# and the service name for YouTube Data API is youtube.googleapis.com
YOUTUBE_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
API_KEY = os.environ.get('apikey')
MAX_RESULT = 50

# initialize API client
youtube_data = build(YOUTUBE_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)


def main(url: str) -> Optional[Tuple]:
    """Main interface for backend, called by flask. It returns the
    result of sentiment analysis and the filename of the word cloud
    picture.
    """
    try:
        _id = utils.translate_url_to_id(url)
    except UrlError:
        return

    if not _id:
        return
    try:
        entity = utils.video_data_aggregate(youtube_data, _id, MAX_RESULT)
    except HttpError:
        return
    else:
        return utils.analysis(entity)


if __name__ == '__main__':
    # start testing below

    print(main('https://www.youtube.com/watch?v=6ajTcwJBbw4'))
