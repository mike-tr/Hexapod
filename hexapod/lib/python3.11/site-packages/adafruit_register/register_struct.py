# SPDX-FileCopyrightText: Copyright (c) 2026 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_register.register_struct`
====================================================

Generic structured registers based on `struct` that use RegisterAccessor

* Author(s): Tim Cocks

"""

__version__ = "1.12.1"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Register.git"

import struct


class Struct:
    """
    Arbitrary structure register that is readable and writeable.

    Values are tuples that map to the values in the defined struct. See struct
    module documentation for struct format string and its possible value types.

    The struct format string determines the byte order of the register *data*.
    The byte order of the register *address* is determined by the ``lsb_first``
    argument given to the `RegisterAccessor`.

    :param int register_address: The register address to read the struct from
    :param str struct_format: The struct format string for this register.
    """

    def __init__(self, register_address: int, struct_format: str) -> None:
        self.format = struct_format
        self.address = register_address

        # the accessor owns address framing, so this buffer holds data only
        self.buffer = bytearray(struct.calcsize(self.format))

    def __get__(self, obj, objtype=None):
        # read data from register
        obj.register_accessor.read_register(self.address, self.buffer)

        return struct.unpack_from(self.format, self.buffer)

    def __set__(self, obj, value):
        # pack the new values into the data buffer
        struct.pack_into(self.format, self.buffer, 0, *value)

        # write data buffer to the register
        obj.register_accessor.write_register(self.address, self.buffer)


class ROStruct(Struct):
    """
    Arbitrary structure register that is read-only. Subclass of `Struct`.

    Values are tuples that map to the values in the defined struct. See struct
    module documentation for struct format string and its possible value types.

    :param int register_address: The register address to read the struct from
    :param str struct_format: The struct format string for this register.
    """

    def __set__(self, obj, value):
        raise AttributeError()


class UnaryStruct:
    """
    Arbitrary single value structure register that is readable and writeable.

    Values map to the first value in the defined struct. See struct
    module documentation for struct format string and its possible value types.

    The struct format string determines the byte order of the register *data*.
    The byte order of the register *address* is determined by the ``lsb_first``
    argument given to the `RegisterAccessor`.

    :param int register_address: The register address to read the value from
    :param str struct_format: The struct format string for this register.
    """

    def __init__(self, register_address: int, struct_format: str) -> None:
        self.format = struct_format
        self.address = register_address

        # the accessor owns address framing, so this buffer holds data only
        self.buffer = bytearray(struct.calcsize(self.format))

    def __get__(self, obj, objtype=None):
        # read data from register
        obj.register_accessor.read_register(self.address, self.buffer)

        return struct.unpack_from(self.format, self.buffer)[0]

    def __set__(self, obj, value):
        # pack the new value into the data buffer
        struct.pack_into(self.format, self.buffer, 0, value)

        # write data buffer to the register
        obj.register_accessor.write_register(self.address, self.buffer)


class ROUnaryStruct(UnaryStruct):
    """
    Arbitrary single value structure register that is read-only. Subclass of `UnaryStruct`.

    Values map to the first value in the defined struct. See struct
    module documentation for struct format string and its possible value types.

    :param int register_address: The register address to read the value from
    :param str struct_format: The struct format string for this register.
    """

    def __set__(self, obj, value):
        raise AttributeError()
