#base.py

from dataclasses import dataclass, field
from enum import Enum

class Status(Enum):
    OK = "✓"
    WARN = "⚠"
    FAIL = "✗"

@dataclass
class CheckItem:
    label: str
    status: Status
    message: str

@dataclass
class CheckCategory:
    name: str
    items: list[CheckItem] = field(default_factory=list)