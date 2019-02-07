from pymongo import MongoClient


def remove_fields_from_test_data(dict_):
    del dict_['_id']

    return dict_


def set_test_database_data(collection, obj):
    client = MongoClient('localhost', 27017)
    db = client['school']
    db[collection].insert(obj)
    client.close()


def clear_test_database(collection):
    client = MongoClient('localhost', 27017)
    db = client['school']
    db[collection].drop()
    client.close()
