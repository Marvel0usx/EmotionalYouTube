# -*- coding: utf-8 -*-
"""
EmotionalYouTube Collection of Features
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

import re
import os
from typing import Optional, Union, List
from data import Video, DataFetchingError, UrlError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion

# YouTube Data API offsets
YOUTUBE_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = os.environ["GCP_APIKEY_EmotionalYouTube"]

# Constants
MAX_NUMBER_COMMENTS = 10
NUM_RESULTS_PER_REQUEST = 1


def init_service() -> Optional[Resource]:
    """Function to construct a API resource.
    """
    try:
        return build(serviceName=YOUTUBE_SERVICE_NAME, version=YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    except HttpError:
        print("Fail to construct a resource for interacting with YouTube Data API.")
    except UnknownApiNameOrVersion:
        print("Error at API name or version.")
    return None


def translate_url_to_id(url: str) -> Optional[str]:
    """Function that translate string id to VideoId object
    """
    video_id_pattern = re.compile(r"\?(v|vi)=([A-Za-z0-9_-]+)")
    video_id = re.findall(video_id_pattern, url)

    if video_id:
        # return the first match
        return video_id[0][1]
    else:
        raise UrlError(url)


def remove_empty_kwargs(**kwargs) -> dict:
    """Helper function removes bad keys in kwargs.
    """
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def get_comments(client: Resource, **kwargs) -> List[str]:
    """Function to obtain comments of the video that has video_id in the order of relevance.
    ptoken marks where to find the next page of comments. Function returns a list of comment
    text.
    """
    comments = []
    for _ in range(0, MAX_NUMBER_COMMENTS, NUM_RESULTS_PER_REQUEST):
        try:
            response = client.commentThreads().list(
                **kwargs
            ).execute()
        except HttpError as e:
            print(e)
            return comments

        if response:
            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]
                text = comment["snippet"]["textDisplay"]
                comments.append(text)
        else:
            raise DataFetchingError(kwargs["videoId"])

        if "nextPageToken" in response:
            kwargs["pageToken"] = response.get("nextPageToken")
        else:
            break

    return comments


def video_meta_by_id(client: Resource, **kwargs) -> List[Union[List[str], str]]:
    """Function to retrieve meta data: the title, channel_id, channel_title, and tags of the given video.
    Returns a list of these information.
    """
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.videos().list(
        **kwargs
    ).execute()

    if not response["items"]:
        raise DataFetchingError(kwargs["id"])

    # information about the video
    title = response["items"][0]["snippet"]["title"]
    channel_id = response["items"][0]["snippet"]["channelId"]
    channel_title = response["items"][0]["snippet"]["channelTitle"]
    tags = response["items"][0]["snippet"].get("tags")
    return [title, channel_id, channel_title, tags]


def video_data_aggregate(client: Resource, video_id) -> Video:
    """Function to gather information about the video and encapsulate to Video object.
    """
    try:
        meta = video_meta_by_id(client, part="snippet", id=video_id)
        comments = get_comments(client, part="snippet", videoId=video_id, maxResults=NUM_RESULTS_PER_REQUEST,
                                pageToken="", order="relevance", textFormat="plainText")
        params = ["id_", "title", "channel_id", "channel_title", "tags", "comments"]
        video_meta = [video_id] + meta + [comments]
        return Video(**dict(zip(params, video_meta)))
    except DataFetchingError as e:
        print(e)
        # TODO(harry) add logging module


if __name__ == "__main__":
    youtube = init_service()
    v = video_data_aggregate(youtube, "2DTNgvcRFE8")
    print(v.comments)

