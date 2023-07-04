from pprint import pprint

from pymongo import MongoClient

URI = "mongodb://localhost:27017/buckit"
DB = "buckit"

SOURCE_COLLECTION = "collectionLists"
DEST_COLLECTION = "hierarchy"
LEVELS = ["collectionListCategory", "collectionListType", "collectionListOwner", "name"]

client = MongoClient(URI)
db = client[DB]
collection_lists = db[SOURCE_COLLECTION]
hierarchy = db[DEST_COLLECTION]

master_hierarchy = {}
root_children = []
collection_categories = collection_lists.find().distinct("collectionListCategory")


def insert_to_mongo(name, bottom_level, children):
    insert_dict = {
        "name": name,
        "bottomLevel": bottom_level
    }
    if bottom_level:
        insert_dict["collectionListChildren"] = children
    else:
        insert_dict["children"] = children

    db_response = hierarchy.insert_one(insert_dict)
    return db_response.inserted_id


for collection_category in collection_categories:
    master_hierarchy[collection_category] = {}
    collection_types = collection_lists.find({"collectionListCategory": collection_category}).distinct(
        "collectionListType")
    category_hierarchy = master_hierarchy[collection_category]
    category_children = []
    for collection_type in collection_types:
        category_hierarchy[collection_type] = {}
        collection_owners = collection_lists.find({"collectionListCategory": collection_category,
                                                   "collectionListType": collection_type}).distinct(
            "collectionListOwner")
        type_hierarchy = category_hierarchy[collection_type]
        type_children = []
        for collection_owner in collection_owners:
            type_hierarchy[collection_owner] = {}
            collection_names = collection_lists.find({"collectionListCategory": collection_category,
                                                      "collectionListType": collection_type,
                                                      "collectionListOwner": collection_owner}).distinct("name")
            owner_hierarchy = type_hierarchy[collection_owner]
            owner_children = []
            for collection_name in collection_names:
                # owner_hierarchy[collection_name] = {}
                owner_hierarchy[collection_name] = []
                collection_identifiers = collection_lists.find({"collectionListCategory": collection_category,
                                                                "collectionListType": collection_type,
                                                                "collectionListOwner": collection_owner,
                                                                "name": collection_name}, {"_id": 1, "year": 1})
                name_children = owner_hierarchy[collection_name]
                for collection_identifier in collection_identifiers:
                    name_children.append(collection_identifier['_id'])
                    # name_hierarchy[collection_identifier['year']] = collection_identifier['_id']


                collection_name_id = insert_to_mongo(collection_name, True, name_children)
                owner_children.append(collection_name_id)

            collection_owner_id = insert_to_mongo(collection_owner, False, owner_children)
            type_children.append(collection_owner_id)

        collection_type_id = insert_to_mongo(collection_type, False, type_children)
        category_children.append(collection_type_id)

    collection_category_id = insert_to_mongo(collection_category, False, category_children)
    root_children.append(collection_category_id)
    print(root_children)
