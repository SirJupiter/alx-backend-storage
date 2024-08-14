#!/usr/bin/env python3
"""Module"""

from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    collection = client.logs.nginx

    number_of_documents = collection.estimated_document_count()

    print(f"{number_of_documents} logs")
    print('Methods:')
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    status_check_count = collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    for each_method in methods:
        number = collection.count_documents({'method': each_method})
        print('\tmethod {}: {}'.format(each_method, number))
    print('{} status check'.format(status_check_count))
