import re
import json
import pprint
import requests
import datetime


class JSONObject:
    def __init__(self, dic):
        self.__dict__ = dic


def parse_json(j_file: json):
    """Function to parse json to python dictionary
    """

    data = json.loads(j_file, object_hook=JSONObject)
    extract_date = re.compile(r'(\d+)-(\d+)-(\d+)')
    begin = re.search(extract_date, data['begin']).groups()
    end = re.search(extract_date, data['end']).groups

    if begin and end:
        begin_date = datetime.date(int(begin[0]), int(begin[1]), int(begin[2]))
        end_date = datetime.date(int(end[0]), int(end[1]), int(end[2]))

        data['begin'] = begin_date
        data['end'] = end_date

    return data


def post_json(j_file_post: json):
    """Function to return json to front-end
    """

    print(j_file_post)
    print('\nHTTP Response')

    headers = {"charset": "utf-8",
               "Accept": "text/plain"}


def convert_to_json(video_data: list):
    """Function to translate python data type to json
    """

    j_video_data = json.dumps(video_data)

    print('Json data has been prepared\n')
    pprint.pprint(j_video_data)


if __name__ == '__main__':
    request = {'url': 'https://www.youtube.com/channel/UCHRUAMAzVUS_Szvxn55GXaQ/videos',
           'begin': '2018-1-3',
           'end': '2019-1-3'}
    j_request = json.dumps(request)
    parse_json(j_request)
