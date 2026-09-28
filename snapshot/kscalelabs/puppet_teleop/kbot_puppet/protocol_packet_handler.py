from .port_handler import PortHandler


# IDs / Instructions
BROADCAST_ID = 0xFE
INST_PING = 0x01
INST_READ = 0x02
INST_WRITE = 0x03
INST_REG_WRITE = 0x04
INST_ACTION = 0x05
INST_SYNC_READ = 0x82
INST_SYNC_WRITE = 0x83

# Result codes
COMM_SUCCESS = 0
COMM_PORT_BUSY = -1
COMM_TX_FAIL = -2
COMM_RX_FAIL = -3
COMM_TX_ERROR = -4
COMM_RX_WAITING = -5
COMM_RX_TIMEOUT = -6
COMM_RX_CORRUPT = -7
COMM_NOT_AVAILABLE = -9


# Protocol Error bit
ERRBIT_VOLTAGE = 1
ERRBIT_ANGLE = 2
ERRBIT_OVERHEAT = 4
ERRBIT_OVERELE = 8
ERRBIT_OVERLOAD = 32


HEADER = b"\xFF\xFF"
PKT_ID = 2
PKT_LENGTH = 3
PKT_INSTRUCTION = 4
PKT_ERROR = 4
PKT_PARAMETER0 = 5


