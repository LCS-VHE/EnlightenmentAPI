"""
The app.py file (main file for the entire api)
"""
from flask import Flask, send_file, request
from constants import *
from utils import *
from flask_restful import Api
from API_Object import GetPostsFromUser, GetOwnUserPosts, GetRecentPost
import urllib.parse

"""
Globals variables
"""
app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = PLACEHOLDING_DATA_DIR # Saving file Directory

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

@app.route('/register', methods=["POST", "GET"])
def register():
    """
    The register object will be in the following format
    {
    "username" :
    "password" :
    }
    :return:  Success or not
    """
    return "<h1> Post Request Not Made </h1>"

@app.route('/file/image/<filename>')
def get_file(filename):
    return send_file(os.path.join(IMAGES_DIR, filename)) #sending this file when requests
"""
A list of API 
"""

@app.route('/upload-image', methods=["POST", "GET"])
def upload_image():
    if request.method == "POST":
        try: # Making sure that the server won't get an error
            image = request.files["file"]
            image.save(os.path.join(PLACEHOLDING_DATA_DIR, "Success.jpeg"))
            return "Success" # All is well
        except Exception as e: # Error processing file
            return f"Error Processing it Error {e}"
    else:
        return "<h1> Invalid Request </h1>"

@app.route('/neural-style-transfere', methods = ["POST", "GET"])
def get_style_picture():
    """

    :return:
    """
    if request.method == "POST":
        style_dir = os.path.join(PLACEHOLDING_DATA_DIR, f"{time.time()}.jpeg")
        request.files["style-image"].save(style_dir)

        original_dir = os.path.join(PLACEHOLDING_DATA_DIR, f"{time.time()}.jpeg")
        request.files["original-image"].save(original_dir)

        filename = save_neural_style_model(original_dir, style_dir)
        file_link = f"{DOMAIN}/file/image/{urllib.parse.quote(filename)}" # Url encoding
        return file_link
    return "<h1> Not Workign </h1>"

@app.route('/new-style-post', methods=["POST", "GET"])
def upload_style_to_database():
    if request.method == "POST":
        json_data = request.get_json()  # Getting the json data
        is_private, title, tags, accoundId, captions, imagelink = json_data['isPrivate'],  json_data['title'], json_data['tags'], json_data['accountId'], json_data['captions'], json_data['imageLink']
        timestamp, made_with, filename = f"{time.time()}", "Neural Style Transfer", get_filename_from_neural_transfer_link(imagelink)
        cursor.execute(
            "INSERT INTO Posts (accountId, timestamp, madeWith, fileLocation, title, captions, isPrivate) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (accoundId, timestamp, made_with, filename, title, captions,
             is_private))  # Uploading everything except tag
        postId = cursor.lastrowid

        cursor.execute("INSERT INTO Tags (postId, tag1, tag2, tag3) VALUES (%s, %s, %s, %s)",
                       (postId, tags[0], tags[1], tags[2]))  # Uploading tags

        db.commit() # Save Changes
        return "<h1> It Worked </h1>"

    return "<h1> Invalid Request Method </h1>"
api.add_resource(GetPostsFromUser, "/api/get-posts-from-user/<int:id>")
api.add_resource(GetOwnUserPosts, "/api/get-own-post/<int:id>")
api.add_resource(GetRecentPost, "/api/get-recent-posts")

if __name__ == "__main__":
    app.run()  # Running the app
