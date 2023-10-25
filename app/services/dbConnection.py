import os
from pymongo import MongoClient
# import pymongo

client = MongoClient(os.getenv('mongodb+srv://gauravsinghmkp2002:developer7408@cluster0.zqyjc5h.mongodb.net/?retryWrites=true&w=majority'))

db = client.get_database("test123")
# def connect_to_mongodb():
#     try:
#         # Replace "your_connection_string" with your MongoDB Atlas connection string
#         client = pymongo.MongoClient("mongodb+srv://gauravsinghmkp2002:developer7408@cluster0.zqyjc5h.mongodb.net/")
#         db = client.get_database("test123")
#         return db
#     except Exception as e:
#         print(f"Connection to MongoDB Atlas failed: {e}")
#         return None
    