from enum import Enum


class StartCondition(Enum):
    """
    defines two start conditions: date and trigger
    """
    DATE = "date"
    TRIGGER = "trigger"
