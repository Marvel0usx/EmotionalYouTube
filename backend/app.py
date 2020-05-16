import os
from utils import translate_url_to_id
from interface import main
from flask import Flask, request, jsonify
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
    """Route """
    print("hi!")
    video_url = request.json["link"]
    video_id = translate_url_to_id(video_url)

    # if not video_id:
    #     # TODO: return empty json
    #     return None

    # # check if the report is available in db
    # if not db.DBM.is_exist(video_id):
    #     # create new record
    #     pass
    # elif db.DBM.is_expired(video_id):
    #     # update record
    #     pass
    # else:
    #     # return as normal
    #     pass


if __name__ == "__main__":
    app.run(debug=True)
