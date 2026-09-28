import asyncio
import math
import time

from kbot_puppet import FT_HAL
from kbot_puppet.utils.feetech_scan import scan_actuators

async def multi_sine_wave(
    port: str = "/dev/ttyACM0",
    actuator_ids: list[int] | None = None,
    center_deg: float = 0.0,
    amplitude_deg: float = 30.0,
    freq_hz: float = 0.5,
    rate_hz: float = 50.0,
    kp: int | None = None,
    kd: int | None = None,
    acceleration: int | None = None,
    torque_enabled: bool = True,
    per_id_phase_deg: dict[int, float] | None = None,
):
    # If no specific IDs provided, scan for all available actuators
    if actuator_ids is None:
        print("Scanning for actuators...")
        actuators = await scan_actuators(port)
        if not actuators:
            print("No actuators found!")
            return
        available_ids = [a["id"] for a in actuators]
        print(f"Found actuators: {available_ids}")
    else:
        # Use provided IDs but verify they exist
        print(f"Looking for specific actuators: {actuator_ids}")
        actuators = await scan_actuators(port)
        all_available = [a["id"] for a in actuators]
        available_ids = [aid for aid in actuator_ids if aid in all_available]
        
        if not available_ids:
            print(f"None of the specified actuators {actuator_ids} were found!")
            print(f"Available actuators: {all_available}")
            return
            
        missing_ids = set(actuator_ids) - set(available_ids)
        if missing_ids:
            print(f"Warning: Expected actuators {list(missing_ids)} not found!")
        print(f"Using actuators: {available_ids}")

    hal = FT_HAL(port=port, actuator_ids=available_ids)
    try:
        # Configure all actuators
        for actuator_id in available_ids:
            await hal.actuator.configure_actuator(
                actuator_id,
                kp=kp,
                kd=kd,
                acceleration=acceleration,
                torque_enabled=torque_enabled,
                zero_position=True
            )

        # Warm start at center
        dt = 1.0 / rate_hz
        step_time_ms = max(1, int(dt * 1000))
        max_amp = max(0.0, min(amplitude_deg, 180.0 - abs(center_deg)))
        commands = [{"actuator_id": aid, "position": center_deg, "time_ms": 250} for aid in available_ids]
        await hal.actuator.command_actuators(commands)
        await asyncio.sleep(1.0)

        t0 = time.perf_counter()
        next_tick = t0
        while True:
            now = time.perf_counter()
            t = now - t0

            commands = []
            for aid in available_ids:
                phase_deg = 0.0
                if per_id_phase_deg and aid in per_id_phase_deg:
                    phase_deg = per_id_phase_deg[aid]
                angle = center_deg + max_amp * math.sin(2.0 * math.pi * freq_hz * t + math.radians(phase_deg))
                angle = max(-180.0, min(180.0, angle))
                commands.append({"actuator_id": aid, "position": angle, "time_ms": step_time_ms})
            await hal.actuator.command_actuators(commands)

            # advance to next tick and sleep
            next_tick += dt
            await asyncio.sleep(max(0.0, next_tick - time.perf_counter()))
    finally:
        await hal.close()

async def main():
    await multi_sine_wave(
        port="/dev/ttyACM0",
        actuator_ids=[11, 12],
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
