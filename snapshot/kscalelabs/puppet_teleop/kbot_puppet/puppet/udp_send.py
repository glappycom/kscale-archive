#!/usr/bin/env python3
import argparse
import asyncio
import json
import math
import socket
import time
from typing import Dict, List, Optional

from kbot_puppet import FT_HAL

#! Flip sign 22 and 12, 13 and 23, 15 and 25. 

SIGN_FLIP_SERVO_IDS = {12, 13, 15, 22, 23, 25}

FIELD_MAPPING_18: Dict[str, int] = {
    "XVel": 0,
    "YVel": 1,
    "YawRate": 2,
    "BaseHeight": 3,
    "BaseRoll": 4,
    "BasePitch": 5,
    "RShoulderPitch": 6,
    "RShoulderRoll": 7,
    "RShoulderYaw": 8,
    "RElbowPitch": 9,
    "RWrist": 10,
    "LShoulderPitch": 11,
    "LShoulderRoll": 12,
    "LShoulderYaw": 13,
    "LElbowPitch": 14,
    "LWrist": 15,
}

SERVO_ID_TO_FIELD_18: Dict[int, str] = {
    # Right arm
    21: "RShoulderPitch",
    22: "RShoulderRoll",
    23: "RShoulderYaw",
    24: "RElbowPitch",
    25: "RWrist",
    # Left arm
    11: "LShoulderPitch",
    12: "LShoulderRoll",
    13: "LShoulderYaw",
    14: "LElbowPitch",
    15: "LWrist",
}

async def stream_and_send_udp(
    device: str,
    baudrate: int,
    ids: List[int],
    rate_hz: float,
    host: str,
    port: int,
    length: int,
    send_named: bool,
):
    ids_for_hal = sorted(set(ids or []).union(SERVO_ID_TO_FIELD_18.keys()))
    hal: Optional[FT_HAL] = None
    if ids_for_hal:
        hal = FT_HAL(port=device, actuator_ids=ids_for_hal, baudrate=baudrate, auto_torque=False)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (host, port)

    try:
        dt = 1.0 / rate_hz
        t0 = time.perf_counter()
        iteration = 0

        print(
            f"Sending UDP to {host}:{port} at {rate_hz:.1f} Hz; length={length} ({'named' if send_named else 'indexed'})"
        )

        while True:
            # Read positions (degrees) and map to radians
            id_to_deg: Dict[int, float] = {}
            if hal is not None:
                resp = await hal.actuator.read_positions(list(SERVO_ID_TO_FIELD_18.keys()))
                for s in resp.states:
                    if s.position_deg is not None:
                        id_to_deg[s.actuator_id] = float(s.position_deg)

            if send_named and length == 18:
                # Send named fields as JSON object
                payload: Dict[str, float] = {name: 0.0 for name in FIELD_MAPPING_18}
                # Populate arm joints
                for servo_id, field_name in SERVO_ID_TO_FIELD_18.items():
                    deg = id_to_deg.get(servo_id)
                    if deg is not None:
                        rad = math.radians(deg)
                        if servo_id in SIGN_FLIP_SERVO_IDS:
                            rad = -rad
                        payload[field_name] = rad
                # Send as JSON object with field names
                message = json.dumps(payload).encode("utf-8")
            else:
                # Array mode: send as {"commands": [array]}
                vec = [0.0 for _ in range(length)]
                for servo_id, field_name in SERVO_ID_TO_FIELD_18.items():
                    idx = FIELD_MAPPING_18.get(field_name)
                    if idx is None or idx >= length:
                        continue
                    deg = id_to_deg.get(servo_id)
                    if deg is not None:
                        rad = math.radians(deg)
                        if servo_id in SIGN_FLIP_SERVO_IDS:
                            rad = -rad
                        vec[idx] = rad
                message = json.dumps({"commands": vec}).encode("utf-8")

            try:
                sock.sendto(message, addr)
            except Exception:
                pass

            iteration += 1
            next_tick = t0 + (iteration * dt)
            await asyncio.sleep(max(0.0, next_tick - time.perf_counter()))
    finally:
        if hal is not None:
            await hal.close()
        sock.close()


async def main():
    p = argparse.ArgumentParser(description="Send servo positions (radians) via UDP at a fixed rate")
    p.add_argument("--device", default="/dev/ttyACM0")
    p.add_argument("--baudrate", type=int, default=1_000_000)
    p.add_argument("--ids", type=str, default="scan", help="comma-separated list or 'scan'")
    p.add_argument("--rate-hz", type=float, default=50.0)
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=10000)
    p.add_argument("--length", type=int, default=18, help="command vector length (16 or 18)")
    p.add_argument("--named", action="store_true", help="send named fields when length==18")
    args = p.parse_args()

    ids: Optional[List[int]]
    if args.ids.lower() == "scan":
        ids = None
    else:
        ids = [int(x.strip()) for x in args.ids.split(",") if x.strip()]

    await stream_and_send_udp(
        device=args.device,
        baudrate=args.baudrate,
        ids=ids,
        rate_hz=args.rate_hz,
        host=args.host,
        port=args.port,
        length=args.length,
        send_named=bool(args.named),
    )


def cli_main():
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()

