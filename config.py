import pymongo
import certifi

me={
    "first_name":"Cody",
    "last_name":"Deal",
    "email": "Deal0308@yahoo.com",
    "github": "Deal0308",
}

con_str ="mongodb+srv://deal0308:nyrwyx-tavjyh-Tigti2@cluster0.my4yn0v.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str, tlsCAFile=certifi.where())
db = client.get_database("supplement_store")

catalog = db['products']