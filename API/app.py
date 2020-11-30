"""
The app.py file (main file for the entire api)
"""
from flask import Flask, send_file, request
from constants import *
from utils import *
from flask_restful import Api
from API_Object import GetPostsFromUser

"""
Globals variables
"""
app = Flask(__name__)
api = Api(app)


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
    for row in range(33):  # Getting the image parms
        if request.args.get(f'row{str(row)}'):
            sliders.append(float(request.args.get(f'row{str(row)}')))
        else:
            sliders.append(0)
    filename = save_anime_face(sliders)
    return send_file(os.path.join(PLACEHOLDING_DATA_DIR, filename))


@app.route('/upload_anime_face', methods=["GET", "POST"])
def upload_anime_face_to_data_base():
    """
    Sending the file
    :return: A file in the directory
    """
    if request.method == "POST":
        json_data = request.get_json()  # Getting the json data
        is_private, image_parms, title, tags, accoundId, captions = json_data['isPrivate'], json_data['imageParms'], json_data['title'], json_data['tags'], json_data['accountId'], json_data['captions']
        timestamp, made_with, filename = time.time(), "Anime Auto Encoder", f"{time.time()}, {accoundId}.png"
        """
        Putting the json data into the database
        """
        print(image_parms)
        save_anime_face(image_parms, loc=os.path.join(IMAGES_DIR, filename)) # Saving the image
        cursor.execute(
            "INSERT INTO Posts (accountId, timestamp, madeWith, fileLocation, title, captions, isPrivate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (accoundId, timestamp, made_with, filename, title, captions,
             is_private))  # Uploading everything except tag

        postId = cursor.lastrowid
        cursor.execute("INSERT INTO Tags (postId, tag1, tag2, tag3) VALUES (%s, %s, %s, %s)", (postId, tags[0], tags[1], tags[2])) # Uploading tags
        db.commit() # Upload to database
        return "Success"

    return "<h1> Working </h1>"

"""
A list of API 
"""
api.add_resource(GetPostsFromUser, "/api/get-posts-from-user/<int:id>")
if __name__ == "__main__":
    app.run()  # Running the app
