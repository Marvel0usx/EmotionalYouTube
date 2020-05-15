import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# init app
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
