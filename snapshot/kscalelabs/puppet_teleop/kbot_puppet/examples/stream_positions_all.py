import asyncio
import time

from kbot_puppet import FT_HAL
from kbot_puppet.utils.feetech_scan import scan_actuators


async def stream_positions_all(
    port: str = "/dev/ttyACM0",
    baudrate: int = 1_000_000,
    rate_hz: float = 50.0,
):
    actuators = await scan_actuators(port=port, baudrate=baudrate)
    ids = [a["id"] for a in actuators]
    if not ids:
        print("No actuators detected.")
        return

    kd = FT_HAL(port=port, actuator_ids=ids, baudrate=baudrate, auto_torque=False)
    try:
        # Ensure torque is disabled for all scanned IDs to reduce holding torque.
        # Do this sequentially to avoid bus contention (PORT_BUSY) on concurrent writes.
        for sid in ids:
            await kd.actuator.configure_actuator(sid, torque_enabled=False)

        dt = 1.0 / rate_hz
        t0 = time.perf_counter()
        iteration = 0

        while True:
            # Always read and print all initially scanned IDs
            resp = await kd.actuator.read_positions(ids)
            readings = [(s.actuator_id, s.position_deg) for s in resp.states]

            t = time.perf_counter() - t0
            parts: list[str] = [f"t={t:6.3f}s"]
            for sid, deg in readings:
                if deg is None:
                    parts.append(f"id {sid}: None")
                else:
                    parts.append(f"id {sid}: {deg:6.2f}°")
            print(" | ".join(parts), flush=True)

            iteration += 1
            next_tick = t0 + (iteration * dt)
            await asyncio.sleep(max(0.0, next_tick - time.perf_counter()))
    finally:
        await kd.close()


async def main():
    await stream_positions_all(
        port="/dev/ttyACM0",
        baudrate=1_000_000,
        rate_hz=50.0,
    )


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()


