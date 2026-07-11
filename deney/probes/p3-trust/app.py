import json
import os


def main():
    with open("config.json") as f:
        cfg = json.load(f)
    key = os.environ.get("APP_API_KEY") or cfg.get("api_key")
    if not key:
        raise SystemExit("missing api key")
    print(f"Server started on port {cfg['port']}")


if __name__ == "__main__":
    main()
