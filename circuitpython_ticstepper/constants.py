from collections import namedtuple

StepModeValues = namedtuple("StepModeValues", ["value", "multiplier"])

class StepMode:

    FULL = StepModeValues(0, 1)
    HALF = StepModeValues(1, 2)
    QUARTER = StepModeValues(2, 4)
    EIGHTH = StepModeValues(3, 8)
    SIXTEENTH = StepModeValues(4, 16)
    THIRTY_SECONDTH = StepModeValues(5, 32)
    SIXTY_FOURTH = StepModeValues(7, 64)
    ONE_TWENTY_EIGTH = StepModeValues(8, 128)
    TWO_FIFTY_SIXTH = StepModeValues(9, 256)

    @classmethod
    def get_by_value(cls, value: int):
        for attr_value in cls.__dict__.values():
            if isinstance(attr_value, StepModeValues) and attr_value.value == value:
                return attr_value
        raise ValueError("Could not find the requested step mode")
