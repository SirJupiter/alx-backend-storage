#!/usr/bin/env python3
"""Module"""


def insert_school(mongo_collection, **kwargs):
    """Function inserts a new document in a collection based on kwargs

    Args:
        mongo_collection: the pymongo collection object
        kwargs: key-value pairs to be inserted

    Returns:
        The new _id
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
