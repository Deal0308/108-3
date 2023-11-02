import pymongo

me={
    "first_name":"Cody",
    "last_name":"Deal",
    "email": "Deal0308@yahoo.com",
    "github": "Deal0308",
}

con_str ="mongodb+srv://deal0308:gontot-2Gujqe-hawzyj@cluster0.my4yn0v.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_str)
db = client.test
