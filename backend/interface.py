# -*- coding: utf-8 -*-
"""
Emotional-YouTube Project Main Interface of Backend
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

from typing import Optional, Tuple
from backend.datatypes import Video, Report
from backend.utils import video_data_aggregate, get_report


def main(video_id: str) -> Tuple[Optional[Video], Optional[Report]]:
    """Main interface for backend, called by flask. It returns the
    result of sentiment analysis and the filename of the word cloud
    picture.
    """
    video = video_data_aggregate(video_id)
    if not video:
        return None, None
    else:
        report = get_report(video)
    return video, report


if __name__ == "__main__":
    # init_db testing below
    main("https://www.youtube.com/watch?v=PTZiDnuC86g")
