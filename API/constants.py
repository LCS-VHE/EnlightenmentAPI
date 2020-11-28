import os
import mysql.connector
from CRED import PASSWORD

IMAGES_DIR = os.path.join(os.curdir, "Data", "images")
PLACEHOLDING_DATA_DIR = os.path.join(os.curdir, "Data", "PlaceHoldingData")
db = mysql.connector.connect(
    user='root',
    password=PASSWORD,
    host='localhost',
)
cursor = db.cursor()