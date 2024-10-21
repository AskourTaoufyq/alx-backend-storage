#!/usr/bin/env python3
''' Insert a document in Python '''


def insert_school(mongo_collection, **kwargs):
    ''' insert documnt into school '''
    res = mongo_collection.insert_one(kwargs)
    return res.inserted_id
