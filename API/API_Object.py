"""
ALL of the api object will be stored here
"""
import urllib.parse
from flask_restful import Resource
from constants import cursor, DOMAIN  # Accessing database


class GetPostsFromUser(Resource):  # Return all the posts from a given user
    num_amount_posts = 10

    def get_sql_command(self, id):
        """

        :param id: user id
        :return: sql data command
        """
        return f"SELECT postId, accountId, timestamp, madeWith, filelocation, title, captions, likes, isPrivate FROM Posts WHERE accountId={id}"

    def get(self, id):
        """

        :param id: uesr id that referes to the database
        :return: Json object that has a list of posts
        """
        cursor.execute(self.get_sql_command(id))
        posts = []
        for element in cursor:
            if element[8] == 0:
                posts.append({
                    "postId": element[0],
                    "accountId": element[1],
                    "timestamp": element[2],
                    "madeWith": element[3],
                    "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                    # This would be get url link in the future
                    "title": element[5],
                    "Captions": element[6],
                    "likes": element[7],
                    "isPrivate": element[8]
                })

        return {"Posts": posts}


class GetOwnUserPosts(Resource):
    def get_sql_command(self, id):
        """

        :param id: user id
        :return: sql data command
        """
        return f"SELECT postId, accountId, timestamp, madeWith, filelocation, title, captions, likes, isPrivate FROM Posts WHERE accountId={id}"

    def get(self, id):
        """

        :return: A list of random posts
        """
        cursor.execute(self.get_sql_command(id))
        posts = []
        for element in cursor:
            posts.append({
                "postId": element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                # This would be get url link in the future
                "title": element[5],
                "Captions": element[6],
                "likes": element[7],
                "isPrivate": element[8]
            })

        return {"Posts": posts}


class GetRecentPost(Resource):
    Q1 = "SELECT * FROM POSTS WHERE isPrivate=0"

    def get(self):
        cursor.execute(self.Q1)
        posts = []
        for element in cursor:
            posts.append({
                "postId": element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                # This would be get url link in the future
                "title": element[5],
                "Captions": element[6],
                "likes": element[7],
                "isPrivate": element[8]
            })
        return {"Posts": posts}


class Trending(Resource):
    Q1 = "SELECT * FROM POSTS WHERE isPrivate=0"

    def get(self):
        cursor.execute(self.Q1)
        posts = []
        count = 0
        for element in cursor:
            posts.append({
                "postId": element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                # This would be get url link in the future
                "title": element[5],
                "Captions": element[6],
                "likes": element[7],
                "isPrivate": element[8]
            })
            count += 1
            if count == 6:
                break

        return {"Posts": posts}


class ExplorePage(Resource):
    Q1 = "SELECT * FROM POSTS WHERE isPrivate=0"

    def get(self):
        cursor.execute(self.Q1)
        trending = []
        others = []
        count = 0
        for element in cursor:
            trending.append({
                "postId": element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                # This would be get url link in the future
                "title": element[5],
                "Captions": element[6],
                "likes": element[7],
                "isPrivate": element[8]
            })
            count += 1
            if count == 6:
                break

        cursor.execute(self.Q1)
        for element in cursor:
            others.append({
                "postId": element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "post_image_url": f"{DOMAIN}/file/image/{urllib.parse.quote(element[4])}",
                # This would be get url link in the future
                "title": element[5],
                "Captions": element[6],
                "likes": element[7],
                "isPrivate": element[8]
            })
        return {"Others": others,
                "Trending": trending}
