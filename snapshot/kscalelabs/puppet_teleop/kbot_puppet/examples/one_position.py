import asyncio
from kbot_puppet import FT_HAL


async def main():
    kd = FT_HAL(port="/dev/ttyACM0", actuator_ids=[1, 2, 3])
    try:
        states = await kd.actuator.get_actuators_state()
        print(states)
        
        # Configure actuator and enable torque
        print("Configuring actuator 1...")
        await kd.actuator.configure_actuator(1, torque_enabled=True)
        await asyncio.sleep(0.1)  # Brief delay after configuration
        
        await kd.actuator.command_actuators([
            {"actuator_id": 1, "position": 20.0},
        ])
    finally:
        await kd.close()


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()