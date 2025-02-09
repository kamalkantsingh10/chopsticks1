from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass

class Intensity(Enum):
    MILD = 0.3
    NORMAL = 0.6
    INTENSE = 1.0

@dataclass
class Position:
    x: float
    y: float
    speed: float