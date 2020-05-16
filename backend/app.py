import os
import datetime
from utils import translate_url_to_id
from interface import main
from db import *
from db import _ReportEntry
from flask import Flask, request, jsonify

# init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# config database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, r"..\dat\db.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def set_app():
    return app

# given id to create a report for the video
@app.route("/analysis/<url>")
def create_report():
    video_url = request.json["url"]
    video_id = translate_url_to_id(video_url)

    if not video_id:
        # TODO: return empty json
        pass

    # check if the report is available in db
    select_report_from_db()

    video_meta, report = main(video_id)
    if not video_meta or not report:
        # TODO: return empty json
        pass

    new_report_entry = _ReportEntry(video_id, video_meta,
                                   report, datetime.datetime.utcnow)

    add_entry_to_db(new_report_entry)

# run server
if __name__ == "__main__":
    app.run(debug=True)
