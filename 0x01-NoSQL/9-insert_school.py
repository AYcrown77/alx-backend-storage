#!/usr/bin/env python3
"""inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Returns the new _id"""
    new = mongo_collection.insertOne(kwargs)
    return new.get('_id')
