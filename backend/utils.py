# -*- coding: utf-8 -*-
"""
Emotional-YouTube Collection of Utilities
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

import re
import os
import langdetect
from wordcloud import WordCloud
from typing import Optional, Union, List, Tuple
from backend.datatypes import Video, Report, DataFetchingError, UrlError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion
from google.cloud import language
from google.cloud.language import enums, types
from google.cloud.language import LanguageServiceClient

# YouTube Data API offsets
YOUTUBE_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
MAX_NUMBER_COMMENTS = 100
NUM_RESULTS_PER_REQUEST = 5
DEVELOPER_KEY = os.environ["GCP_APIKEY_EmotionalYouTube"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

# Sentiment analysis mark scale and magnitude scale
SCORE_SCALE = [-0.5, -0.3, -0.1, 0.1, 0.3, 0.5]

# Word-cloud generation constants
EN_FONT = "CODE Light.otf"
CH_FONT = "STKAITI.TTF"
PATH_TO_IMG = r"..\dat\img\{}.png"
PATH_TO_STOPWORDS = r"..\dat\{}_stopwords.txt"
PATH_TO_FONTS = r"..\dat\{}"


def _init_service() -> Optional[Resource]:
    """Function to construct a API resource.
    """
    try:
        return build(serviceName=YOUTUBE_SERVICE_NAME, version=YOUTUBE_API_VERSION,
                     developerKey=DEVELOPER_KEY)
    except HttpError:
        print("Fail to construct a resource for interacting with YouTube Data API.")
    except UnknownApiNameOrVersion:
        print("Error at API name or version.")
    return None


def translate_url_to_id(url: str) -> Optional[str]:
    """Function that translate string id to VideoId object
    """
    video_id_pattern = re.compile(r"(?<=\?v\=)([A-Za-z0-9_-]+)")
    video_id = re.findall(video_id_pattern, url)

    if video_id:
        # return the first match
        return video_id[0][1]
    else:
        raise UrlError(url)


def _remove_empty_kwargs(**kwargs) -> dict:
    """Helper function removes bad keys in kwargs.
    """
    good_kwargs = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


def _get_comments(client: Resource, **kwargs) -> List[str]:
    """Function to obtain comments of the video that has video_id in the order 
    of relevance. ptoken marks where to find the next page of comments. Function 
    returns a list of comment text.
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
            # TODO: catch

        if "nextPageToken" in response:
            kwargs["pageToken"] = response.get("nextPageToken")
        else:
            break

    return comments


def _video_meta_by_id(client: Resource, **kwargs) -> List[Union[List[str], str]]:
    """Function to retrieve meta data: the title, channel_id, channel_title, and 
    tags of the given video. Returns a list of these information.
    """
    kwargs = _remove_empty_kwargs(**kwargs)

    response = client.videos().list(
        **kwargs
    ).execute()

    if not response["items"]:
        raise DataFetchingError(kwargs["id"])
        # TODO catch

    # meta data
    title = response["items"][0]["snippet"]["title"]
    channel_id = response["items"][0]["snippet"]["channelId"]
    channel_title = response["items"][0]["snippet"]["channelTitle"]
    tags = response["items"][0]["snippet"].get("tags")
    return [title, channel_id, channel_title, tags]


def video_data_aggregate(video_id: str) -> Optional[Video]:
    """Facade function to gather information about the video and encapsulate to 
    Video object.
    """
    client = _init_service()
    try:
        # gather meta data
        meta = _video_meta_by_id(client, part="snippet", id=video_id)
        comments = _get_comments(client, part="snippet", videoId=video_id,
                                 maxResults=NUM_RESULTS_PER_REQUEST, pageToken="",
                                 order="relevance", textFormat="plainText")
        # guess language for the majority of the comments
        lang = _detect_lang(comments)
        # encapsulate
        params = ["_id", "video_title", "channel_id",
                  "channel_title", "tags", "comments", "lang"]
        video_meta = [video_id] + meta + [comments] + [lang]
        return Video(**dict(zip(params, video_meta)))
    except DataFetchingError as e:
        print(e)
        return None
        # TODO(harry) add logging module


def _detect_lang(comments: List[str]) -> str:
    """Helper function to detect the language of the comments.
    """
    text = "".join(comments)
    lang = langdetect.detect(text)
    return lang


