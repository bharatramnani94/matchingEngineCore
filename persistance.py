from engine import engine
from utility import convert_order_to_json
import json

def write():
    print("Trying to write...")
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
    with open('state.json', 'w') as outfile:
        json.dump(all_orders, outfile)
    return "Written " + str(len(all_orders)) + " orders!"
