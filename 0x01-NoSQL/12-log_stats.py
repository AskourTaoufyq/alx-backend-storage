#!/usr/bin/env python3
''' Log stats '''
from pymongo import MongoClient


def stats_about_nginx_logs(collection):
    ''' stats about Nginx logs '''

    # count documents in nginx collection and print it
    num_collections = collection.count_documents({})
    print(f'{num_collections} logs')

    # count documents in nginx collection for every method and print it
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print('Methods:')
    for method in methods:
        res = collection.count_documents({'method': method})
        print(f'\tmethod {method}: {res}')

    # count status check and print it out
    num_checks = collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    print(f'{num_checks} status check')


if __name__ == '__main__':
    client = MongoClient("mongodb://localhost:27017/")
    db = client.logs
    collection = db.nginx
    stats_about_nginx_logs(collection)
