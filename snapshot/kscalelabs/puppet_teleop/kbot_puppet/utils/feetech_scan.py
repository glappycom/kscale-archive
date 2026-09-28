#!/usr/bin/env python3
"""
Feetech actuator scanner utility.
Scans all possible IDs (1-253) to find which actuators are connected to the bus.
"""
import asyncio
import time
from typing import List, Dict

from kbot_puppet.port_handler import PortHandler
from kbot_puppet.protocol_packet_handler import ProtocolPacketHandler
from kbot_puppet.sms_sts import SMS_STS


async def scan_actuators(port: str = "/dev/ttyACM0", baudrate: int = 1_000_000) -> List[Dict]:
    """
    Scan all possible actuator IDs to find which ones are connected.
    
    Args:
        port: Serial port path
        baudrate: Communication baudrate
        
    Returns:
        List of dictionaries with actuator info: [{"id": int, "model": str}, ...]
    """
    print(f"Scanning for actuators on {port} at {baudrate} baud...")
    
    ph = PortHandler(port, baudrate)
    ph.openPort()
    proto = ProtocolPacketHandler(ph)
    sms = SMS_STS(proto)
    
    found_actuators = []
    
    try:
        start_time = time.time()
        
        # Scan all possible IDs (1-253, skip 0 and 254 as they're reserved)
        for actuator_id in range(1, 254):
            if actuator_id % 50 == 0:
                print(f"Scanning ID {actuator_id}...")
            
            def _ping_blocking() -> bool:
                ok, _ = sms.ping(actuator_id)
                return ok
            
            ok = await asyncio.to_thread(_ping_blocking)
            
            if ok:
                def _get_model_blocking() -> str:
                    try:
                        val, res, err = proto.read2(actuator_id, 3)
                        if res == 0:
                            return f"Model_{val}"
                        return "Unknown"
                    except Exception:
                        return "Unknown"

                model = await asyncio.to_thread(_get_model_blocking)

                found_actuators.append({"id": actuator_id, "model": model})
                print(f"Found actuator ID {actuator_id}: {model}")
        
        scan_time = time.time() - start_time
        print(f"\nScan complete in {scan_time:.1f}s")
        print(f"Found {len(found_actuators)} actuators:")
        
        for actuator in found_actuators:
            print(f"  ID {actuator['id']}: {actuator['model']}")
            
    finally:
        ph.closePort()
    
    return found_actuators


async def main():
    """Command line interface for the scanner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan for Feetech actuators on serial bus")
    parser.add_argument("--port", "-p", default="/dev/ttyACM0", help="Serial port (default: /dev/ttyACM0)")
    parser.add_argument("--baudrate", "-b", type=int, default=1_000_000, help="Baudrate (default: 1000000)")
    parser.add_argument("--ids-only", action="store_true", help="Only print actuator IDs (for scripting)")
    
    args = parser.parse_args()
    
    try:
        actuators = await scan_actuators(args.port, args.baudrate)
        
        if args.ids_only:
            # Print just the IDs for easy parsing by other scripts
            ids = [str(a["id"]) for a in actuators]
            print(",".join(ids))
        else:
            if actuators:
                print(f"\nActuator IDs found: {[a['id'] for a in actuators]}")
                print("Use these IDs in your scripts!")
            else:
                print("\nNo actuators found. Check connections and baudrate.")
                
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
    except Exception as e:
        print(f"Error during scan: {e}")


def cli_main():
    """Synchronous entry point for CLI"""
    asyncio.run(main())

if __name__ == "__main__":
    cli_main()
