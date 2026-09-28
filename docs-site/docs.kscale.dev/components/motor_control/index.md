<!-- preserved from https://docs.kscale.dev/components/motor_control via https://web.archive.org/web/20241111164837id_/https://docs.kscale.dev/components/motor_control -->

# Motor Control - K-Scale Docs

[Components](/components/mcu "Components")Motor Control

# Motor Control

There are multiple communication protocols that can be used to communicate with motors. Each protocol has its own advantages and is suited for different applications.

ℹ️

The choice of protocol depends on factors such as required speed, distance, noise immunity, and system complexity. Always consider the specific requirements of your application when selecting a communication protocol.

| Protocol | Type | Bitrate | Advantages | Common Uses |
| --- | --- | --- | --- | --- |
| CAN | Serial | 0.5-1.0Mbps | Robust, deterministic, multi-master | Vehicle systems, robotics |
| EtherCAT | Serial | 100Mbps | Real-time, high-speed, flexible topology | Factory automation, motion control |
| Modbus | Serial | 19.2kbps-115.2kbps | Simple, widely supported | HVAC, energy management |
| PROFIBUS | Serial | 9.6kbps-12Mbps | Deterministic, multi-master | Process automation, manufacturing |
| RS-485 | Serial | Up to 10Mbps | Long distance, multi-drop | Building automation, industrial control |
| SPI | Serial | Up to 50Mbps | Full-duplex, simple hardware | Sensor interfaces, local motor drivers |
| Ethernet/IP | Ethernet-based | 10/100/1000Mbps | Standard Ethernet hardware, flexible | Factory automation, process control |

[MCU](/components/mcu "MCU")[Cameras](/components/cameras "Cameras")
