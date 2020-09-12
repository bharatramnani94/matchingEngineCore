from flask import Flask, Blueprint, jsonify, request, abort
from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side, OrderBook
from utility import convert_order_to_json, get_empty_orderbook_json, convert_trades_to_json, convert_orderbook_to_json

route_defs = Blueprint('route_defs', __name__)

lme = LightMatchingEngine()

@route_defs.route('/')
def index():
    return jsonify("Hello Python-Matching-Engine!")

@route_defs.route('/order/<symbol>/<id>', methods=['GET'])
def get_order(symbol, id):
    orderbooks = lme.order_books
    if not orderbooks:
        abort(400)
    orderbook = lme.order_books.get(symbol)
    if not orderbook:
        abort(400)
    for pricepoint, orders in orderbook.bids.items():
        for order in orders:
            if order.order_id == int(id):
                return jsonify(convert_order_to_json(order)), 200
    for pricepoint, orders in orderbook.asks.items():
        for order in orders:
            if order.order_id == int(id):
                return jsonify(convert_order_to_json(order)), 200
    abort(404)

@route_defs.route('/order/create', methods=['POST'])
def create_order():
    if not request.json:
        abort(400)

    symbol = request.json['symbol']
    price = int(request.json['price'])
    quantity = int(request.json['quantity'])
    side = Side.BUY if request.json['side'] == "BUY" else Side.SELL

    order, trades = lme.add_order(symbol, price, quantity, side)
    return jsonify({'order': convert_order_to_json(order), 'trades': convert_trades_to_json(trades)}), 201

@route_defs.route('/order/cancel', methods=['POST'])
def cancel_order():
    if not request.json:
        abort(400)
    symbol = request.json['symbol']
    orderId = int(request.json['orderId'])
    order = lme.cancel_order(orderId, symbol)
    if order is not None:
        return jsonify(convert_order_to_json(order)), 200
    else:
        abort(400)

@route_defs.route('/orderbook/<symbol>', methods=['GET'])
def get_orderbook(symbol):
    orderbooks = lme.order_books
    if not orderbooks:
        return jsonify(get_empty_orderbook_json())
    orderbook = lme.order_books.get(symbol)
    if not orderbook:
        return jsonify(get_empty_orderbook_json())
    return jsonify(convert_orderbook_to_json(orderbook)), 200