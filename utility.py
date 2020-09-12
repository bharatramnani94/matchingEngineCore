from lightmatchingengine.lightmatchingengine import Side

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