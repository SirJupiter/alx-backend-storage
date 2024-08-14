#!/usr/bin/env python3
"""Module"""


def list_all(mongo_collection):
    """lists all documents in a collection"""
    collection = mongo_collection.find()
    if not collection:
        return []
    return collection
