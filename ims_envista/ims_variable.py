"""Data Class for IMS Variable."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IMSVariable:
    """IMS Envista Variable."""

    variable_code: str
    unit: str
    description: str

    def __repr__(self) -> str:
        return f"Code: {self.variable_code} - Unit: ({self.unit}) - Description: {self.description}"
