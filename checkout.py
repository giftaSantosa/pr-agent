from cart import total_price, apply_discount

def checkout(items, code=None):
    total = total_price(items)
    total = apply_discount(total, code)
    return round(total, 2)
