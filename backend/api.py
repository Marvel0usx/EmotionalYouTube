import os
from typing import Optional
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion

YOUTUBE_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = os.environ["GCP_APIKEY_EmotionalYouTube"]


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


def get_comments(youtube, video_id, channel_id=None):
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        # channelId=channel_id,
        textFormat="plainText"
        ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        print("Comment by %s: %s" % (author, text))

    return results["items"]


if __name__ == "__main__":
    youtube = init_service()
    get_comments(youtube, "HxGT5z6d-GA")
