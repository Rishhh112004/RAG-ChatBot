from pymongo import MongoClient
from datetime import datetime


class DBService:

    def __init__(self):

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["rag_chatbot"]
        self.collection = self.db["paragraphs"]

    def insert_paragraph(self, text):

        self.collection.insert_one({
            "text": text,
            "timestamp": datetime.now()
        })

    def get_all_paragraphs(self):

        return list(self.collection.find())

    def delete_paragraphs(self, ids):

        from bson import ObjectId

        object_ids = [ObjectId(i) for i in ids]

        self.collection.delete_many({
            "_id": {"$in": object_ids}
        })

    def clear_all(self):

        self.collection.delete_many({})