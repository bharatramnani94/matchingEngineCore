from utility import convert_order_to_json
from lightmatchingengine.lightmatchingengine import Side
import json

state_file = 'state.json'

def write(engine):
    orderbooks = engine.order_books
    if not orderbooks:
        return
    all_orders = []
    for key in orderbooks.keys():
        orderbook = engine.order_books.get(key)
        for pricepoint, orders in orderbook.bids.items():
            for order in orders:
                all_orders.append(convert_order_to_json(order))
        for pricepoint, orders in orderbook.asks.items():
            for order in orders:
                all_orders.append(convert_order_to_json(order))
    with open(state_file, 'w', 0) as outfile:
        json.dump(all_orders, outfile, indent=2)
    return "Written " + str(len(all_orders)) + " orders!"

def boot(engine):
    with open(state_file) as json_file:
        orders = json.load(json_file)
        if not orders:
            return
        sorted_orders = sorted(orders, key=lambda order: order.get('orderId'))
        for order in sorted_orders:
            symbol = order.get('symbol')
            price = int(order.get('price'))
            quantity = int(order.get('quantityRemaining'))
            side = Side.BUY if order.get('side') == "BUY" else Side.SELL
            engine.add_order(symbol, price, quantity, side)
        print("Booting of Engine successful with " + str(len(orders)) + " Orders")