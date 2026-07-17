import sys

from pydantic import ValidationError
from Config import ConfigParser, MazeConfig


# to test:
# go to root folder and run:
# poetry run python -m tests.config_test config.txt

def main() -> None:
    """Test configuration parsing and validation."""
    if len(sys.argv) != 2:
        print(
            "Usage: poetry run python -m Tests.config_test config.txt"
        )
        return

    try:
        raw_settings = ConfigParser(sys.argv[1]).parse()
        settings = MazeConfig.model_validate(raw_settings)

    except OSError as err:
        print(f"File error: {err}")
        return

    except ValidationError as err:
        print(f"Config validation error:\n{err}")
        return

    except ValueError as err:
        print(f"Config parser error: {err}")
        return

    print("Config is valid.")

    print("\nRaw config:")
    print(raw_settings)

    print("\nValidated model:")
    print(settings)

    print("\nValidated dictionary:")
    print(
        settings.model_dump(
            by_alias=True,
            exclude_none=True,
        )
    )


if __name__ == "__main__":
    main()
