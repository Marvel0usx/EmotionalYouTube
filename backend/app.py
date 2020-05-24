# -*- coding: utf-8 -*-
"""
Emotional-YouTube Collection of Utilities
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

import os
import db
import base64
from interface import main
from datatypes import Report
from flask_cors import cross_origin
from flask import Flask, jsonify


# init app
app = Flask(__name__)

# config app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, r"..\dat\db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# config, create database, and update the bound app with sqlalchemy and marshmallow
app = db.init_db(app)


@app.route("/analysis/<vid>", methods=["GET"])
@cross_origin()
def rest_return_report(vid: str):
    """Route for getting report by providing video id. Function returns
    formatted json file on success; returns empty json file otherwise.
    """
    # TODO: logging
    if db.DBM.does_exist(vid):
        if not db.DBM.is_expired(vid):
            report = db.DBM.select_report_from_db(vid)
            return process_response(report)
        else:
            new_video_meta, new_report = main(vid)
            db.DBM.update_entry(vid, new_video_meta, new_report)
            return process_response(new_report)
    else:
        new_video_meta, new_report = main(vid)
        db.DBM.add_entry_to_db(vid, new_video_meta, new_report)
        return process_response(new_report)


def process_response(report: Report):
    """Helper function to format json file as response."""
    # encode image to base64 string
    response = dict()

    response["attitude"] = report.attitude
    response["video_title"] = report.video_title
    response["emoji"] = report.emoji

    with open(report.wcloud, "rb") as img:
        b64_img_str = base64.b64encode(img.read()).decode("ascii")
        response["wcloud"] = b64_img_str

    return jsonify(**response)


if __name__ == "__main__":
    app.run(debug=True)
