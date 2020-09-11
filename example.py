from lightmatchingengine.lightmatchingengine import LightMatchingEngine, Side, OrderBook

lme = LightMatchingEngine()

# ---

symbol = "EUR/USD"

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






buy_order1, trades = lme.add_order(symbol, 1.00, 1000, Side.BUY)
buy_order2, trades = lme.add_order(symbol, 1.20, 1200, Side.BUY)
buy_order2, trades = lme.add_order(symbol, 1.20, 800, Side.BUY)
buy_order3, trades = lme.add_order(symbol, 1.10, 1000, Side.BUY)

# print("Number of trades = %d" % len(trades))                # Number of trades = 0
print_order(buy_order1)
print_order(buy_order2)
print_order(buy_order3)

print_orderbook()

# print(lme.order_books['EUR/USD'].bids)



sell_order, trades = lme.add_order(symbol, 1.50, 1000, Side.SELL)
sell_order, trades = lme.add_order(symbol, 1.10, 1000, Side.SELL)

print_order(sell_order)

print_trade(trades[0])
print_trade(trades[1])

print_orderbook()




