from datetime import datetime
from math import ceil
from flask import request
from models.order import Order
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity
from flask_restful import Resource, reqparse, fields
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


class OrderConvention(Resource):
    @admin_validator()
    def get(self):
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


class OrderActions(Resource):
    @jwt_required()
    def get(self, _id):
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            return order, 200
        return {'error': {'message': 'Order Not Found'}}, 404

    @jwt_required()
    def delete(self, _id):
        order_id = ObjectId(_id)
        order = Order.find_one({'_id': order_id})
        if order:
            Order.delete_one(order)
            return {'message': 'Order Deleted Successfully'}, 200
        return {'error': 'Order Not Found'}, 404


class OrderSummary(Resource):
    @admin_validator()
    def get(self):
        pass


class UserOrder(Resource):
    @jwt_required()
    def get(self):
        page = int(request.args.get('pageNumber') or 1)
        user_id = ObjectId(get_jwt_identity()['_id'])
        count = Order.count_documents({'user': user_id})
        order_list = Order.find({'user': user_id})\
            .sort('createdAt', -1)\
            .skip(PAGE_SIZE * (page-1))\
            .limit(PAGE_SIZE)
        return {
            'orders': list(order_list),
            'page': page,
            'pages': ceil(count / PAGE_SIZE)
        }, 200


