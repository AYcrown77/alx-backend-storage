#!/usr/bin/env python3
"""returns the list of school having a specific topic"""


def schools_by_topic(mngo_collection, topic):
    """search for the topic and return the school"""
    result_list = mongo_collection.find({'topics': topic})
    return result_list
