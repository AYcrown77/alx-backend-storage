#!/usr/bin/env python3
"""function that lists all documents in a collection"""


def  list_all(mongo_collection):
    """returns the list  of documents"""
    list_result = mongo_collection.find({})
    return list_result
