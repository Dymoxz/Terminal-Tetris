import pymongo
from pymongo import MongoClient



cluster = MongoClient("mongodb+srv://210250:Bakkerijdymo420@cluster0.d1df6mp.mongodb.net/?retryWrites=true&w=majority")

database = cluster["Tetris"]
collection = database["score"]



id = 0
while id < 5:
    score = int(input("Score: "))
    post = {
        "_id": id,
        "score": score
    }
    print(post)
    print(id)
    collection.insert_one(post)
    id += 1
    post.clear()

# delete_collection = collection.delete_one({"_id": 0})
