from constants import cursor
import mysql.connector

Q1 = "CREATE DATABASE EnlightenmentApi" # Create a database
Q2 = "CREATE TABLE Posts (postId INT PRIMARY KEY AUTO_INCREMENT, accountId INT, timestamp INT, madeWith VARCHAR(100), fileLocation VARCHAR(300), title VARCHAR(300), captions VARCHAR(500), likes INT DEFAULT 0, isPrivate BOOL)" # Table one
Q3 = "CREATE TABLE Tags (postId INT, FOREIGN KEY(postId) REFERENCES Posts(postId), tag1 VARCHAR(100), tag2 VARCHAR(100), tag3 VARCHAR(100 ))" # Table two
Q4 = "CREATE TABLE Accounts (accountId INT PRIMARY KEY AUTO_INCREMENT, accountName VARCHAR(100), accountPassword VARCHAR(100), posts INT DEFAULT 0)"
Q5 = "DROP TABLE Accounts"
cursor.execute(Q2)
cursor.execute(Q3)
cursor.execute(Q4)

cursor.execute("DESCRIBE Posts")
for x in cursor:
    print(x)

cursor.execute("DESCRIBE Tags")
for x in cursor:
    print(x)
