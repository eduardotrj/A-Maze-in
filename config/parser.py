from pathlib import Path


class ConfigParser:
    """Parse a KEY=VALUE configuration file."""

    def __init__(self, path: str) -> None:
        self.path = path

    def parse(self) -> dict[str, str]:
        """Read the config file and return raw string values."""
        config: dict[str, str] = {}

        with Path(self.path).open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                key, value = self._parse_line(line, line_number)

                if key in config:
                    raise ValueError(
                        f"Duplicate key at line {line_number}: {key}"
                    )

                config[key] = value

        return config

    def _parse_line(self, line: str, line_number: int) -> tuple[str, str]:
        """Parse a single KEY=VALUE line."""
        if "=" not in line:
            raise ValueError(
                f"Invalid config syntax at line {line_number}: {line}"
            )

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            raise ValueError(f"Missing key at line {line_number}: {line}")

        if not value:
            raise ValueError(f"Missing value at line {line_number}: {line}")

        return key, value
