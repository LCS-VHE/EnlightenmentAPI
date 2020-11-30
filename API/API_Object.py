"""
ALL of the api object will be stored here
"""
from flask_restful import Resource, Api
from constants import db, cursor # Accessing database

class GetPostsFromUser(Resource): # Return all the posts from a given user
    num_amount_posts = 10

    def get(self, id):
        """

        :param id: uesr id that referes to the database
        :return: Json object that has a list of posts
        """
        return {"Success" : id}

class GetPosts(Resource):
    def get(self):
        """

        :return: A list of random posts
        """
        return {"success" : "True"}

