#!/usr/bin/env python3
"""
Example showing the new workflow:
1. Scan for actuators
2. Use explicit IDs in FT_HAL
"""
import asyncio
from kbot_puppet import FT_HAL
from kbot_puppet.utils.feetech_scan import scan_actuators

async def main():
    port = "/dev/ttyACM0"
    
    # Step 1: Scan for actuators
    print("Scanning for actuators...")
    actuators = await scan_actuators(port)
    
    if not actuators:
        print("No actuators found!")
        return
    
    # Step 2: Extract IDs
    actuator_ids = [a["id"] for a in actuators]
    print(f"Using actuator IDs: {actuator_ids}")
    
    # Step 3: Use explicit IDs with FT_HAL
    kd = FT_HAL(port=port, actuator_ids=actuator_ids)
    try:
        # Configure all actuators
        for aid in actuator_ids:
            await kd.actuator.configure_actuator(aid, torque_enabled=True)
        
        # Move all to center position
        commands = [
            {"actuator_id": aid, "position": 0.0}
            for aid in actuator_ids
        ]
        await kd.actuator.command_actuators(commands)
        
        print("Moved all actuators to 0 degrees")
        
    finally:
        await kd.close()

def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
