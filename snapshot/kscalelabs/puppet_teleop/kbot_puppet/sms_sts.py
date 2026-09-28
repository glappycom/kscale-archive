from .protocol_packet_handler import (
    ProtocolPacketHandler,
    COMM_SUCCESS,
    INST_PING,
    BROADCAST_ID,
)


# Addresses (subset)
SMS_STS_ID = 5
SMS_STS_BAUD_RATE = 6
SMS_STS_TORQUE_ENABLE = 40
SMS_STS_ACC = 41
SMS_STS_GOAL_POSITION_L = 42
SMS_STS_GOAL_TIME_L = 44
SMS_STS_GOAL_SPEED_L = 46
SMS_STS_PRESENT_POSITION_L = 56
SMS_STS_LOCK = 55


def _lo(v: int) -> int:
    return v & 0xFF


def _hi(v: int) -> int:
    return (v >> 8) & 0xFF


class SMS_STS:
    def __init__(self, proto: ProtocolPacketHandler):
        self.p = proto

    # --- basic ops ---
    def ping(self, scs_id: int) -> tuple[bool, int]:
        tx = [0] * 6
        tx[2] = scs_id
        tx[3] = 2
        tx[4] = INST_PING
        rx, res, _ = self.p.txRxPacket(tx)
        return (res == COMM_SUCCESS and rx is not None), res

    def enable_torque(self, scs_id: int, enable: bool) -> tuple[int, int]:
        return self.p.write1(scs_id, SMS_STS_TORQUE_ENABLE, 1 if enable else 0)

    def write_position(self, scs_id: int, position: int, time_ms: int = 0, speed: int = 0) -> tuple[int, int]:
        data = [_lo(position), _hi(position), _lo(time_ms), _hi(time_ms), _lo(speed), _hi(speed)]
        return self.p.writeTxRx(scs_id, SMS_STS_GOAL_POSITION_L, data)

    def read_position(self, scs_id: int) -> tuple[int | None, int, int]:
        data, res, err = self.p.readTxRx(scs_id, SMS_STS_PRESENT_POSITION_L, 2)
        if res != COMM_SUCCESS or len(data) != 2:
            return None, res, err
        return data[0] | (data[1] << 8), res, err

    # --- group ops ---
    def sync_write_positions(self, moves: dict[int, tuple[int, int, int]]) -> int:
        # moves: id -> (pos, time_ms, speed)
        param: list[int] = []
        for sid, (pos, t, spd) in moves.items():
            param += [sid, _lo(pos), _hi(pos), _lo(t), _hi(t), _lo(spd), _hi(spd)]
        return self.p.syncWrite(SMS_STS_GOAL_POSITION_L, 6, param)

    # --- eeprom lock helpers ---
    def unlock_eeprom(self, scs_id: int) -> tuple[int, int]:
        return self.p.write1(scs_id, SMS_STS_LOCK, 0)

    def lock_eeprom(self, scs_id: int) -> tuple[int, int]:
        return self.p.write1(scs_id, SMS_STS_LOCK, 1)


