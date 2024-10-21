#!/usr/bin/env python3
''' List all documents in Python '''


def list_all(mongo_collection):
    '''list all'''
    all_documents = list(mongo_collection.find())
    return all_documents
