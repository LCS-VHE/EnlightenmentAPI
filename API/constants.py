import os
import mysql.connector
from CRED import PASSWORD

IMAGES_DIR = os.path.join(os.curdir, "images")
db = mysql.connector.connect(
    user='root',
    password=PASSWORD,
    host='localhost',
)
cursor = db.cursor()