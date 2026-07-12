from abc import ABC, abstractmethod


class MazeGenerator(ABC):

    @abstractmethod
    def generate(self) -> None:
        pass

    @abstractmethod
    def open_path(self, current: tuple) -> None:
        pass

    @abstractmethod
    def add_pattern(self, pattern: list[str] | None = None
                    ) -> set[tuple[int, int]]:
        pass
