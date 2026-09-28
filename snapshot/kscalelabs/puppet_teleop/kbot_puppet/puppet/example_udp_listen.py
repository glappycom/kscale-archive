#!/usr/bin/env python3
import argparse
import json
import socket
import time
from typing import Dict, List


FIELD_MAPPING_18: Dict[str, int] = {
    "XVel": 0,
    "YVel": 1,
    "YawRate": 2,
    "BaseHeight": 3,
    "BaseRoll": 4,
    "BasePitch": 5,
    "RShoulderPitch": 6,
    "RShoulderRoll": 7,
    "RElbowPitch": 8,
    "RElbowRoll": 9,
    "RWristRoll": 10,
    "RWristGripper": 11,
    "LShoulderPitch": 12,
    "LShoulderRoll": 13,
    "LElbowPitch": 14,
    "LElbowRoll": 15,
    "LWristRoll": 16,
    "LWristGripper": 17,
}


def _format_vector(values: List[float]) -> str:
    return ", ".join(f"{v:+.4f}" for v in values)


def listen_udp(host: str, port: int, length: int, timeout_s: float) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.settimeout(timeout_s)

    cmd: List[float] = [0.0 for _ in range(length)]
    print(f"Listening on {host}:{port} for JSON UDP; vector length={length}")
    print("Accepts either named 18-field payloads or index-based {\"commands\": {\"i\": value}}")

    t0 = time.perf_counter()
    try:
        while True:
            try:
                data, addr = sock.recvfrom(65536)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break

            try:
                payload = json.loads(data.decode("utf-8"))
            except Exception:
                continue

            if isinstance(payload, list):
                # Plain array payload
                for i, v in enumerate(payload):
                    if i < length:
                        try:
                            cmd[i] = float(v)
                        except Exception:
                            continue
            elif isinstance(payload, dict) and payload.get("type") == "reset":
                cmd = [0.0 for _ in range(length)]
            elif isinstance(payload, dict) and "commands" in payload and isinstance(payload["commands"], dict):
                # Index-based payload
                for k, v in payload["commands"].items():
                    try:
                        i = int(k)
                        if 0 <= i < length:
                            cmd[i] = float(v)
                    except Exception:
                        continue
            elif isinstance(payload, dict):
                # Named 18-field payload
                for name, idx in FIELD_MAPPING_18.items():
                    if idx < length and name in payload:
                        try:
                            cmd[idx] = float(payload[name])
                        except Exception:
                            continue

            t = time.perf_counter() - t0
            print(f"t={t:7.3f}s | [{_format_vector(cmd)}]")
    finally:
        sock.close()


def main() -> None:
    p = argparse.ArgumentParser(description="Example UDP listener for kbot_puppet commands")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=10000)
    p.add_argument("--length", type=int, default=18, help="Command vector length (16 or 18)")
    p.add_argument("--timeout", type=float, default=0.1, help="Socket timeout seconds")
    args = p.parse_args()

    listen_udp(host=args.host, port=args.port, length=args.length, timeout_s=args.timeout)


def cli_main() -> None:
    main()


if __name__ == "__main__":
    cli_main()


