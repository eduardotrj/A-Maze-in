from pathlib import Path


def load_config(path: str) -> dict[str, str]:
    """Load KEY=VALUE pairs from a config file.

    Lines starting with '#' and empty lines are ignored.
    """
    config: dict[str, str] = {}

    with Path(path).open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError(
                    f"Invalid config syntax at line {line_number}: {line}"
                )

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            if not key:
                raise ValueError(
                    f"Missing key at line {line_number}: {line}"
                )

            config[key] = value

    return config
