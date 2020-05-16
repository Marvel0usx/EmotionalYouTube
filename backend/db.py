from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_sqlalchemy import BaseQuery
from flask_marshmallow import Marshmallow
from typing import Optional
from datatypes import Video, Report
from datetime import datetime, timedelta
import pickle


# init database (must be initialized first before Marshmallow)
_db = SQLAlchemy()


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
        self.video_id = video_id
        self.video_meta = video_meta
        self.report = report
        self.latest_update = latest_update


# init ma
_ma = Marshmallow()


# db schema for serialization
class _ReportEntrySchema(_ma.Schema):
    class Meta:
        fields = ("video_id", "video_meta", "report", "latest_update")


# init schema
_report_schema = _ReportEntrySchema()


class DBM:
    """Database Manager class. Class manages the read and write to the database.
    """

    @staticmethod
    def select_from_db(vid: str, attribute: str) -> Optional[BaseQuery]:
        """Function to retrieve the record who has the given video_id.
        """
        # select by primary key
        pass

    @staticmethod
    def is_exist(vid: str) -> bool:
        """Helper function to check for existence."""
        return True if _db.Query.get(vid) else False

    @staticmethod
    def is_expired(vid: str) -> bool:
        """Function to check whether report is expired or not."""
        entry = _db.Query.get(vid)
        return datetime.utcnow() - entry.latest_update > timedelta(10)

    @staticmethod
    def update_entry(vid, video_meta, report):
        pass

    @staticmethod
    def add_entry_to_db(vid: str, video_meta: Video, report: Report) -> None:
        """Function to add new report entry to database.
        """
        new_entry = _ReportEntry(vid, video_meta, report, datetime.utcnow())
        # update database
        _db.session.add(new_entry)
        try:
            _db.session.commit()
        except exc.SQLAlchemyError as e:
            # TODO logging
            pass


def init_db(app):
    """Function to initialize database, schema, and register
    with application."""
    # IMPORTANT: bind sqlalchemy to app
    _db.init_app(app)
    # IMPORTANT: bind marshmallow to app
    _ma.init_app(app)
    # IMPORTANT: bind app to sqlalchemy
    app.app_context().push()
    # IMPORTANT: create the database on disk
    _db.create_all()
    # return the bound app
    return app
