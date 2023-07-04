import sys
from pymongo import MongoClient

URI = "mongodb://localhost:27017/buckit"
DB = "buckit"

SOURCE_COLLECTION = "collectionLists"
DEST_COLLECTION = "hierarchy"
LEVELS = ["collectionListCategory", "collectionListType", "collectionListOwner", "name"]

client = MongoClient(URI)
db = client[DB]
collection_lists = db[SOURCE_COLLECTION]
# hierarchy = db[DEST_COLLECTION]

master_hierarchy = {}

collection_categories = collection_lists.find().distinct("collectionListCategory")
for collection_category in collection_categories:
    master_hierarchy[collection_category] = {}
    collection_types = collection_lists.find({"collectionListCategory": collection_category}).distinct(
        "collectionListType")
    category_hierarchy = master_hierarchy[collection_category]
    for collection_type in collection_types:
        category_hierarchy[collection_type] = {}
        collection_owners = collection_lists.find({"collectionListCategory": collection_category,
                                                   "collectionListType": collection_type}).distinct(
            "collectionListOwner")
        type_hierarchy = category_hierarchy[collection_type]
        for collection_owner in collection_owners:
            type_hierarchy[collection_owner] = {}
            collection_names = collection_lists.find({"collectionListCategory": collection_category,
                                                      "collectionListType": collection_type,
                                                      "collectionListOwner": collection_owner}).distinct("name")
            owner_hierarchy = type_hierarchy[collection_owner]
            for collection_name in collection_names:
                owner_hierarchy[collection_name] = {}
                collection_identifiers = collection_lists.find({"collectionListCategory": collection_category,
                                                        "collectionListType": collection_type,
                                                        "collectionListOwner": collection_owner,
                                                        "name": collection_name}, {"_id": 1, "year": 1})
                name_hierarchy = owner_hierarchy[collection_name]
                for collection_identifier in collection_identifiers:
                    name_hierarchy[collection_identifier['year']] = collection_identifier['_id']
                    print(collection_category, collection_type, collection_owner, collection_name, collection_identifier['year'], collection_identifier['_id'])

print(master_hierarchy)
