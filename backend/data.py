# -*- coding: utf-8 -*-
"""
EmotionalYouTube Project Datatypes
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

__author__ = 'Jan(Zhan) Lu and Haoyan Wang'


class Video:
    """Class to store all related information of a YouTube video.

    === Attributes ===
    _id         : The unique YouTube id of the video;
    title       : String of the title of the video;
    channel_id  : The unique YouTube id of the channel;
    num_comment : number of comments below this video;
    comments    : comments of this video;
    lang        : language of the majority of comments
    """

    _id        : str
    lang       : str
    title      : str
    channel_id : str
    num_comment: int

    def __init__(self, **kwargs):
        valid_keys = ["_id", "title", "channel_id", "num_comment", "comments", "lang"]

        for key in valid_keys:
            self.__dict__[key] = kwargs.get(key)

    def __repr__(self) -> str:
        return self.title


class UrlError(Exception):
    """Exception class for URL error

    === Attributes ===
    url: string representation of the url
    """

    url: str

    def __init__(self, url):
        self.url = url

    def __str__(self) -> str:
        return f'URL Error on {self.url}'


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
