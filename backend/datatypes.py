# -*- coding: utf-8 -*-
"""
Emotional-YouTube Project Datatypes
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.
4
"""

from typing import List


class Video:
    """Class to store all related information of a YouTube video.

    === Attributes ===
    _id          : the unique YouTube id of the video;
    video_title  : string of the title of the video;
    channel_id   : the unique YouTube id of the channel;
    channel_title: title of this video's channel;
    tags         : list of tags of this video;
    comments     : comments of this video;
    lang         : language of the majority of comments
    """

    _id        : str
    lang       : str
    tags       : List[str]
    video_title: str
    channel_id : str
    channel_title: str
    comments   : List[str]

    def __init__(self, **kwargs):
        valid_keys = ["_id", "video_title", "channel_id", "channel_title", "tags", "comments", "lang"]

        for key in valid_keys:
            self.__dict__[key] = kwargs.get(key)

    def __repr__(self) -> str:
        return self.title

    def get_id(self) -> str:
        return self._id


class Report:
    """Report contains the metadata of the video being analyzed and the results
    carried out by the analysis function.

    === Attributes ===
    _id: the video id that this report corresponds to;
    video_title: title of video;
    attitude: the attitude of viewers;
    emoji: emoji repr of the attitude;
    wcloud: absolute path to where the image of word-cloud is stored.
    """

    _id: str
    video_title: str
    attitude: str
    emoji: str
    wcloud: str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            # add tags and most mentioned words
            if k in ["_id", "video_title", "attitude", "emoji", "wcloud"]:
                self.__dict__[k] = v

    def __str__(self) -> str:
        return f"Video {self.video_title} (id: {self._id}) received {self.attitude}, which is {self.emoji}."


class UrlError(Exception):
    """Exception class for URL error

    === Attributes ===
    url: string representation of the url
    """

    url: str

    def __init__(self, url):
        self.url = url

    def __str__(self) -> str:
        return f"URL Error on {self.url}"


class DataFetchingError(Exception):
    """Exception class for 401-404 errors

    === Attributes ===
    _id: string representation of the id of YouTube video;
    """

    _id: str

    def __init__(self, _id):
        self._id = _id

    def __str__(self) -> str:
        return f"Error in fetching data from video id {self._id}"