def _extract_adjective(client: LanguageServiceClient, comments: List[str]) -> str:
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


# TODO(harry) update api call
def _sentiment_analysis(client: LanguageServiceClient, text: str) -> Tuple[str, str]:
    """detects sentiment in the text."""
    length = text.count(" ") + 1

    # instantiates a plain text document
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # detects sentiment in the document
    sentiment = client.analyze_sentiment(document).document_sentiment
    if not sentiment:
        return "", ""
    else:
        score = sentiment.score
        magnitude = sentiment.magnitude

        saturation = magnitude / length > 0.1

        if score <= SCORE_SCALE[0]:
            return "Audiences have apparently negative reviews", "&#x1f620"
        elif SCORE_SCALE[0] < score <= SCORE_SCALE[1]:
            return "The reviews are somewhat negative", "&#x2639"
        elif SCORE_SCALE[1] < score < SCORE_SCALE[2]:
            return "The reviews are slightly negative", "&#x1f641"
        elif SCORE_SCALE[2] <= score <= SCORE_SCALE[3]:
            if saturation:
                return "Audiences have mixed reviews", "&#x1f928"
            else:
                return "Audiences are neutral", "&#x1f636"
        elif SCORE_SCALE[3] < score <= SCORE_SCALE[4]:
            return "Reviews are pretty positive~", "&#128578"
        else:
            return "Reviews are complimenting!", "&#x1f604"


def _generate_word_cloud(filename: str, text: str, lang: str) -> str:
    """Function to generate word cloud and returns the absolute path to the image.
    """
    # extend to file file path
    this_path = os.path.abspath(os.path.dirname(__file__))

    stopwords_file = os.path.join(this_path, PATH_TO_STOPWORDS.format(
        rf"{['en', 'zh-cn'][lang == 'zh-cn']}"))
    file_out_path = os.path.join(this_path, PATH_TO_IMG.format(filename))
    # bg_image_path = os.path.join(this_path, r"..\dat\wcloud_bg.jpg")

    if lang == "zh-cn":
        font_path = os.path.join(this_path, PATH_TO_FONTS.format(CH_FONT))
    else:
        font_path = os.path.join(this_path, PATH_TO_FONTS.format(EN_FONT))

    # background_image = plt.imread(bg_image_path)
    # fetch all stopwords
    stopwords = set("")
    if lang == "en":
        with open(stopwords_file) as file:
            words = [word.rstrip() for word in file.readlines()]
        stopwords.update(words)

    wc = WordCloud(
        background_color=None,
        mode="RGBA",
        font_path=font_path,
        max_words=2000,
        width=1000,
        height=800,
        max_font_size=150,
        random_state=10,
        stopwords=stopwords
    )

    wc.generate_from_text(text)

    # process_word = WordCloud.process_text(wc, text)
    # sorted_keywords = sorted(process_word.items(), key=lambda e: e[1], reverse=True)
    # print(sorted_keywords[:50])
    # img_colors = ImageColorGenerator(background_image)
    # wc.recolor(color_func=img_colors)

    wc.to_file(file_out_path)

    abs_path_to_img = os.path.join(this_path, PATH_TO_IMG.format(filename))

    return abs_path_to_img


def get_report(video: Video) -> Optional[Report]:
    """Facade function to get sentiment analysis report and to get the path to
    the word-cloud image.
    """
    if not video.lang:
        raise AttributeError(f"Error: video(id: {video.get_id()}) language is not set.")
        # TODO: catch
    # acquire nlp client
    nlp = language.LanguageServiceClient()

    adj_list = _extract_adjective(nlp, video.comments)
    attitude, emoji = _sentiment_analysis(nlp, " ".join(video.comments))
    wcloud_img_path = _generate_word_cloud(video.get_id(), adj_list, video.lang)

    init_dict = dict(zip(["_id", "video_title", "attitude", "emoji", "wcloud", "tags"],
                         [video.get_id(), video.video_title, attitude, emoji, wcloud_img_path,
                          video.tags]))
    return Report(**init_dict)


if __name__ == "__main__":
    v = video_data_aggregate("PTZiDnuC86g")
    r = get_report(v)
    print(r)
