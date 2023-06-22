# -*- coding: utf-8 -*-
"""Module for storing the backweb server to render all the dags"""

import json

from flask import Flask  # pylint: disable=import-error

app = Flask(__name__)


@app.route("/")
def index():
    """Main Home Page"""

    # We get the

    return json.dumps({"name": "alice", "email": "alice@outlook.com"})
