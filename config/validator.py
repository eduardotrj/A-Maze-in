class ConfigValidator:
    """Validate raw configuration values and return a typed dictionary."""

    MANDATORY_KEYS = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    OPTIONAL_KEYS = {
        "SEED",
        "GENERATOR",
        "DISPLAY",
    }

    def __init__(self, raw_config: dict[str, str]) -> None:
        self.raw_config = raw_config

    def validate(self) -> dict[str, object]:
        """Validate raw values and return a typed config dictionary."""
        self._check_mandatory_keys()
        self._check_unknown_keys()

        width = self._parse_positive_int("WIDTH")
        height = self._parse_positive_int("HEIGHT")
        entry = self._parse_coordinates("ENTRY")
        exit_ = self._parse_coordinates("EXIT")
        output_file = self._validate_output_file()
        perfect = self._parse_bool("PERFECT")

        self._validate_coordinates(entry, exit_, width, height)

        config: dict[str, object] = {
            "WIDTH": width,
            "HEIGHT": height,
            "ENTRY": entry,
            "EXIT": exit_,
            "OUTPUT_FILE": output_file,
            "PERFECT": perfect,
        }

        self._add_optional_values(config)

        return config

    def _check_mandatory_keys(self) -> None:
        """Check whether all mandatory keys are present."""
        for key in self.MANDATORY_KEYS:
            if key not in self.raw_config:
                raise ValueError(f"Missing mandatory key: {key}")

    def _check_unknown_keys(self) -> None:
        """Reject unsupported configuration keys."""
        allowed_keys = self.MANDATORY_KEYS | self.OPTIONAL_KEYS

        for key in self.raw_config:
            if key not in allowed_keys:
                raise ValueError(f"Unknown config key: {key}")

    def _add_optional_values(self, config: dict[str, object]) -> None:
        """Validate optional values and add them if they exist."""
        if "SEED" in self.raw_config:
            config["SEED"] = self._parse_seed()

        if "GENERATOR" in self.raw_config:
            config["GENERATOR"] = self._parse_generator()

        if "DISPLAY" in self.raw_config:
            config["DISPLAY"] = self._parse_display()

    def _parse_positive_int(self, key: str) -> int:
        """Parse a positive integer value."""
        value = self.raw_config[key]

        try:
            number = int(value)
        except ValueError as exc:
            raise ValueError(f"{key} must be an integer") from exc

        if number <= 0:
            raise ValueError(f"{key} must be greater than 0")

        return number

    def _parse_bool(self, key: str) -> bool:
        """Parse a boolean value."""
        value = self.raw_config[key]

        if value == "True":
            return True

        if value == "False":
            return False

        raise ValueError(f"{key} must be True or False")

    def _parse_coordinates(self, key: str) -> tuple[int, int]:
        """Parse coordinates in x,y format."""
        value = self.raw_config[key]
        parts = value.split(",")

        if len(parts) != 2:
            raise ValueError(f"{key} must be in x,y format")

        try:
            x = int(parts[0].strip())
            y = int(parts[1].strip())
        except ValueError as exc:
            raise ValueError(f"{key} coordinates must be integers") from exc

        if x < 0 or y < 0:
            raise ValueError(f"{key} coordinates must not be negative")

        return x, y

    def _parse_seed(self) -> int | None:
        """Parse optional SEED value."""
        value = self.raw_config["SEED"]

        if value in {"None", "null"}:
            return None

        try:
            seed = int(value)
        except ValueError as exc:
            raise ValueError("SEED must be an integer, None, or null") from exc

        if seed < 0:
            raise ValueError("SEED must not be negative")

        return seed

    def _parse_generator(self) -> str:
        """Parse optional GENERATOR value."""
        generator = self.raw_config["GENERATOR"]

        allowed_generators = {
            "recursive_backtracker",
        }

        if generator not in allowed_generators:
            raise ValueError(
                "GENERATOR must be one of: recursive_backtracker"
            )

        return generator

    def _parse_display(self) -> str:
        """Parse optional DISPLAY value."""
        display = self.raw_config["DISPLAY"]

        allowed_displays = {
            "ascii",
        }

        if display not in allowed_displays:
            raise ValueError("DISPLAY must be one of: ascii")

        return display

    def _validate_output_file(self) -> str:
        """Validate the output file name."""
        output_file = self.raw_config["OUTPUT_FILE"]

        if output_file.strip() != output_file:
            raise ValueError("OUTPUT_FILE must not start or end with spaces")

        if "/" in output_file or "\\" in output_file:
            raise ValueError("OUTPUT_FILE must be a file name, not a path")

        if output_file in {".", ".."}:
            raise ValueError("OUTPUT_FILE is invalid")

        return output_file

    def _validate_coordinates(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        width: int,
        height: int,
    ) -> None:
        """Validate entry and exit coordinates."""
        entry_x, entry_y = entry
        exit_x, exit_y = exit_

        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different")

        if entry_x >= width or entry_y >= height:
            raise ValueError("ENTRY must be inside maze bounds")

        if exit_x >= width or exit_y >= height:
            raise ValueError("EXIT must be inside maze bounds")
