from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from typing import Optional
from data import Report
from app import set_app

# flask application associated
_app = set_app()

# init database
_db = SQLAlchemy(_app)
# init ma
_ma = Marshmallow(_app)


# product class/model
class _ReportEntry(_db.Model):
    """Private class represents the database model.

    === Attributes ===
    video_id: video id primary key;
    video_meta: pickled Video object of video meta data;
    report: pickled Report object of analysis report;
    latest_update: latest update for the report.
    """
    video_id = _db.Column(_db.String(20), primary_key=True)
    video_meta = _db.Column(_db.PickleType)
    report = _db.Column(_db.PickleType)
    latest_update = _db.Column(_db.DateTime)

    def __init__(self, video_id: str, video_meta: Video, report: Report, latest_update):
        self.report = report
        self.video_id = video_id
        self.video_meta = video_meta
        self.latest_update = latest_update


# db schema for serialization
class _ReportEntrySchema(_ma.Schema):
    class Meta:
        fields = ("video_id", "video_meta", "report", "latest_update")


# init schema
_report_schema = _ReportEntrySchema()


# ----- database management functions below -----

def select_report_from_db(video_id: str) -> Optional[Report]:
    """Function to retreive the record who has the given video_id
    """

def add_entry_to_db(new_report_entry):
    # update database
    _db.session.add(new_report_entry)
    _db.session.commit()