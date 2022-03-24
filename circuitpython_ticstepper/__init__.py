from circuitpython_ticstepper.constants import StepMode

try:
    import typing  # pylint: disable=unused-import
    from circuitpython_ticstepper.constants import (
        StepModeValues,
    )  # pylint: disable=ungrouped-imports
except ImportError:
    pass


class TicMotor:

    MAX_RPM = 550

    def __init__(self, step_mode: StepModeValues = StepMode.FULL) -> None:
        self._step_mode = step_mode
        self._rpm = 0
        self.clear()

    def clear(self) -> None:
        raise NotImplementedError("Must define in subclass")

    def _rpm_to_pps(self, rpm: float) -> int:
        return int(rpm * self._step_mode.multiplier * 10000)

    @property
    def step_mode(self) -> StepMode:
        return self._step_mode

    @step_mode.setter
    def step_mode(self, mode: StepMode) -> None:
        raise NotImplementedError("Must define in subclass")

    @property
    def settings(self):
        raise NotImplementedError("Must define in subclass")

    # @property
    # def position(self):
    #    raise NotImplementedError("Must define in subclass")

    def move(self, units):
        raise NotImplementedError("Must define in subclass")

    def drive(self, rpm):
        raise NotImplementedError("Must define in subclass")

    def halt(self):
        raise NotImplementedError("Must define in subclass")

    def set_circ_mode(self):
        self.halt()
        self.clear()
        self.step_mode = StepMode.FULL
        self.drive(200)

    def aspirate_slug(self):
        self.halt()
        self.clear()
        self.step_mode = StepMode.EIGHTH
