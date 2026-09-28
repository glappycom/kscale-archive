#!/usr/bin/env python3
import argparse
import asyncio
from kbot_puppet import FT_HAL
from kbot_puppet.utils.feetech_scan import scan_actuators


async def main():
    p = argparse.ArgumentParser(description="Change baudrate for all detected Feetech servos")
    p.add_argument("--device", default="/dev/ttyACM0")
    p.add_argument("--current-baudrate", type=int, default=1_000_000)
    p.add_argument("--new-baudrate", type=int, required=True, choices=[1_000_000, 500_000, 250_000])
    args = p.parse_args()

    # First scan for actuators
    print("Scanning for actuators...")
    actuators = await scan_actuators(args.device, args.current_baudrate)
    
    if not actuators:
        print("No actuators found!")
        return
    
    ids = [a["id"] for a in actuators]
    print(f"Found actuators: {ids}")

    kd = FT_HAL(port=args.device, actuator_ids=ids, baudrate=args.current_baudrate)
    try:
        # Map actual baud → register index
        baud_to_index = {1_000_000: 0, 500_000: 1, 250_000: 2}
        idx = baud_to_index[args.new_baudrate]

        # Write EEPROM per-id (unlock, set, lock)
        async def write_one(aid: int):
            def _block():
                sms = kd._sms
                sms.unlock_eeprom(aid)
                sms.p.write1(aid, 6, idx)  # SMS_STS_BAUD_RATE
                sms.lock_eeprom(aid)
            await asyncio.to_thread(_block)

        await asyncio.gather(*[write_one(a) for a in ids])
        print(f"Changed baudrate to {args.new_baudrate} for actuators: {ids}")
    finally:
        await kd.close()


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()


