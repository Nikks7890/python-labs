from functools import total_ordering
from typing import Any


@total_ordering
class Athlete:
    def __init__(
        self, name: str, country: str, points: float, penalties: float, age: int
    ) -> None:
        self.name = name
        self.country = country
        self.points = points
        self.penalties = penalties
        self.age = age

    @property
    def final_points(self) -> float:
        return self.points - self.penalties

    def _key(self) -> tuple[float, float, str]:
        # спочатку final_points, потім points, потім name
        return (self.final_points, self.points, self.name)

    def __repr__(self) -> str:
        return (
            f"Athlete({self.name!r}, {self.country!r}, "
            f"{self.points}, {self.penalties}, {self.age})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Athlete):
            return NotImplemented
        return self._key() == other._key()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Athlete):
            return NotImplemented
        return self._key() < other._key()

    @classmethod
    def from_dict(cls, r: dict[str, Any]) -> "Athlete":
        return cls(
            r["name"],
            r["country"],
            float(r["points"]),
            float(r["penalties"]),
            int(r["age"]),
        )
