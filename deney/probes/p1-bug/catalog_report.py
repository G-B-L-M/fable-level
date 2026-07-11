from load import load_products


def main():
    products = load_products()
    for sku in ["p1", "p2"]:
        print(f"{sku}: {products[sku]}")


if __name__ == "__main__":
    main()
