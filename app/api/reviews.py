from datetime import datetime
from .models.review import Review
from .models.product import Product
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from .decorators import admin_validator


_parser = reqparse.RequestParser()
_parser.add_argument('rating', type=float)
_parser.add_argument('comment', type=str)


# /api/reviews/user
class UserReview(Resource):
    @jwt_required()
    def get(self):
        _id = ObjectId(get_jwt_identity()['_id'])
        review_list = Review.find({'user': _id})
        if len(review_list) != 0:
            for review in review_list:
                review['_id'] = str(review['_id'])
                review['user'] = {}
                review['product'] = {}
            return list(review_list), 200
        return {'error': {'message': 'Error'}}, 404


# /api/reviews/product/{id}
class ProductReview(Resource):
    @jwt_required()
    def get(self, _id):
        product_id = ObjectId(_id)
        reviews = Review.find({'product': product_id})
        if len(reviews) != 0:
            for review in reviews:
                review['_id'] = str(review['_id'])
                review['user'] = {}
                review['product'] = {}
            return list(reviews), 200
        return {'error': {'message': 'Error'}}, 404


# /api/reviews/user/{id}
class UserReviewForAdmin(Resource):
    @admin_validator()
    def get(self, _id):
        _id = ObjectId(_id)
        reviews = Review.find({'user': _id})
        if len(reviews) != 0:
            for review in reviews:
                review['_id'] = str(review['_id'])
                review['user'] = {}
                review['product'] = {}
            return list(reviews), 200
        return {'error': {'message': 'Error'}}, 404


# /api/reviews/{id}
class ReviewActions(Resource):
    @jwt_required()
    def post(self, _id):
        """
        Create a review by using product id
        """
        product_id = ObjectId(_id)
        product = Product.find_one({'_id': product_id})
        if product:
            user_id = get_jwt_identity()['_id']
            data = _parser.parse_args()
            creating_review = {
                'user': user_id,
                'product': product_id,
                'rating': data['rating'],
                'comment': data['comment'],
                'timestamp': datetime.now()
            }
            Review.create_one(creating_review)
            return {}, 200
        return {'error': {'message': 'Error'}}, 404

    @jwt_required()
    def put(self, _id):
        review_id = ObjectId(_id)
        review = Review.find_one({'_id': review_id})
        if review:
            data = _parser.parse_args()
            Review.update_one(review, {
                '$set': {
                    'rating': data['rating'],
                    'comment': data['comment']
                }
            })
            return {}, 200
        return {'error': {'message': 'Error'}}, 404

    @jwt_required()
    def delete(self, _id):
        review_id = ObjectId(_id)
        review = Review.find_one({'_id': review_id})
        if review:
            Review.delete_one(review)
            return {}, 200
        return {'error': {'message': 'Error'}}, 404




