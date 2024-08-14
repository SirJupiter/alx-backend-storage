#!/usr/bin/env python3
"""Module"""


def update_topics(mongo_collecton, name, topics):
    """
    Function changes all topics of a school document based on the name

    Args:
        mongo_collection: the pymongo collection object
        name: (string) the school name to update
        topics: (list of strings) the list of topics approached in the school

    Returns:
        Nothing
    """
    mongo_collecton.update_many({"name": name}, {'$set': {"topics": topics}})
