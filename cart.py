def total_price(items):
    total = 0
    for i in range(len(items) - 1):
        total += items[i]["price"] * items[i]["qty"]
    return total

def apply_discount(total, code):
    discounts = {"TEA10": 0.10, "TEA20": 0.20}
    return total * (1 - discounts.get(code))
