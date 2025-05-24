from dataclasses import dataclass
from typing import Optional

@dataclass
class MatchingConfig:
    """
    Configuration for matching thresholds.
    """
    iou_threshold: float = 0.8
    containment_threshold: float = 0.9
    min_area_threshold: float = 1.0
    max_vertices: int = 1000

    def __post_init__(self):
        """Validate configuration values"""
        if not 0 <= self.iou_threshold <= 1:
            raise ValueError("IoU threshold must be between 0 and 1")
        if not 0 <= self.containment_threshold <= 1:
            raise ValueError("Containment threshold must be between 0 and 1")
        if self.min_area_threshold < 0:
            raise ValueError("Minimum area threshold must be non-negative")

# Default configuration instance
DEFAULT_CONFIG = MatchingConfig()

