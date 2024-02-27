import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

class MongoDB():
    def __init__(self):
        self.client = pymongo.MongoClient(os.getenv("MONGO_HOST"))
        self.db = self.client[os.getenv("MONGO_DATABASE")]
        self.model = self.db[os.getenv("MONGO_COLLECTION")]

    def create_data(self, data=None):
        try:
            if data is None:
                return TypeError("data must be list or dict")
            if type(data) is list:
                return self.model.insert_many(data)
            else:
                return self.model.insert_one(data)
        except Exception as e:
            print(f"create_data error: {e}")

    def read_data(self, conditions=None):
        try:
            return list(self.model.find(conditions))
        except Exception as e:
            print(f"get_data error: {e}")

    def update_date(self, data=None, conditions=None, is_update_many=True):
        try:
                
            if (type(data) is dict and type(conditions) is dict):
                if is_update_many:
                    return self.model.update_many(conditions, { "$set": data })
                else:
                    return self.model.update_one(conditions, { "$set": data })
            else:
                return TypeError("data and conditions must be both dict")
        except Exception as e:
            print(f"update_date error: {e}")

    def delete_data(self, conditions=None):
        try:
            if conditions is None:
                return self.model.delete_many({})
            
            if type(conditions) is list:
                return self.model.delete_many(conditions)
            else:
                return self.model.delete_one(conditions)
        except Exception as e:
            print(f"delete_data error: {e}")
