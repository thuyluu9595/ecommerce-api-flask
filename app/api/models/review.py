from app import db

review_validator = {
    '$jsonSchema': {
        "bsonType": "object",
        "required": ["user", "product", "rating", "timestamp"],
        "properties": {
            "user": {
                "bsonType": "objectId",
                "description": "must be a ObjectId type and is required"
            },
            "product": {
                "bsonType": "objectId",
                "description": "must be a ObjectId type and is required"
            },
            "rating": {
                "bsonType": "double",
                "description": "rating score is required"
            },
            "comment": {
                "bsonType": "string",
                "description": "comment must be a string"
            },
            "timestamp": {
                "bsonType": "date",
                "description": "date is required"
            }
        }
    }
}

try:
    db.create_collection("Review")
except Exception as e:
    pass

db.command("collMod", "Review", validator=review_validator)
Review = db.Review
