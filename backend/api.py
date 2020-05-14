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
import langdetect
from typing import Optional, Union, List
from data import Video, DataFetchingError, UrlError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
from google.cloud import language
from google.cloud.language import enums, types
from google.cloud.language import LanguageServiceClient

# YouTube Data API offsets
YOUTUBE_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
DEVELOPER_KEY = os.environ["GCP_APIKEY_EmotionalYouTube"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

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

    # meta data
    title = response["items"][0]["snippet"]["title"]
    channel_id = response["items"][0]["snippet"]["channelId"]
    channel_title = response["items"][0]["snippet"]["channelTitle"]
    tags = response["items"][0]["snippet"].get("tags")
    return [title, channel_id, channel_title, tags]


def video_data_aggregate(client: Resource, video_id) -> Video:
    """Function to gather information about the video and encapsulate to Video object.
    """
    try:
        # gather meta data
        meta = video_meta_by_id(client, part="snippet", id=video_id)
        comments = get_comments(client, part="snippet", videoId=video_id, maxResults=NUM_RESULTS_PER_REQUEST,
                                pageToken="", order="relevance", textFormat="plainText")
        # guess language for the majority of the comments
        lang = detect_lang(comments)
        # encapsulate
        params = ["id_", "title", "channel_id", "channel_title", "tags", "comments", "lang"]
        video_meta = [video_id] + meta + [comments] + [lang]
        return Video(**dict(zip(params, video_meta)))
    except DataFetchingError as e:
        print(e)
        # TODO(harry) add logging module


def detect_lang(comments: List[str]) -> str:
    """Helper function to detect the language of the comments.
    """
    text = "".join(comments)
    lang = langdetect.detect(text)
    return lang


def extract_adjective(client: LanguageServiceClient, comments: List[str]) -> str:
    """Function all to NLP to pull out all adjectives from the text.
    """
    text = "".join(comments)
    # if isinstance(text, six.binary_type):
    #     text = text.encode("utf-8")

    # instantiates a plain text document.
    document = types.Document(
        content=text.encode("utf-8"),
        type=enums.Document.Type.PLAIN_TEXT
    )

    # decompose the text to tokens
    tokens = client.analyze_syntax(document).tokens

    # results are store as list of tokens
    adj_list = u""
    for token in tokens:
        # append all adjectives to result
        part_of_speech_tag = enums.PartOfSpeech.Tag(token.part_of_speech.tag)
        if part_of_speech_tag.name == "ADJ":
            adj_list += f"{token.text.content} "
    return adj_list


if __name__ == "__main__":
    # youtube = init_service()
    # v = video_data_aggregate(youtube, "2DTNgvcRFE8")
    # print(v.comments)
    nlp = language.LanguageServiceClient()
    t = extract_adjective(nlp, ["职责是一扇窗户，他带给人们在自由"])
    print(t)
