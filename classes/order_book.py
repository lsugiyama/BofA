import classes.order as Order
import heapq
import classes.trade as Trade

class OrderBook:
    def __init__(self):
        # self.bids = []
        # self.asks = []
        # heapq.heapify(self.bids)
        # heapq.heapify(self.asks)
        self.books_by_symbol ={}
        self.trade_log = []
        self.market_positions = {}

    def show_positions(self):
        for symbol, net in self.market_positions:
            print(f"{symbol}: {net}")
    
    def show_trades(self):
        for order in self.trade_log:
            print(order.__repr__)

    def _get_or_create_symbol_book(self, symbol):
        if symbol not in self.books_by_symbol:
            bids_asks_dict = {'bids': [], 'asks': []}
            self.books_by_symbol[symbol] = bids_asks_dict
        return self.books_by_symbol[symbol]
    
    def add_order(self, order: Order):
        if order.side == "BUY":
            # heapq.heappush(self.bids,(-order.price, order.order_id, order))
            self._try_match_buy(order)
        elif order.side =="SELL":
            # heapq.heappush(self.asks, (order.price, order.order_id, order))
            self._try_match_sell(order)
        else:
            print("error non defined order.side")
    
    def display_book(self, symbol=None):
        print("here")
        if symbol is None:
            for symbol in self.books_by_symbol.keys():
                print(self.books_by_symbol[symbol])
        else:
            print(self.books_by_symbol[symbol])

    def _try_match_buy(self, new_buy_order):
        bids_asks_dict = self._get_or_create_symbol_book(new_buy_order.symbol)
        self.asks = bids_asks_dict['asks']
        self.bids = bids_asks_dict['bids']
        while self.asks:
            if self.asks[0].price <= new_buy_order.price:
                price, id, best_ask_order = heapq.heappop(self.asks)
                if best_ask_order.quantity >= new_buy_order.quantity:
                    print(f"TRADE executed {new_buy_order.quantity} at {best_ask_order.price}")
                    best_ask_order.quantity -= new_buy_order.quantity
                    trade = Trade(new_buy_order.symbol, best_ask_order.price, new_buy_order.quantity, best_ask_order.order_id, new_buy_order.order_id)
                    self.trade_log.append(trade)
                    self.market_positions[new_buy_order.symbol] -= new_buy_order.quantity
                    if best_ask_order.quantity > 0:
                        heapq.heappush(self.asks, (price, id, best_ask_order))
                else:
                    print(f"TRADE executed {best_ask_order.quantity} at {best_ask_order.price}")
                    new_buy_order.quantity -= best_ask_order.quantity
                    self.market_positions[new_buy_order.symbol] -= best_ask_order.quantity
                    trade = Trade(new_buy_order.symbol, best_ask_order.price, best_ask_order.quantity, best_ask_order.order_id, new_buy_order.order_id)
                    self.trade_log.append(trade)
                    if new_buy_order.quantity:
                        heapq.heappush(self.bids, (-new_buy_order.price, new_buy_order.order_id, new_buy_order))
            else:
                print(f"TRADE failed buy price {new_buy_order.price} > {best_ask_order.price}")
                break
        else:
            print("no trade could be done")
            if new_buy_order.quantity:
                heapq.heappush(self.bids, (-new_buy_order.price, new_buy_order.order_id, new_buy_order))

    def _try_match_sell(self, new_sell_order):
        bids_asks_dict = self._get_or_create_symbol_book(new_sell_order.symbol)
        self.bids = bids_asks_dict['asks']
        while self.bids:
            if -self.bids[0].price >= new_sell_order.price:
                price, id, best_bid_order = heapq.heappop(self.bids)
                best_bid_price = - price
                if best_bid_order.quantity >= new_sell_order.quantity:
                    print(f"TRADE executed {new_sell_order.quantity} at {best_bid_price}")
                    best_bid_order.quantity -= new_sell_order.quantity
                    self.market_positions[new_sell_order.symbol] -= new_sell_order.quantity
                    trade = Trade(new_sell_order.symbol, best_bid_order.price, new_sell_order.quantity, best_bid_order.order_id, new_sell_order.order_id)
                    self.trade_log.append(trade)
                    if best_bid_order.quantity > 0:
                        heapq.heappush(self.bids, (price, id, best_bid_order))
                else:
                    print(f"TRADE executed {best_bid_order.quantity} at {best_bid_price}")
                    new_sell_order.quantity -= best_bid_order.quantity
                    self.market_positions[new_sell_order.symbol] -= best_bid_order.quantity
                    trade = Trade(new_sell_order.symbol, best_bid_order.price, best_bid_order.quantity, best_bid_order.order_id, new_sell_order.order_id)
                    self.trade_log.append(trade)
                    if new_sell_order.quantity:
                        heapq.heappush(self.asks, (new_sell_order.price, new_sell_order.order_id, new_sell_order))
            else:
                print(f"TRADE failed buy price {new_sell_order.price} > {best_bid_order.price}")
                break
        else:
            print("no trades could be done")
            self.market_positions[new_sell_order.symbol] += new_sell_order.quantity
            if new_sell_order.quantity:
                    heapq.heappush(self.asks, (new_sell_order.price, new_sell_order.order_id, new_sell_order))

