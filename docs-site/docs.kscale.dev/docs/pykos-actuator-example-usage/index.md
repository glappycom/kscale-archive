<!-- preserved from https://docs.kscale.dev/docs/pykos-actuator-example-usage via https://web.archive.org/web/20250621023418id_/https://docs.kscale.dev/docs/pykos-actuator-example-usage -->

# PyKOS Example Usage

The first step on receiving the prototype k-bot is to check the zeros. You can do this once installing `pykos` using the following command. Check the K-Bot section of the doc and make sure the CAN lines are connected to the CAN board and the usb c from the CAN board is plugging into the head.

You can also find the out-of-box actuator id to where the motor is on the K-Bot section of this doc.

**Read Motor**

Python

```
import pykos
import asyncio

async def main():
    async with pykos.KOS(0.0.0.0) as kos:
        print(await kos.actuator.get_actuators_state([25])) #for actuator ID 25

if __name__ == "__main__":
    asyncio.run(main())
```

**Set Zero in Current Place**

Python

```
import asyncio
import pykos

async def main():
    async with pykos.KOS() as kos:
        # for id in range(60):
            try:
                await kos.actuator.configure_actuator(actuator_id=id, torque_enabled=False, zero_position=True)
            except Exception as e:
                print(f"Failed to configure actuator {id}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Move Motor**

Controlling the actuator is as follows:

Python

```
import pykos
import asyncio

async def main():
    async with pykos.KOS() as kos:
        await kos.actuator.configure_actuator(actuator_id=13, kp=10, kd=1, torque_enabled=True)

        //

        await kos.actuator.command_actuators([{'actuator_id': id, 'position': -10}])

if __name__ == "__main__":
    asyncio.run(main())
```

We use actuators from [Robstride Dynamics](%5Bhttps://github.com/RobStride/Product_Information%5D(https://github.com/RobStride/Product_Information)). The control mode we use is the 'Operation control mode' which is described at the end of the manual. Thus, we can also pass in an expected velocity as such:

Python

```
import pykos
import asyncio

async def main():
    async with pykos.KOS() as kos:
        await kos.actuator.configure_actuator(actuator_id=13, kp=10, kd=1, torque_enabled=True)

        //

        await kos.actuator.command_actuators([{'actuator_id': id, 'velocity':10.0, 'position': -10}])

if __name__ == "__main__":
    asyncio.run(main())
```

Updated 25 days ago

---

[K-OS](/docs/kos)[Software Developer Kit](/docs/kos-sdk)

Ask AI
