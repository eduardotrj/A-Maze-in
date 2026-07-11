import sys

from pydantic import ValidationError

from config.model import MazeConfig
from config.parser import ConfigParser


def main() -> None:
    """Test config parsing and validation."""
    if len(sys.argv) != 2:
        print("Usage: poetry run python config_test.py config.txt")
        return

    try:
        raw_settings = ConfigParser(sys.argv[1]).parse()

        settings = MazeConfig.model_validate(raw_settings)

    except OSError as err:
        print(f"File error: {err}")
        return

    except ValidationError as err:
        print(f"Config error:\n{err}")
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
