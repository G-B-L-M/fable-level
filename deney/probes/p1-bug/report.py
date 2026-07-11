from load import load_users, load_orders


def main():
    users = load_users()
    orders = load_orders()
    totals = {}
    for o in orders:
        name = users[o["user_id"]]
        totals[name] = totals.get(name, 0) + o["amount"]
    for name, total in sorted(totals.items()):
        print(f"{name}: {total:.2f}")


if __name__ == "__main__":
    main()
