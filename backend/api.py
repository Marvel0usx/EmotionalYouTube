import os
import math
from typing import Optional, List
from data import Video, DataFetchingError
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError, UnknownApiNameOrVersion

YOUTUBE_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = os.environ["GCP_APIKEY_EmotionalYouTube"]

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


def get_comments(service: Resource, video_id: str, ptoken: str = "") -> List[str]:
    """Function to obtain comments of the video that has video_id in the order of relevance.
    ptoken marks where to find the next page of comments. Function returns a list of comment
    text.
    """
    comments = []
    for _ in range(0, MAX_NUMBER_COMMENTS, NUM_RESULTS_PER_REQUEST):
        try:
            results = service.commentThreads().list(
                part       = "snippet",
                videoId    = video_id,
                maxResults = NUM_RESULTS_PER_REQUEST,
                pageToken  = ptoken,
                order      = "relevance",
                textFormat = "plainText"
                ).execute()
        except HttpError as e:
            print(e)
            return comments

        if results:
            for item in results["items"]:
                comment = item["snippet"]["topLevelComment"]
                text = comment["snippet"]["textDisplay"]
                comments.append(text)
        else:
            raise DataFetchingError(video_id)

        if "nextPageToken" in results:
            ptoken = results.get("nextPageToken")
        else:
            break

    return comments


if __name__ == "__main__":
    youtube = init_service()
    print(get_comments(youtube, "2DTNgvcRFE8"))