class ProtocolPacketHandler:
    def __init__(self, port_handler: PortHandler):
        self.ph = port_handler

    # --- helpers ---
    @staticmethod
    def _checksum(core: bytes) -> int:
        return (~sum(core) & 0xFF)

    # --- tx/rx ---
    def txPacket(self, txpacket: list[int]) -> int:
        total_len = txpacket[PKT_LENGTH] + 4
        if self.ph.is_using:
            return COMM_PORT_BUSY
        self.ph.is_using = True

        if total_len > 250:
            self.ph.is_using = False
            return COMM_TX_ERROR

        # header and checksum
        txpacket[0:2] = [0xFF, 0xFF]
        txpacket[total_len - 1] = self._checksum(bytes(txpacket[2:total_len - 1]))

        self.ph.clearPort()
        written = self.ph.writePort(txpacket)
        if written != total_len:
            self.ph.is_using = False
            return COMM_TX_FAIL
        return COMM_SUCCESS

    def rxPacket(self) -> tuple[bytes | None, int]:
        rx = bytearray()
        result = COMM_RX_WAITING
        first_seen = False
        last_byte_us = self.ph.getCurrentTime_us()
        IDLE_GAP_US = max(2 * (10.0 * 1_000_000.0 / self.ph.baudrate), 40.0)

        try:
            while True:
                chunk = self.ph.readPort(64)
                if chunk:
                    rx.extend(chunk)
                    first_seen = True
                    last_byte_us = self.ph.getCurrentTime_us()
                else:
                    if first_seen and (self.ph.getCurrentTime_us() - last_byte_us) > IDLE_GAP_US:
                        result = COMM_RX_CORRUPT
                        break

                if len(rx) < 6:
                    if self.ph.isPacketTimeout():
                        result = COMM_RX_TIMEOUT if not rx else COMM_RX_CORRUPT
                        break
                    continue

                # align header
                if rx[:2] != HEADER:
                    while len(rx) >= 2 and rx[:2] != HEADER:
                        rx.pop(0)
                    first_seen = False
                    last_byte_us = self.ph.getCurrentTime_us()
                    continue

                pkt_len = rx[PKT_LENGTH]
                need = 4 + pkt_len
                if len(rx) < need:
                    continue

                ck = self._checksum(bytes(rx[2:need - 1]))
                result = COMM_SUCCESS if rx[need - 1] == ck else COMM_RX_CORRUPT
                break
        finally:
            self.ph.is_using = False

        return (bytes(rx[:need]) if result == COMM_SUCCESS else None), result

    def txRxPacket(self, txpacket: list[int]) -> tuple[bytes | None, int, int]:
        error = 0
        res = self.txPacket(txpacket)
        if res != COMM_SUCCESS:
            return None, res, error
        if txpacket[PKT_ID] == BROADCAST_ID:
            self.ph.is_using = False
            return None, res, error

        # Timeout policy: READ depends on length; EEPROM writes (addr < 32) need longer
        if txpacket[PKT_INSTRUCTION] == INST_READ:
            self.ph.setPacketTimeout(txpacket[PKT_PARAMETER0 + 1] + 6)
        elif txpacket[PKT_INSTRUCTION] == INST_WRITE and txpacket[PKT_PARAMETER0] < 32:
            # EEPROM zone → give the servo more time to commit
            self.ph.setPacketTimeout(6, extra_us=100_000)
        else:
            self.ph.setPacketTimeout(6)

        while True:
            rx, res = self.rxPacket()
            if res != COMM_SUCCESS or (rx and txpacket[PKT_ID] == rx[PKT_ID]):
                break
        if res == COMM_SUCCESS and rx:
            error = rx[PKT_ERROR]
        return rx, res, error

    # --- typed ops ---
    def readTxRx(self, scs_id: int, address: int, length: int) -> tuple[list[int], int, int]:
        if scs_id >= BROADCAST_ID:
            return [], COMM_NOT_AVAILABLE, 0
        tx = [0] * 8
        tx[PKT_ID] = scs_id
        tx[PKT_LENGTH] = 4
        tx[PKT_INSTRUCTION] = INST_READ
        tx[PKT_PARAMETER0 + 0] = address
        tx[PKT_PARAMETER0 + 1] = length
        rx, res, err = self.txRxPacket(tx)
        if res != COMM_SUCCESS or not rx:
            return [], res, err
        return list(rx[PKT_PARAMETER0: PKT_PARAMETER0 + length]), res, err

    def writeTxRx(self, scs_id: int, address: int, data: list[int]) -> tuple[int, int]:
        tx = [0] * (len(data) + 7)
        tx[PKT_ID] = scs_id
        tx[PKT_LENGTH] = len(data) + 3
        tx[PKT_INSTRUCTION] = INST_WRITE
        tx[PKT_PARAMETER0] = address
        tx[PKT_PARAMETER0 + 1: PKT_PARAMETER0 + 1 + len(data)] = data
        _, res, err = self.txRxPacket(tx)
        return res, err

    # convenience
    def read1(self, scs_id: int, address: int):
        data, res, err = self.readTxRx(scs_id, address, 1)
        return (data[0] if res == COMM_SUCCESS and data else 0), res, err

    def read2(self, scs_id: int, address: int):
        data, res, err = self.readTxRx(scs_id, address, 2)
        val = (data[0] | (data[1] << 8)) if res == COMM_SUCCESS and len(data) == 2 else 0
        return val, res, err

    def write1(self, scs_id: int, address: int, value: int):
        return self.writeTxRx(scs_id, address, [value & 0xFF])

    def write2(self, scs_id: int, address: int, value: int):
        return self.writeTxRx(scs_id, address, [value & 0xFF, (value >> 8) & 0xFF])

    # sync write (positions/time/speed)
    def syncWrite(self, start_address: int, data_length: int, param: list[int]) -> int:
        tx_len = len(param) + 8
        tx = [0] * tx_len
        tx[PKT_ID] = BROADCAST_ID
        tx[PKT_LENGTH] = len(param) + 4
        tx[PKT_INSTRUCTION] = INST_SYNC_WRITE
        tx[PKT_PARAMETER0 + 0] = start_address
        tx[PKT_PARAMETER0 + 1] = data_length
        tx[PKT_PARAMETER0 + 2: PKT_PARAMETER0 + 2 + len(param)] = param
        _, res, _ = self.txRxPacket(tx)
        return res

    # --- decoding helpers ---
    def getTxRxResult(self, result: int) -> str:
        if result == COMM_SUCCESS:
            return "[TxRxResult] Communication success!"
        if result == COMM_PORT_BUSY:
            return "[TxRxResult] Port is in use!"
        if result == COMM_TX_FAIL:
            return "[TxRxResult] Failed transmit instruction packet!"
        if result == COMM_RX_FAIL:
            return "[TxRxResult] Failed get status packet from device!"
        if result == COMM_TX_ERROR:
            return "[TxRxResult] Incorrect instruction packet!"
        if result == COMM_RX_WAITING:
            return "[TxRxResult] Now receiving status packet!"
        if result == COMM_RX_TIMEOUT:
            return "[TxRxResult] RX Timeout (status packet)"
        if result == COMM_RX_CORRUPT:
            return "[TxRxResult] RX corrupt (status packet)"
        if result == COMM_NOT_AVAILABLE:
            return "[TxRxResult] Protocol does not support this function!"
        return ""

    def getRxPacketError(self, error: int) -> str:
        if error & ERRBIT_VOLTAGE:
            return "[ServoStatus] Input voltage error!"
        if error & ERRBIT_ANGLE:
            return "[ServoStatus] Angle sensor error!"
        if error & ERRBIT_OVERHEAT:
            return "[ServoStatus] Overheat error!"
        if error & ERRBIT_OVERELE:
            return "[ServoStatus] Over Electric error!"
        if error & ERRBIT_OVERLOAD:
            return "[ServoStatus] Overload error!"
        return ""


