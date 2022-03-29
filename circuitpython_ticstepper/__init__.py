# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_ticstepper`
================================================================================

CircuitPython driver library for TIC stepper motor drivers


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Hardware:**

TIC stepper motor drivers

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's Register library:
  https://github.com/adafruit/Adafruit_CircuitPython_Register

"""

from circuitpython_ticstepper.constants import StepMode

try:
    import typing  # pylint: disable=unused-import
    from circuitpython_ticstepper.constants import (
        StepModeValues,
    )  # pylint: disable=ungrouped-imports
except ImportError:
    pass


class TicMotor:
    """Base class for TIC stepper motors

    :param StepModeValues step_mode: The step mode to use
    """

    MAX_RPM = 550

    def __init__(self, step_mode: StepModeValues = StepMode.FULL) -> None:
        self._step_mode = step_mode
        self._rpm = 0
        self.clear()

    def clear(self) -> None:
        """Clears and reinits the stepper motor"""
        raise NotImplementedError("Must define in subclass")

    def _rpm_to_pps(self, rpm: float) -> int:
        """Converts RPM to the pulses per 10000 seconds input needed
        for speed commands

        :param float rpm: Speed in rpm
        """
        return int((rpm*self._step_mode.multiplier*10000*10)/3)

    @property
    def step_mode(self) -> StepMode:
        """Gets and sets the stepper step mode"""
        return self._step_mode

    @step_mode.setter
    def step_mode(self, mode: StepMode) -> None:
        raise NotImplementedError("Must define in subclass")

    # @property
    # def settings(self):
    #    raise NotImplementedError("Must define in subclass")

    # @property
    # def position(self):
    #    raise NotImplementedError("Must define in subclass")

    def move(self, units: int) -> None:
        """Moves the given number of steps/microsteps

        :param int units: The number of steps/microsteps to move
        """
        raise NotImplementedError("Must define in subclass")

    def drive(self, rpm: float) -> None:
        """Drives the motor at a given speed

        :param float rpm: The speed to move the motor in RPM
        """
        raise NotImplementedError("Must define in subclass")

    def halt(self) -> None:
        """Stops the motor"""
        raise NotImplementedError("Must define in subclass")
