#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright 2025 Semyon Yakimov <sdyakimov@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from datetime import time
from serial import Serial
from serial.serialutil import SerialException


class Huichang(object):
    
    START_SEQUENCE = b'\xaa\xbb\xff'

    CMD_CARD_DATA = b'\x20'
    CMD_WRITE_FINGER_NAME = b'\x64'
    CMD_READ_FINGER_NAME = b'\x65'

    def __init__(self, port=None, debug=False, logger=None):
        self._serial = None
        self._log_info = print
        self._log_debug = lambda s: None
        if debug:
            self._log_debug = print
        if logger:
            if callable(logger.debug):
                self._log_debug = logger.debug
            if callable(logger.info):
                self._log_info = logger.info

        if port:
            self._connect_master_station(port)


    def send_command(self, cmd, params=None, wait_response=True, timeout=None):
        if params is None:
            params = b''
        if self._serial is None:
            raise HuichangException("Not connected to master station")

        datalen = len(params) + 1
        packet = cmd + bytes([datalen]) + params
        crc = 0xff
        if datalen > 1:
            crc = self.crc8(packet)
        packet = self.START_SEQUENCE + packet + bytes([crc])

        self._log_debug("=> 0x {}".format(" ".join(f"{b:02x}" for b in packet)))

        self._serial.flushInput()
        self._serial.write(packet)

        if wait_response:
            resp_code, data = self._read_response(timeout)
            return self._process_response(resp_code, data)

        return None

    def _connect_master_station(self, port):
        try:
            self._serial = Serial(port, baudrate=38400, timeout=3)
        except (SerialException, OSError):
            raise HuichangException(("Could not open port {}").format(port))

    def _read_response(self, timeout=None):
        if self._serial is None:
            raise HuichangException("Not connected to master station")
        serial = self._serial

        if timeout is not None:
            old_timeout = serial.timeout
            serial.timeout = timeout

        try:
            # Skip any bytes before start sequence
            while True:
                byte = serial.read()
                if byte == b"":
                    raise HuichangTimeout("No response")
                elif byte == Huichang.START_SEQUENCE[0] and serial.read() == Huichang.START_SEQUENCE[1] and serial.read() == Huichang.START_SEQUENCE[2]:
                    break

            cmd_code = serial.read()
            length = serial.read()
            if length < 1:
                raise HuichangException(f"Invalid length: {length}")

            read_more_fragments = False
            if cmd_code == Huichang.CMD_CARD_DATA and length > 1:
                read_more_fragments = True

            payload = serial.read(length - 1)
            crc = serial.read()
            self._log_debug("<= code 0x{b:02x}, len {}, data 0x {}".format(cmd_code, length, " ".join(f"{b:02x}" for b in payload)))
            if not self.crc8(cmd_code + length + payload) == crc:
                raise HuichangException("CRC mismatch")

        except (SerialException, OSError) as msg:
            raise HuichangException(f"Error reading response: {msg}")
        finally:
            if timeout is not None:
                serial.timeout = old_timeout

        if read_more_fragments:
            next_cmd_code, next_data = self._read_response(timeout)
            if next_cmd_code == cmd_code:
                payload += next_data
            else:  # got an error
                return next_cmd_code, next_data

        return cmd_code, payload

    def _process_response(self, cmd_code, data):
        if cmd_code == Huichang.CMD_CARD_DATA:
            ret = {}
            ret["card_number"] = int.from_bytes(data[0:4], order="big")
            ret["start_time"] = huichang._to_time(data[5:9])
            ret["finish_time"] = huichang._to_time(data[10:14])
            ret["clear_time"] = huichang._to_time(data[15:18])
            ret["punches"] = []
            for i in range(18, len(data), 4):
                cp_code = data[i]
                cp_time = Huichang._to_time(data[i + 1:i + 4])
                ret["punches"].append((cp_code, cp_time))
            return ret
        else:
            return None

    @staticmethod
    def _to_time(data: bytes) -> time:
        ms = 0
        if len(data) > 3:
            ms = data[3]
        return time(hour=data[0], minute=data[1], second=data[2], microsecond=ms*1000)
        

    @staticmethod
    def crc8(data: bytes) -> int:
        poly = 0x1d
        crc = 0x03  # init

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ poly) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        crc ^= 0x03  # xorout
        return crc

class HuichangException(Exception):
    pass

class HuichangTimeout(HuichangException):
    pass


if __name__ == "__main__":
    hc = Huichang("/dev/ttyUSB0", debug=True)
    hc.send_command(Huichang.CMD_READ_FINGER_NAME, wait_response=False)
    hc.send_command(Huichang.CMD_WRITE_FINGER_NAME, params=bytes.fromhex("61 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20"))

