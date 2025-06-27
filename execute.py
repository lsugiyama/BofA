from classes.order_book import OrderBook
from classes.order import Order

def main():
    orderbook = OrderBook()
    ID = 1
    input_line = input().split()
    while input_line:
        try:
            print(input_line)
            command = input_line[0]
            print(command)
            match command:
                case "BUY":
                    symbol = input_line[1]
                    quantity = int(input_line[2])
                    price = float(input_line[3])
                    order = Order(ID, symbol, "BUY", price, quantity)
                    orderbook.add_order(order)
                    ID += 1
                case "SELL":
                    symbol = input_line[1]
                    quantity = input_line[2]
                    price = input_line[3]
                    order = Order(ID, symbol, "SELL", price, quantity)
                    orderbook.add_order(order)
                    ID += 1
                case "BOOK":
                    symbol = None
                    if len(input_line) > 1:
                        symbol = input_line[1]
                    orderbook.display_book(symbol)
                case "TRADES":
                    orderbook.show_trades()
                case "POSITIONS":
                    orderbook.show_positions()
                case "QUIT":
                    print("quit called, quitting...")
                    exit(0)
            input_line = input().split()
        except Exception as e:
            print("input_line invalid or empty quitting...")
            print(e)
            return

main()