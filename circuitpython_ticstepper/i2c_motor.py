import struct
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_register.i2c_struct import Struct
from circuitpython_ticstepper import TicMotor
from circuitpython_ticstepper.constants import StepMode

try:
    from typing import Optional, Type, List
    from circuitpython_typing import ReadableBuffer
    from circuitpython_typing.device_drivers import I2CDeviceDriver
    from busio import I2C
    from circuitpython_ticstepper.constants import StepModeValues
except ImportError:
    pass

_CMD_STEP_MODE = const(0x94)
_CMD_RESET = const(0xB0)
_CMD_CLEAR_ERROR = const(0x8A)
_CMD_MAX_SPEED = const(0xE6)
_CMD_HALT = const(0xEC)
_CMD_MOVE = const(0xE0)
_CMD_DRIVE = const(0xE3)

class ClearMSBByteStruct:
    """
    Arbitrary structure register that is readable and writeable.
    Values are tuples that map to the values in the defined struct.  See struct
    module documentation for struct format string and its possible value types.
    
    :param int register_address: The register address to read the bit from
    """

    def __init__(self, register_address: int) -> None:
        self.format = "<b"
        self.buffer = bytearray(1 + struct.calcsize(self.format))
        self.buffer[0] = register_address

    def __get__(self, obj: "TicMotorI2C", objtype: Type["TicMotorI2C"] = None) -> List[int]:
        with obj.i2c_device as i2c:
            i2c.write_then_readinto(self.buffer, self.buffer, out_end=1, in_start=1)
        return struct.unpack_from(self.format, memoryview(self.buffer)[1:])

    def __set__(self, obj: "TicMotorI2C", value: ReadableBuffer) -> None:
        struct.pack_into(self.format, self.buffer, 1, *value)
        with obj.i2c_device as i2c:
            i2c.write(self.buffer)


class TicMotorI2C(TicMotor):

    _step_mode_reg = ClearMSBByteStruct(_CMD_STEP_MODE)
    _max_speed_reg = Struct(_CMD_MAX_SPEED, "<I")
    _halt_and_set_reg = Struct(_CMD_HALT, "<i")
    _move_reg = Struct(_CMD_MOVE, "<i")
    _drive_reg = Struct(_CMD_DRIVE, "<i")

    def __init__(self, i2c: I2C, address: int = 0x0E, step_mode: StepModeValues = StepMode.FULL) -> None:

        self.i2c_device = I2CDevice(i2c, address)
        super().__init__(step_mode)
        self.clear()

    @property
    def step_mode(self) -> StepModeValues:
        return super().step_mode

    @step_mode.setter
    def step_mode(self, mode: StepModeValues) -> None:
        self._step_mode = mode
        self._step_mode_reg = [mode.value]

    #@property
    #def position(self):
    #    return super().position

    def clear(self) -> None:
        self.reset()

    def _quick_write(self, cmd: int) -> None:
        with self.i2c_device as i2c:
            i2c.write(bytes(cmd))
        
    def reset(self) -> None:
        self._quick_write(_CMD_RESET)

    def reinit(self) -> None:
        self.step_mode = self._step_mode

    def clear_error(self) -> None:
        self._quick_write(_CMD_CLEAR_ERROR)

    @property
    def max_speed(self) -> float:
        raise AttributeError("Max speed is writable only")

    @max_speed.setter
    def max_speed(self, rpm: float) -> None:
        #if not -self.MAX_RPM <= rpm <= self.MAX_RPM:
        #    raise ValueError("Given speed is over the RPM threshold")
        pulse_speed = self._rpm_to_pps(rpm)
        self._max_speed_reg = pulse_speed
        self.MAX_RPM = rpm

    def halt(self) -> None:
        self._halt_and_set_reg = [0]

    def move(self, units) -> None:
        self._move_reg = [units]

    def drive(self, rpm: float) -> None:
        if not -self.MAX_RPM <= rpm <= self.MAX_RPM:
            raise ValueError("Cannot set speed above {} RPM".format(self.MAX_RPM))

        self._drive_reg = [self._rpm_to_pps(rpm)]
        self._rpm = rpm
