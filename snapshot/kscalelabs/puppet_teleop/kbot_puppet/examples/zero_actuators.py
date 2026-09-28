#!/usr/bin/env python3
import argparse
import asyncio
from kbot_puppet import FT_HAL
from kbot_puppet.utils.feetech_scan import scan_actuators


async def main():
    p = argparse.ArgumentParser(description="Zero Feetech actuators (min=0, max=4095, position mode, torque 0x80)")
    p.add_argument("--device", default="/dev/ttyACM0")
    p.add_argument("--baudrate", type=int, default=1_000_000)
    p.add_argument("--ids", type=str, required=True, help="comma-separated list or 'scan' to auto-discover")
    args = p.parse_args()

    if args.ids.lower() == "scan":
        print("Scanning for actuators...")
        actuators = await scan_actuators(args.device, args.baudrate)
        actuator_ids = [a["id"] for a in actuators]
        if not actuator_ids:
            print("No actuators found!")
            return
        print(f"Found actuators: {actuator_ids}")
    else:
        actuator_ids = [int(x.strip()) for x in args.ids.split(",") if x.strip()]

    kd = FT_HAL(port=args.device, actuator_ids=actuator_ids, baudrate=args.baudrate)
    try:
        for aid in actuator_ids:
            await kd.actuator.configure_actuator(aid, zero_position=True)
            await asyncio.sleep(0.2)
    finally:
        await kd.close()


def cli_main():
    """Entry point for console script"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()


