"""
ALL of the api object will be stored here
"""
from flask_restful import Resource, Api
from constants import db, cursor # Accessing database

class GetPostsFromUser(Resource): # Return all the posts from a given user
    num_amount_posts = 10
    def get_sql_command(self, id):
        return f"SELECT postId, accountId, timestamp, madeWith, filelocation, title, captions, likes, isPrivate FROM Posts WHERE accountId={id}"

    def get(self, id):
        """

        :param id: uesr id that referes to the database
        :return: Json object that has a list of posts
        """
        cursor.execute(self.get_sql_command(id))
        posts = []
        for element in cursor:
            posts.append({
                "postId" : element[0],
                "accountId": element[1],
                "timestamp": element[2],
                "madeWith": element[3],
                "filelocation": element[4], # This would be get url link in the future
                "title": element[5],
                "likes": element[6],
                "isPrivate": element[7],
            })

        return {"Posts" : posts}

class GetPosts(Resource):
    def get(self):
        """

        :return: A list of random posts
        """
        return {"success" : "True"}

