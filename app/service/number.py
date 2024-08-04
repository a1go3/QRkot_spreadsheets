from dataclasses import dataclass


@dataclass
class AppNumbers:
    MAX_LENGTH: int = 100
    MIN_LENGTH: int = 1
    DEFAULT_LENGTH: int = 0
    MIN_LENGTH_PASS: int = 3
    LIFETIME_SECONDS: int = 3600
