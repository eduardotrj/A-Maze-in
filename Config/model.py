import re
from typing import Any, Literal, Self

from pydantic import BaseModel, ConfigDict, Field
from pydantic import field_validator, model_validator


HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")


class MazeConfig(BaseModel):
    """Validate and store maze configuration values."""

    model_config = ConfigDict(extra="forbid")

    width: int = Field(alias="WIDTH", ge=1)
    height: int = Field(alias="HEIGHT", ge=1)

    entry: tuple[int, int] = Field(alias="ENTRY")
    exit_: tuple[int, int] = Field(alias="EXIT")

    output_file: str = Field(alias="OUTPUT_FILE", min_length=1)
    perfect: bool = Field(alias="PERFECT")

    seed: int | None = Field(default=None, alias="SEED", ge=0)
    generator: Literal[
        "recursive_backtracker",
        "kruskal",
        "prim",
    ] | None = Field(
        default=None,
        alias="GENERATOR",
    )

    animation: bool | None = Field(default=None, alias="ANIMATION")
    speed: int | None = Field(default=None, alias="SPEED", ge=0)

    wall_color: str | None = Field(default=None, alias="WALL_COLOR")
    floor_color: str | None = Field(default=None, alias="FLOOR_COLOR")
    solution_color: str | None = Field(default=None, alias="SOLUTION_COLOR")
    entry_color: str | None = Field(default=None, alias="ENTRY_COLOR")
    exit_color: str | None = Field(default=None, alias="EXIT_COLOR")

    @field_validator("entry", "exit_", mode="before")
    @classmethod
    def parse_coordinates(cls, value: Any) -> tuple[int, int]:
        """Parse coordinates written in x,y format."""
        if not isinstance(value, str):
            raise ValueError("coordinates must be in x,y format")

        parts = value.split(",")

        if len(parts) != 2:
            raise ValueError("coordinates must be in x,y format")

        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except ValueError as exc:
            raise ValueError(
                "coordinates must contain integers"
            ) from exc

    @field_validator("seed", mode="before")
    @classmethod
    def parse_seed(cls, value: Any) -> Any:
        """Convert null-like SEED values to None."""
        if value in {"None", "null"}:
            return None

        return value

    @field_validator("generator", mode="before")
    @classmethod
    def normalize_generator(
        cls,
        value: str | None,
    ) -> str | None:
        """Normalize generator name."""
        if value is None:
            return None

        return value.strip().lower()

    @field_validator(
        "wall_color",
        "floor_color",
        "solution_color",
        "entry_color",
        "exit_color",
    )
    @classmethod
    def validate_hex_color(cls, value: str | None) -> str | None:
        """Validate hexadecimal color values."""
        if value is None:
            return None

        if not HEX_COLOR_PATTERN.fullmatch(value):
            raise ValueError(
                "color values must be in #RRGGBB format"
            )

        return value

    @field_validator("output_file")
    @classmethod
    def validate_output_file(cls, value: str) -> str:
        """Validate output file name."""
        if value.strip() != value:
            raise ValueError(
                "OUTPUT_FILE must not start or end with spaces"
            )

        if "/" in value or "\\" in value:
            raise ValueError(
                "OUTPUT_FILE must be a file name, not a path"
            )

        if value in {".", ".."}:
            raise ValueError("OUTPUT_FILE is invalid")

        return value

    @model_validator(mode="after")
    def validate_entry_and_exit(self) -> Self:
        """Validate entry and exit positions against maze bounds."""
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit_

        if self.entry == self.exit_:
            raise ValueError("ENTRY and EXIT must be different")

        if entry_x < 0 or entry_y < 0:
            raise ValueError("ENTRY must not be negative")

        if exit_x < 0 or exit_y < 0:
            raise ValueError("EXIT must not be negative")

        if entry_x >= self.width or entry_y >= self.height:
            raise ValueError("ENTRY must be inside maze bounds")

        if exit_x >= self.width or exit_y >= self.height:
            raise ValueError("EXIT must be inside maze bounds")

        return self
