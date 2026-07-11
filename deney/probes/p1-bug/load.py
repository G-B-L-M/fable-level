import csv


def load_users(path="users.csv"):
    users = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            users[row["id"]] = row["name"]
    return users


def load_orders(path="orders.csv"):
    orders = []
    with open(path) as f:
        for row in csv.DictReader(f):
            orders.append({
                "order_id": row["order_id"].strip(),
                "user_id": row["user_id"].strip(),
                "amount": float(row["amount"]),
            })
    return orders


def load_products(path="products.csv"):
    products = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            products[row["sku"]] = row["title"]
    return products
