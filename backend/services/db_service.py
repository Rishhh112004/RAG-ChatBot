from pymongo import MongoClient
from datetime import datetime

class DBService:

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["rag_chatbot"]
        self.collection = self.db["paragraphs"]
        self.sessions = self.db["sessions"]
        self.messages = self.db["messages"]

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
    
    def create_session(self):
        session = {
            "created_at": datetime.now()
        }
        result = self.sessions.insert_one(session)
        return str(result.inserted_id)


    def save_message(self, session_id, question, answer):
        from bson import ObjectId
        self.messages.insert_one({
            "session_id": ObjectId(session_id),
            "question": question,
            "answer": answer,
            "timestamp": datetime.now()
        })


    def get_sessions(self):
        return list(self.sessions.find().sort("created_at", -1))


    def get_messages(self, session_id):
        from bson import ObjectId
        return list(self.messages.find({
            "session_id": ObjectId(session_id)
        }).sort("timestamp", 1))


    def delete_session(self, session_id):
        from bson import ObjectId
        sid = ObjectId(session_id)
        self.sessions.delete_one({"_id": sid})
        self.messages.delete_many({"session_id": sid})
        
    def get_sessions_with_titles(self):
        sessions = list(self.sessions.find().sort("created_at", -1))

        result = []

        for session in sessions:
            first_message = self.messages.find_one(
                {"session_id": session["_id"]},
                sort=[("timestamp", 1)]
            )

            if first_message:
                title = first_message["question"][:50]
            else:
                title = "New Chat"

            result.append({
                "id": str(session["_id"]),
                "title": title
            })

        return result    