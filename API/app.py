"""
The app.py file (main file for the entire api)
"""
from utils import *
import os
from flask import Flask, send_file, request
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

@app.route('/getanimeface')
def return_anime_face():
    sliders = []
    for row in range(33): # Getting the image parms
        if request.args.get(f'row{str(row)}'):
            sliders.append(float(request.args.get(f'row{str(row)}')))
        else:
            sliders.append(0)
    filename = save_anime_face(sliders)
    return send_file(os.path.join(PLACEHOLDING_DATA_DIR, filename))


@app.route('/getfile/<filename>', methods=["GET"])
def get_file(filename):
    """
    Sending the file
    :return: A file in the directory
    """

    return send_file(os.path.join(IMAGES_DIR, filename), mimetype="image/png")
if __name__ == "__main__":
    app.run(debug=True, port=5000) # Running the app