#!/usr/bin/env python3
import argparse
import asyncio
from kbot_puppet import FT_HAL


async def main():
    p = argparse.ArgumentParser(description="Change a Feetech servo ID")
    p.add_argument("--device", default="/dev/ttyACM0")
    p.add_argument("--baudrate", type=int, default=1_000_000)
    p.add_argument("--current-id", type=int, required=True)
    p.add_argument("--new-id", type=int, required=True)
    args = p.parse_args()

    if not (0 <= args.current_id <= 253 and 0 <= args.new_id <= 253):
        raise SystemExit("IDs must be between 0 and 253")

    # Use the current ID as the only actuator ID for this operation
    kd = FT_HAL(port=args.device, actuator_ids=[args.current_id], baudrate=args.baudrate)
    try:
        def _block():
            sms = kd._sms
            sms.unlock_eeprom(args.current_id)
            sms.p.write1(args.current_id, 5, args.new_id)  # SMS_STS_ID
            sms.lock_eeprom(args.current_id)
        await asyncio.to_thread(_block)
        print(f"Changed actuator ID from {args.current_id} to {args.new_id}")
    finally:
        await kd.close()


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()


