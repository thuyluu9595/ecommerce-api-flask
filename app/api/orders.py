from datetime import datetime
from math import ceil
from flask import request
from models.order import Order
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from bson.objectid import ObjectId
from authentication import admin_validator
from constants import PAGE_SIZE

_parser = reqparse.RequestParser()
_parser.add_argument('orderItems', type=list, required=True, location='json')
_parser.add_argument('shippingAddress', type=dict, required=True)
_parser.add_argument('paymentMethod', type=str, required=True)
_parser.add_argument('itemsPrice', type=float, required=True)
_parser.add_argument('shippingPrice', type=float, required=True)
_parser.add_argument('taxPrice', type=float, required=True)
_parser.add_argument('totalPrice', type=float, required=True)
_parser.add_argument('paymentResult', type=dict, required=True)


# /api/orders/
class OrderConvention(Resource):
    @admin_validator()
    def get(self):
        """
        Get a list of all orders
        """
        orders = Order.find()
        return {'order': list(orders)}, 200

    @jwt_required()
    def post(self):
        data = _parser.parse_args()

        identity = get_jwt_identity()
        _id = identity['_id']
        data['user'] = _id

        additional_data = {
            "timestamps": datetime.now(),
            "isDelivered": False,
            "requestCancel": False,
            "isCanceled": False
        }
        order = Order.insert_one({**data, **additional_data})
        return {'message': 'Successfully Placed Order'}, 201


# /api/orders/{id}/
class OrderActions(Resource):
    @jwt_required()
    def get(self, _id):
        """
        Get order by id
        """
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            return order, 200
        return {'error': {'message': 'Order Not Found'}}, 404

    @jwt_required()
    def delete(self, _id):
        """
        Delete order belong to given id
        """
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            Order.delete_one(order)
            return {'message': 'Order Deleted Successfully'}, 200
        return {'error': 'Order Not Found'}, 404


# /api/orders/summary/
class OrderSummary(Resource):
    @admin_validator()
    def get(self):
        """
        Get a summary of orders
        """
        users = Order.aggregate([
            {
                "$group": {"_id": None, "numUsers": {"$sum": 1}}
            }
        ])
        orders = Order.aggregate([
            {
                "$group": {
                    "_id": None,
                    "numOrders": {"$sum": 1},
                    "totalSale": {"$sum": "totalPrice"}
                }
            }
        ])
        dailyOrders = Order.aggregate([
            {
                "$group": {
                    "_id": {"dateToString": {"format": '%Y-%m-%d', "date": "createdAt"}},
                    "orders": {"$sum": 1},
                    "sales": {"$sum": "totalPrice"}
                }
            }
        ])
        productCategories = Order.aggregate([
            {
                "$group": {
                    "_id": "$category",
                    "count": {"$sum": 1}
                }
            }
        ])

        return {
            'users': users,
            'orders': orders,
            'dailyOrders': dailyOrders,
            'productCategories': productCategories
        }, 200


# /api/orders/mine/
class GetUserOrder(Resource):
    @jwt_required()
    def get(self):
        page = int(request.args.get('pageNumber') or 1)
        user_id = ObjectId(get_jwt_identity()['_id'])
        count = Order.count_documents({'user': user_id})
        order_list = Order.find({'user': user_id}) \
            .sort('createdAt', -1) \
            .skip(PAGE_SIZE * (page - 1)) \
            .limit(PAGE_SIZE)
        return {
                   'orders': list(order_list),
                   'page': page,
                   'pages': ceil(count / PAGE_SIZE)
               }, 200


# /api/orders/user/{id}/
class GetOrderById(Resource):
    @jwt_required()
    def get(self, _id):
        user_id = ObjectId(_id)
        orders = Order.find({'user': user_id})
        order_list = list(orders)
        if orders:
            return {'count': len(order_list), 'orders': order_list}, 200
        return {'error': {'message': 'Error'}}, 404


# /{id}/deliver/
class DeliverOrder(Resource):
    @admin_validator()
    def put(self, _id):
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            Order.update_one(order, {
                '$set': {
                    'isDelivered': True,
                    'deliveredAt': datetime.now()
                }
            })
            return {}, 200
        return {'error': {'message': 'Error'}}, 404


# /{id}/cancelrequest/
class OrderCancellation(Resource):
    @jwt_required()
    def put(self, _id):
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            Order.update_one(order, {
                '$set': {
                    'requestCancel': True,
                    'requestAt': datetime.now()
                }
            })
            return {}, 200
        return {'error': {'message': 'Error'}}, 404


# /{id}/canceled/
class ConfirmCancellation(Resource):
    @admin_validator()
    def put(self, _id):
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            Order.update_one(order, {
                '$set': {
                    'isCanceled': True,
                    'canceledAt': datetime.now()
                }
            })
            return {}, 200
        return {'error': {'message': 'Error'}}, 404
