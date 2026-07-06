import sys
from config.parser import load_config


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 config_test.py config.txt")
        return

    config_path = sys.argv[1]
    try:
        config = load_config(config_path)
        print(config)
    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
