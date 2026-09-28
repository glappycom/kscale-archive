import time
import serial


DEFAULT_BAUDRATE = 1000000
LATENCY_TIMER_US = 40
MAX_BUSY_US = 8000
MIN_TIMEOUT_US = 1000


class PortHandler:
    def __init__(self, port_name: str, baudrate: int = DEFAULT_BAUDRATE):
        self.port_name = port_name
        self.baudrate = baudrate
        self.ser: serial.Serial | None = None
        self.is_using: bool = False
        self.packet_start_time_us: float = 0.0
        self.packet_timeout_us: float = 0.0

    # --- lifecycle ---
    def openPort(self) -> bool:
        return self.setBaudRate(self.baudrate)

    def closePort(self) -> None:
        if self.ser:
            self.ser.close()
            self.ser = None

    def clearPort(self) -> None:
        if self.ser:
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()

    # --- configuration ---
    def setPortName(self, port_name: str) -> None:
        self.port_name = port_name

    def getPortName(self) -> str:
        return self.port_name

    def setBaudRate(self, baudrate: int) -> bool:
        self.baudrate = baudrate
        return self._setupPort()

    def getBaudRate(self) -> int:
        return self.baudrate

    # --- I/O ---
    def readPort(self, length: int) -> bytes:
        if not self.ser:
            return b""
        return self.ser.read(length)

    def writePort(self, packet: bytes | bytearray | list[int]) -> int:
        if not self.ser:
            return 0
        if isinstance(packet, list):
            packet = bytes(packet)
        return self.ser.write(packet)

    # --- timing ---
    def setPacketTimeout(self, expected_bytes: int, extra_us: int = 0) -> None:
        self.packet_start_time_us = self.getCurrentTime_us()
        bit_time_us = 1_000_000.0 / float(self.baudrate)
        calc_timeout = expected_bytes * 10.0 * bit_time_us
        calc_timeout += LATENCY_TIMER_US
        if calc_timeout < MIN_TIMEOUT_US:
            calc_timeout = MIN_TIMEOUT_US
        elif calc_timeout > MAX_BUSY_US:
            calc_timeout = MAX_BUSY_US
        calc_timeout += extra_us
        self.packet_timeout_us = calc_timeout

    def isPacketTimeout(self) -> bool:
        if self.getTimeSinceStart_us() > self.packet_timeout_us:
            self.packet_timeout_us = 0.0
            return True
        return False

    def getTimeSinceStart_us(self) -> float:
        return self.getCurrentTime_us() - self.packet_start_time_us

    def getCurrentTime_us(self) -> float:
        return time.monotonic_ns() / 1_000.0

    # --- internal ---
    def _setupPort(self) -> bool:
        if self.ser:
            self.closePort()
        self.ser = serial.Serial(
            port=self.port_name,
            baudrate=self.baudrate,
            bytesize=serial.EIGHTBITS,
            timeout=0,
        )
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        return True


