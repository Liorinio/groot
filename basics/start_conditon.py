from enum import Enum


class StartCondition(Enum):
    """
    Defines two start conditions: date and trigger
    """
    DATE = "date"
    TRIGGER = "trigger"
