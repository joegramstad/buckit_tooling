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


def insert_to_mongo(cur_level, bottom_level, children, list_category, list_type=None, list_owner=None,
                    list_name=None):
    insert_dict = {"currentLevel": cur_level, "bottomLevel": bottom_level, "collectionListCategory": list_category}

    if list_type:
        insert_dict["collectionListType"] = list_type

    if list_owner:
        insert_dict["collectionListOwner"] = list_owner

    if list_name:
        insert_dict["name"] = list_name

    if bottom_level:
        if len(children) == 1:
            children = children[0]
        else:
            insert_dict["filter"] = "year"

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
                owner_hierarchy[collection_name] = []
                collection_identifiers = collection_lists.find({"collectionListCategory": collection_category,
                                                                "collectionListType": collection_type,
                                                                "collectionListOwner": collection_owner,
                                                                "name": collection_name}, {"_id": 1})
                name_children = owner_hierarchy[collection_name]

                for collection_identifier in collection_identifiers:
                    name_children.append(collection_identifier['_id'])

                collection_name_id = insert_to_mongo(4, True, name_children, collection_category, collection_type,
                                                     collection_owner, collection_name)
                owner_children.append(collection_name_id)

            collection_owner_id = insert_to_mongo(3, False, owner_children, collection_category, collection_type,
                                                  collection_owner)
            type_children.append(collection_owner_id)

        collection_type_id = insert_to_mongo(2, False, type_children, collection_category, collection_type)
        category_children.append(collection_type_id)

    collection_category_id = insert_to_mongo(1, False, category_children, collection_category)
    root_children.append(collection_category_id)
insert_to_mongo(0, False, root_children, "root")
