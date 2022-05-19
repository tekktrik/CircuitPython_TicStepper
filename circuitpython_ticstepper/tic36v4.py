# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""
`circuitpython_ticstepper.tic36v4`
================================================================================

TIC Motor over I2C control


* Author(s): Alec Delaney

"""

from circuitpython_ticstepper.i2c import TicMotorI2C
from circuitpython_ticstepper.constants import StepMode

try:
    import typing  # pylint: disable=unused-import
    from busio import I2C
    from circuitpython_ticstepper.constants import (  # pylint: disable=ungrouped-imports
        StepModeValues,
    )
except ImportError:
    pass

class TIC36v4_I2C(TicMotorI2C):

    MAX_CURRENT_LIMIT = 4
    """The maximum current limit for the TIC 36v4.
    
    .. note::
    
        It is technically possible to change this, both for the hardware and
        in this library, so be sure to make sure they match.
        
    """

    def convert_current_value(self, current: float) -> int:
        """Converts the desired current into the TIC value, rounds down
        to nearest acceptable value
        """

        acceptable_values = [value for value in range(128) if current >= (value/127)*self.MAX_CURRENT_LIMIT]
        return max(acceptable_values)

    def convert_current_enum(self, enum_value: int) -> float:
        """Converts the desired TIC enumeration into the corresponding
        current limit
        """

        return enum_value * (enum_value/127) * self.MAX_CURRENT_LIMIT
