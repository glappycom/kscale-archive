import asyncio
import time
from typing import Iterable

from kbot_puppet import FT_HAL

async def stream_positions(
    port: str = "/dev/ttyACM0",
    actuator_ids: list[int] = [1, 2, 3],
    rate_hz: float = 50.0,
):
    kd = FT_HAL(port=port, actuator_ids=actuator_ids, auto_torque=False)
    try:
        resp = await kd.actuator.get_actuators_state()
        ids = [s.actuator_id for s in resp.states]
        if not ids:
            print("No actuators detected.")
            return

        dt = 1.0 / rate_hz
        t0 = time.perf_counter()
        iteration = 0

        while True:
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
    await stream_positions(
        port="/dev/ttyACM0",
        actuator_ids=[1, 2, 3],
        rate_hz=50.0,
    )


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()


