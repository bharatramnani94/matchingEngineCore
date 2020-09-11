#!flask/bin/python


# https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask


from flask import Flask, jsonify, request, abort
from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side, OrderBook

def get_empty_orderbook_json():
    return {"bids": {}, "asks": {}}

def convert_order_to_json(order):
    return {
        "orderId": order.order_id,
        "side": "BUY" if order.side == Side.BUY else "SELL",
        "price": order.price,
        "quantityTotal": order.qty,
        "quantityFilled": order.cum_qty,
        "quantityRemaining": order.leaves_qty,
        "symbol": order.instmt
    }

def convert_trade_to_json(trade):
    return {
        "tradeId": trade.trade_id,
        "orderId": trade.order_id,
        "side": "BUY" if trade.trade_side == Side.BUY else "SELL",
        "price": trade.trade_price,
        "quantity": trade.trade_qty,
        "symbol": trade.instmt
    }

def convert_trades_to_json(trades):
    return map(lambda trade: convert_trade_to_json(trade), trades)

def convert_orderbook_to_json(orderbook):
    result = get_empty_orderbook_json()
    for pricepoint, orders in orderbook.bids.items():
        result["bids"][pricepoint] = sum(o.leaves_qty for o in orders)
    for pricepoint, orders in orderbook.asks.items():
        result["asks"][pricepoint] = sum(o.leaves_qty for o in orders)
    return result

lme = LightMatchingEngine()
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify("Hello, World!")

@app.route('/order/create', methods=['POST'])
def create_order():
    if not request.json:
        abort(400)

    symbol = request.json['symbol']
    price = int(request.json['price'])
    quantity = int(request.json['quantity'])
    side = Side.BUY if request.json['side'] == "BUY" else Side.SELL

    order, trades = lme.add_order(symbol, price, quantity, side)
    return jsonify({'order': convert_order_to_json(order), 'trades': convert_trades_to_json(trades)}), 201

@app.route('/orderbook/<symbol>', methods=['GET'])
def get_orderbook(symbol):
    orderbooks = lme.order_books
    if not orderbooks:
        return jsonify(get_empty_orderbook_json())
    orderbook = lme.order_books.get(symbol)
    if not orderbook:
        return jsonify(get_empty_orderbook_json())
    return jsonify(convert_orderbook_to_json(orderbook)), 200


if __name__ == '__main__':
    app.run(debug=True)



def print_trade(trade):
    side = "BUY"
    if trade.trade_side == 2:
        side = "SELL"
    print("TRADE: id=" + str(trade.trade_id) + ", side=" + side + ", qty=" + str(trade.trade_qty) + ", price=" + str(trade.trade_price) + ", orderId=" + str(trade.order_id))


def print_order(order):
    side = "BUY"
    if order.side == 2:
        side = "SELL"
    print("ORDER: id=" + str(order.order_id) + ", side=" + side + ", qty=" + str(order.leaves_qty) + ", price=" + str(order.price) + ", orderId=" + str(order.order_id))

def print_orderbook():
    print('\n')
    print("BIDS:")
    for pricepoint, orders in lme.order_books['EUR/USD'].bids.items():
        print(pricepoint, map(lambda o: o.leaves_qty, orders))
    print("ASKS:")
    for pricepoint, orders in lme.order_books['EUR/USD'].asks.items():
        print(pricepoint, map(lambda o: o.leaves_qty, orders))
    print('\n')

