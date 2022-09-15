from app import db
order_validator = {
    '$jsonSchema': {
        "bsonType": "object",
        "required": ["orderItems", "shippingAddress", "paymentMethod", "itemsPrice",
                     "shippingPrice", "taxPrice", "totalPrice", "isDelivered", "user",
                     "timestamps"],
        "properties": {
            "orderItems": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["name", "qty", "image", "price", "product"],
                    "properties": {
                        "name": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "qty": {
                            "bsonType": "int",
                            "minimum": 1,
                            "description": "must be an integer greater than 0"
                        },
                        "image": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "price": {
                            "bsonType": ["decimal", "int", "double"],
                            "minimum": 0,
                            "description": "must be an double greater than 0"
                        },
                        "product": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "options": {
                            "bsonType": "object"
                        }
                    }
                }
            },
            "shippingAddress": {
                "bsonType": "object",
                "required": ["fullname", "address", "city", "postalCode", "country"],
                "properties": {
                    "fullname": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "address": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "city": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "postalCode": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "country": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    }
                }
            },
            "paymentMethod": {
                "enum": ["PayPal", "Stripe"],
                "description": "can only be one of the enum values and is required"
            },
            "paymentResult": {
                "bsonType": "object",
                "required": ["id", "status", "update_time", "email_address"],
                "properties": {
                    "id": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "status": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "update_time": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "email_address": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    }
                }
            },
            "itemsPrice": {
                "bsonType": ["decimal", "int", "double"],
                "minimum": 0,
                "description": "must be a double greater than 0 and is required"
            },
            "shippingPrice": {
                "bsonType": ["decimal", "int", "double"],
                "minimum": 0,
                "description": "must be a double greater than 0 and is required"
            },
            "taxPrice": {
                "bsonType": ["decimal", "int", "double"],
                "minimum": 0,
                "description": "must be a double greater than 0 and is required"
            },
            "totalPrice": {
                "bsonType": ["decimal", "int", "double"],
                "minimum": 0,
                "description": "must be a double greater than 0 and is required"
            },
            "user": {
                "bsonType": "objectId",
                "description": "must be a objectID and is required"
            },
            "isDelivered": {
                "bsonType": "bool",
                "description": "must be a boolean and is required"
            },
            "deliveredAt": {
                "bsonType": "date",
                "description": "must be a date"
            },
            "requestCancel": {
                "bsonType": "bool",
                "description": "must be a boolean"
            },
            "requestedAt": {
                "bsonType": "date",
                "description": "must be a date"
            },
            "reasonCancel": {
                "bsonType": "string",
                "description": "must be a string"
            },
            "isCanceled": {
                "bsonType": "bool",
                "description": "must be a boolean"
            },
            "canceledAt": {
                "bsonType": "date",
                "description": "must be a date"
            },
            "timestamps": {
                "bsonType": "date",
                "description": "must be a date and is required"
            }
        }
    }
}

try:
    db.create_collection("Order")
except Exception as e:
    pass

db.command("collMod", "Order", validator=order_validator)
Order = db.Order
