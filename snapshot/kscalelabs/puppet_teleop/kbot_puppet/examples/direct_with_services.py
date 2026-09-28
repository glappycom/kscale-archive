# from . import PortHandler, ProtocolPacketHandler, SMS_STS

# ph = PortHandler(port_name="/dev/ttyACM0", baudrate=1_000_000)
# ph.openPort()
# pp = ProtocolPacketHandler(ph)
# sms = SMS_STS(pp)

# ok, res = sms.ping(1)
# assert ok, f"Servo 1 ping failed (res={res})"

# sms.enable_torque(1, True)
# sms.write_position(1, position=1500, time_ms=0, speed=0)
# pos, res, err = sms.read_position(1)
# print("pos:", pos)
# sms.sync_write_positions({1: (1500, 0, 0), 2: (1200, 0, 0)})

# ph.closePort()

