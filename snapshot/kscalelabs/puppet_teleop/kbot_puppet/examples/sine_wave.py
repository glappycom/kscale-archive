# /Users/aaronxie/Documents/Code_Local/feetechs/kd_feetech/examples/sine_wave.py
import asyncio
import math
import time

from kbot_puppet import FT_HAL

async def sine_wave(
    port: str = "/dev/ttyACM0",
    actuator_id: int | None = None,
    center_deg: float = 0.0,
    amplitude_deg: float = 30.0,
    freq_hz: float = 0.5,
    rate_hz: float = 50.0,
):
    kd = FT_HAL(port=port, actuator_ids=[1, 11, 12, 13, 14, 15, 21, 22, 23, 24, 25])
    try:
        # Pick the first detected actuator if none specified
        if actuator_id is None:
            resp = await kd.actuator.get_actuators_state()
            if not resp.states:
                print("No actuators detected.")
                return
            actuator_id = resp.states[0].actuator_id

        # Configure actuator and enable torque
        print(f"Configuring actuator {actuator_id}...")
        await kd.actuator.configure_actuator(actuator_id, torque_enabled=True)
        await asyncio.sleep(0.1)  # Brief delay after configuration

        # Match move time to update rate for smooth interpolation
        dt = 1.0 / rate_hz
        step_time_ms = max(1, int(dt * 1000))

        # Ensure the wave stays within [-180, 180]
        max_amp = max(0.0, min(amplitude_deg, 180.0 - abs(center_deg)))

        t0 = time.perf_counter()
        while True:
            t = time.perf_counter() - t0
            angle = center_deg + max_amp * math.sin(2.0 * math.pi * freq_hz * t)
            angle = max(-180.0, min(180.0, angle))

            await kd.actuator.command_actuators([
                {"actuator_id": actuator_id, "position": angle, "time_ms": step_time_ms}
            ])

            # Sleep to maintain rate
            next_tick = t0 + (math.floor((t / dt) + 1) * dt)
            await asyncio.sleep(max(0.0, next_tick - time.perf_counter()))
    finally:
        await kd.close()

async def main():
    await sine_wave(
        port="/dev/ttyACM0",
        actuator_id=11,
        center_deg=0.0,
        amplitude_deg=30.0,
        freq_hz=0.5,
        rate_hz=50.0,
    )

def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()