
from unittest import TestCase

import mongomock

class MongoMockTest(TestCase):

    def setUp(self):
        self.client = mongomock.MongoClient()

    def test_mongoclient(self):
        self.assertIsNotNone(self.client)
        self.assertIsNotNone(mongomock.MongoClient('mongo://localhost'))


    def test_database(self):
        mongoDB = self.client.TEST
        self.assertIsNotNone(mongoDB)
        self.assertIs(mongoDB, self.client.TEST)
        self.assertIs(mongoDB, self.client['TEST'])

    def test_insert_find(self):
        mongoDB = self.client.TEST
        collection = mongoDB.test_insert_find

        insert_id = collection.insert({'one':'two'})
        result = collection.find_one({"_id": insert_id})

        self.assertIsNotNone(result.get('one'))
        self.assertEqual('two', result.get('one'))

    def test_delete(self):
        mongoDB = self.client.TEST
        collection = mongoDB.test_insert_find
        insert_id = collection.insert({'one':'two'})
        result = collection.find_one({"_id": insert_id})

        self.assertIsNotNone(result.get('one'))
        self.assertEqual('two', result.get('one'))
        self.assertIsNotNone(collection.find_one({"_id": insert_id}))

        collection.delete_one({"_id": insert_id})

        self.assertIsNone(collection.find_one({"_id": insert_id}))

    def test_update(self):
        mongoDB = self.client.TEST
        collection = mongoDB.test_insert_find
        insert_id = collection.insert({'one':'two'})
        result = collection.find_one({"_id": insert_id})

        self.assertIsNotNone(result.get('one'))
        self.assertEqual('two', result.get('one'))

        collection.update_one({
          '_id': insert_id
        },{
          '$set': {
            'one': 'three'
          }
        }, upsert=False)

        result = collection.find_one({"_id": insert_id})

        self.assertEqual('three', result.get('one'))
