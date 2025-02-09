from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time
import random
import logging

# Base Enums and Data Classes
class Intensity(Enum):
    MILD = 0.3
    NORMAL = 0.6
    INTENSE = 1.0

class Mode(Enum):
    PLAYFUL = "playful"
    SLEEPY = "sleepy"
    CURIOUS = "curious"
    CLINGY = "clingy"
    GUARD = "guard"
    NORMAL = "normal"
    SLEEP = "sleep"

class Emotion(Enum):
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ALERT = "alert"
    CURIOUS = "curious"
    SLEEPY = "sleepy"
    LOVING = "loving"
    GRUMPY = "grumpy"
    SCARED = "scared"
    MISCHIEVOUS = "mischievous"
    NEUTRAL = "neutral"

@dataclass
class Position:
    x: float
    y: float
    z: float = 0.0

@dataclass
class ServoConfig:
    pin: int
    min_angle: float
    max_angle: float
    default_speed: float

@dataclass
class EmotionConfig:
    idle_actions: List[str]
    sounds: List[str]
    expressions: List[str]
    default_intensity: Intensity