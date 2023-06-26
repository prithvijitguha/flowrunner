# -*- coding: utf-8 -*-
"""Module docstring for flask server"""
from flask import Flask, jsonify  # pylint: disable=import-error

app = Flask(__name__)


@app.route("/")
def index():
    """Base url for homepage"""
    data = {"name": "prithvijit", "age": "30"}
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
