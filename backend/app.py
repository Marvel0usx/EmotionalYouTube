import os
from utils import translate_url_to_id
from interface import main
from flask import Flask, jsonify
from datatypes import Report
import db

# init app
app = Flask(__name__)

# config app
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, r"..\dat\db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# config, create database, and update the bound app with sqlalchemy and marshmallow
app = db.init_db(app)


@app.route("/analysis/<link>", methods=["GET"])
def rest_return_report(link: str):
    """Route for getting report by providing video id. Function returns
    formatted json file on success; returns empty json file otherwise.
    """
    # TODO: logging
    video_id = translate_url_to_id(link)

    if not video_id:
        # TODO: return empty json
        return jsonify()

    if not db.DBM.does_exist(video_id) or db.DBM.is_expired(video_id):
        new_video_meta, new_report = main(video_id)
        db.DBM.update_entry(video_id, new_video_meta, new_report)
        return process_response(new_report)
    else:
        report = db.DBM.select_report_from_db(video_id)
        return process_response(report)


def process_response(report: Report):
    """Helper function to format json file as response."""
    # TODO
    pass


if __name__ == "__main__":
    app.run(debug=True)
