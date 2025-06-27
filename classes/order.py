class Order:
    def __init__(self, id, symbol, side, price, quantity):
        print("initializing order")
        self.order_id = id
        self.symbol = symbol
        self.side = side
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f'{self.symbol} {self.side} #{self.order_id} {self.quantity}@{self.price}'
