import pymongo

def insert_post(data, se_mongo_host, se_mongo_port):
    try:
        client = pymongo.MongoClient(se_mongo_host,se_mongo_port)
        db = client.servers_data
        table = db.serverData_tbl
        post_id = table.insert_one(data).inserted_id
    except ConnectionError:
        print('Couldn\'t connect to MongoDB. Check if \'mongod\' is running\n')
    
    