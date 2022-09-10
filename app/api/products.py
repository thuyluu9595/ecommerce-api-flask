from math import ceil
from flask import request
from models.product import Product
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Resource, reqparse, fields
from bson.objectid import ObjectId
from authentication import admin_validator
from constants import PAGE_SIZE


_parser = reqparse.RequestParser()
_parser.add_argument('name', type=str, required=True)
_parser.add_argument('image', type=str, required=True)
_parser.add_argument('price', type=float, required=True)
_parser.add_argument('category', type=str, required=True)
_parser.add_argument('brand', type=str, required=True)
_parser.add_argument('countInStock', type=int, required=True)
_parser.add_argument('attribute', type=list, required=True, location='json')
_parser.add_argument('description', type=str, required=True)


class Products(Resource):
    def get(self):
        args = request.args
        name = args.get("name", type=str) or ''
        category = args.get("category", type=str) or ''
        brand = args.get("brand", type=str) or ''
        order = args.get("order", type=str) or ''
        _min = args.get("min", type=int) or 0
        _max = args.get("max", type=int) or 0
        rating = args.get("rating", type=int) or 0
        page = args.get("pageNumber",type=int) or 1

        name_filter = {"name": {"$regex": name, "$options": 'i'}} if name else {}
        category_filter = {"category": category} if category else {}
        brand_filter = {"brand": brand} if brand else {}
        price_filter = {"price": {"$gte": _min, "$lte": _max}} if _max and _min else {}
        rating_filter = {"rating": {"$gte": rating}} if rating else {}
        sort_order = ["price", 1] if order == "lowest" else \
            ["price", -1] if order == "highest" else \
                ["rating", -1] if order == "toprated" else \
                    ["_id", -1]

        # count matching data
        count = Product.count_documents({
            **name_filter,
            **category_filter,
            **brand_filter,
            **price_filter,
            **rating_filter
        })

        product_list = Product.find({
            **name_filter,
            **category_filter,
            **brand_filter,
            **price_filter,
            **rating_filter
        }) \
            .sort(*sort_order) \
            .skip(PAGE_SIZE * (page - 1)) \
            .limit(PAGE_SIZE)

        return {
                   "products": list(product_list),
                   "page": page,
                   "pages": ceil(count / PAGE_SIZE)
               }, 200

    @admin_validator()
    def post(self):
        data = _parser.parse_args()
        product = Product.insert_one({**data, "rating": 0, "numReviews":0})
        return {}, 200


class ProductActions(Resource):
    def get(self, _id):
        try:
            product_id = ObjectId(_id)
        except Exception as e:
            return {'message': 'Invalid id'}, 401

        product = Product.find_one({"_id": product_id})
        if product:
            return product, 200
        return {'error': {'message': 'Product Not Found'}}, 404

    @admin_validator()
    def put(self, _id):
        try:
            product_id = ObjectId(_id)
        except Exception as e:
            return {'message': 'Invalid id'}, 401

        product = Product.find_one({'_id': product_id})
        if product:
            data = _parser.parse_args()
            product = {**product,**data}
            Product.update_one({'_id': product_id}, {'$set': product})
            return {'message': 'Product Updated Successfully'}, 200
        else:
            return {'error': {'message': 'Product doesnt exist'}}, 404

    @admin_validator()
    def delete(self, _id):
        try:
            product_id = ObjectId(_id)
        except Exception as e:
            return {'message': 'Invalid id'}, 401
        product = Product.find_one({'_id': product_id})
        if product:
            Product.delete_one(product)
            return {'message': 'Product Deleted Successfully'}, 200
        else:
            return {'error': {'message': 'Product doesnt exist'}}, 404


class ProductCategory(Resource):
    pass


class ProductBrands(Resource):
    pass
