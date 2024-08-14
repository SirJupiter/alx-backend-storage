#!/usr/bin/env python3
"""Module"""


def schools_by_topic(mongo_collection, topic):
    """Fucntion that returns the list of school having a specific topic

    Args:
        mongo_collection: the pymongo collection object
        topic: (string) the topic searched

        Returns:
            (list) the list of school having a specific topic
    """
    return mongo_collection.find({'topics': {'$elemMatch': {'$eq': topic}}})
