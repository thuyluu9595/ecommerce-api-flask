from app import db
product_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Product Object Validation",
        "required": ["name", "image", "brand", "category", "description", "price", "countInStock", "rating",
                     "numReviews", "attribute"],
        "properties": {
            "name": {
                "bsonType": "string",
                "description": "'name' must be a string and is required"
            },
            "image": {
                "bsonType": "string"
            },
            "brand": {
                "bsonType": "string"
            },
            "category": {
                "bsonType": "string"
            },
            "description": {
                "bsonType": "string"
            },
            "price": {
                "bsonType": "double"
            },
            "countInStock": {
                "bsonType": "int"
            },
            "rating": {
                "bsonType": "double"
            },
            "numReviews": {
                "bsonType": "int"
            },
            "attribute": {
                "bsonType": ["array"],
                "items": {
                    "bsonType": "object",
                    "required": ["name", "options"],
                    "properties": {
                        "name": {
                            "bsonType": "string"
                        },
                        "options": {
                            "bsonType": "string"
                        }
                    }
                }
            }
        }
    }
}
try:
    db.create_collection("Product")
except Exception as e:
    pass

db.command("collMod", "Product", validator=product_validator)
Product = db.Product
