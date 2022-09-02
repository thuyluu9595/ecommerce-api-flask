from app import db
user_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "User Object Validation",
        "required": ["email", "name", "password", "isAdmin"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "'name' must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "description": "'email' is required"
            },
            "password": {
                "bsonType": "string",
                "description": "password"
            },
            "isAdmin": {
                "bsonType": "string",
                "description": "isAdmin"
            }
        }
    }
}
try:
    db.create_collection("User")
except Exception as e:
    pass

db.command("collMod", "User", validator=user_validator)
User = db.User
