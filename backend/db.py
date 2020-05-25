# -*- coding: utf-8 -*-
"""
Emotional-YouTube Collection of Utilities
Jan(Zhan) Lu and Haoyan Wang, Winter 2020

This code is provided for non-commercial and study purpose.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, should conform to the open source licence as provided.

"""

from sqlalchemy import exc
from . import datatypes
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


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

    def __init__(self, video_id: str, video_meta: datatypes.Video, report: datatypes.Report, latest_update):
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
    def select_report_from_db(vid: str) -> datatypes.Report:
        """Function to retrieve the record who has the given video_id.
        """
        # select by primary key
        return _ReportEntry.query.filter_by(video_id=vid).first().report

    @staticmethod
    def does_exist(vid: str) -> bool:
        """Helper function to check for existence."""
        res = _ReportEntry.query.filter_by(video_id=vid).first()
        return True if res else False

    @staticmethod
    def is_expired(vid: str) -> bool:
        """Function to check whether report is expired or not."""
        entry = _ReportEntry.query.filter_by(video_id=vid).first()
        return datetime.utcnow() - entry.latest_update > timedelta(10)

    @staticmethod
    def update_entry(vid, video_meta, report):
        """Function to update the entry indexed by video_id."""
        _ReportEntry.query.get(vid).update({video_meta: video_meta, report: report})

    @staticmethod
    def add_entry_to_db(vid: str, video_meta: datatypes.Video, report: datatypes.Report) -> None:
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
