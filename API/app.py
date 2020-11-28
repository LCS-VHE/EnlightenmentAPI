"""
The app.py file (main file for the entire api)
"""
from utils import *
import os
from flask import Flask, send_file
from constants import *
from flask_restful import Api, Resource

"""
Globals variables
"""
app = Flask(__name__)

@app.route('/')
def main():
    """
    The front page of the website
    :return: A html for the user to see if it's working
    """
    return "<h1> Successful Connection</h1>"

@app.route('/getfile/<filename>', methods=["GET"])
def get_file(filename):
    """
    Sending the file
    :return: A file in the directory
    """

    return send_file(os.path.join(IMAGES_DIR, filename), mimetype="image/png")
if __name__ == "__main__":
    app.run(debug=True, port=5000) # Running the app