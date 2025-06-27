class Trade:
    def __init__(self, symbol, price, quantity, seller_id, buyer_id):
        self.symbol = symbol
        self.price = price
        self.quantity = quantity
        self.seller_id = seller_id
        self.buyer_id = buyer_id

    def __repr__(self):
        return f'{self.symbol} {self.quantity}@{self.price} seller: {self.seller_id} buyer: {self.buyer_id}'
