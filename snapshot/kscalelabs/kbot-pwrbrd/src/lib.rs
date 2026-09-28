use socketcan::{CanSocket, Socket, CanFrame, ExtendedId, EmbeddedFrame, CanError, Id};
use std::error::Error;
use std::time::Duration;
use serde::{Serialize, Deserialize};
pub struct PowerBoard {
    socket: CanSocket,
}


/// Builds a 29-bit arbitration ID from:
///  - `target_address` (lowest 8 bits)
///  - `comm_type` (next 13 bits)
///  - `reserved` (top 8 bits)
fn arbitration_id(target_address: u8, comm_type: u16, reserved: u8) -> Option<ExtendedId> {
    // bits 0..7   -> target_address
    // bits 8..20  -> comm_type
    // bits 21..28 -> reserved
    let arbitration_id = (target_address as u32 & 0xFF)
        | ((comm_type as u32 & 0x1FFF) << 8)
        | ((reserved as u32 & 0xFF) << 21);

    ExtendedId::new(arbitration_id)
}

/// 0x1003: Status Frame structure.
/// Mirrors the Python logic:
///  - battery_voltage (bytes 0..1)
///  - motor_voltage   (bytes 2..3)
///  - current         (bytes 4..5)
///  - fault_raw       (bytes 6..7), plus bitfield flags
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PowerBoardGeneralFrame {
    pub battery_voltage: f32,
    pub motor_voltage: f32,
    pub current: f32,
    pub fault_raw: u16,
    pub power_chip_oc: bool,
    pub power_chip_ot: bool,
    pub power_chip_sc: bool,
    pub sampling_oc: bool,
    pub vbus_ov: bool,
    pub vbus_uv: bool,
    pub vmbus_ov: bool,
    pub vmbus_uv: bool,
    pub raw_data: Vec<u8>,
}

/// 0x1004: Status Frame structure.
///  - left_leg_power  (bytes 0..1)
///  - right_leg_power (bytes 2..3)
///  - left_arm_power  (bytes 4..5)
///  - right_arm_power (bytes 6..7)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PowerBoardLimbFrame {
    pub left_leg_power: f32,
    pub right_leg_power: f32,
    pub left_arm_power: f32,
    pub right_arm_power: f32,
    pub raw_data: Vec<u8>,
}

/// An enum to represent "parsed" power board frames.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum PowerBoardFrame {
    General(PowerBoardGeneralFrame), // 0x1003
    Limbs(PowerBoardLimbFrame),     // 0x1004
    Unknown(u32, Vec<u8>),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ControlCommand {
    pub fan: bool,
    pub pre_charge: bool,
    pub motor: bool,
    pub main: bool,
    pub restart: bool,
    pub clear_fault: bool,
    pub auto_report: bool,
    pub reserved: bool,
}

impl PowerBoard {
    pub fn new(interface: &str) -> Result<Self, Box<dyn Error>> {
        let socket = CanSocket::open(interface)?;
        socket.set_read_timeout(Duration::from_millis(100))?;
        Ok(Self { socket })
    }

    /// Configures the board to enable auto-reporting and normal operation.
    pub fn configure_board(&self) -> Result<(), Box<dyn Error>> {
        let command = ControlCommand {
            fan: false,
            pre_charge: true,
            motor: true,
            main: true,
            restart: false,
            clear_fault: false,
            auto_report: true,
            reserved: false,
        };
        self.send_control_frame(&command)?;
        Ok(())
    }

    pub fn configure_and_clear_faults(&self) -> Result<(), Box<dyn Error>> {
        let command = ControlCommand {
            fan: false,
            pre_charge: true,
            motor: true,
            main: true,
            restart: false,
            clear_fault: true,
            auto_report: true,
            reserved: false,
        };
        self.send_control_frame(&command)?;
        Ok(())
    }

    /// Sends a 0x1001 Control Frame to enable auto-reporting on the power board.
    /// 
    /// Byte layout (0..7):
    ///     Byte0: 1/0 -> Fan
    ///     Byte1: 1/0 -> Pre-charge
    ///     Byte2: 1/0 -> Motor output
    ///     Byte3: 1/0 -> Main control
    ///     Byte4: 1/0 -> Restart
    ///     Byte5: 1/0 -> Clear fault
    ///     Byte6: 1/0 -> Auto-report data (100ms)
    ///     Byte7: 1/0 -> Reserved
    pub fn send_control_frame(&self, command: &ControlCommand) -> Result<(), Box<dyn Error>> {
        let target_address = 0xAA; // Should be 0xAA for all power boards
        let comm_type = 0x1001; // Control code
        let reserved = 0x00;

        // Build the 29-bit extended ID
        let id = arbitration_id(target_address, comm_type, reserved)
            .ok_or("Invalid 29-bit ID for control frame")?;

        let data = [command.fan as u8, command.pre_charge as u8, command.motor as u8, command.main as u8, command.restart as u8, command.clear_fault as u8, command.auto_report as u8, command.reserved as u8];

        // Construct the extended CAN frame
        let frame = CanFrame::new(id, &data)
            .ok_or("Failed to create 0x1001 control CAN frame")?;

        // Send
        self.socket.write_frame(&frame)?;
        tracing::info!("Sent 0x1001 Control Frame with command: {:?}", command);
        Ok(())
    }

    /// Parse a single incoming CAN frame as a power board message.
    /// Returns `None` if the frame is not extended or data is invalid.
    pub fn parse_power_board_message(frame: &CanFrame) -> Option<PowerBoardFrame> {
        // Must be an extended ID
        let id = frame.id();
        if !matches!(id, Id::Extended(_)) {
            // Not a 29-bit ID
            return None;
        }

        // Extract the raw 29-bit arbitration ID
        let arbitration_id = match id {
            Id::Extended(ext_id) => ext_id.as_raw(),
            _ => return None,
        };

        // Bits [0..7]:   target_address
        // Bits [8..20]:  comm_type
        // Bits [21..28]: reserved
        let target_address = (arbitration_id & 0xFF) as u8;
        let comm_type = ((arbitration_id >> 8) & 0x1FFF) as u16;
        let _reserved = ((arbitration_id >> 21) & 0xFF) as u8;

        let data = frame.data();
        if data.len() < 8 {
            // Not enough data to parse
            return None;
        }

        // Dispatch based on comm_type
        match comm_type {
            0x1003 => {
                // parse 0x1003 frame
                Some(PowerBoardFrame::General(parse_status_frame_1003(data)))
            }
            0x1004 => {
                // parse 0x1004 frame
                Some(PowerBoardFrame::Limbs(parse_limb_power_frame(data)))
            }
            _ => {
                // Unknown or not implemented
                Some(PowerBoardFrame::Unknown(arbitration_id, data.to_vec()))
            }
        }
    }

    /// Example of reading a single frame from the CAN socket and parsing it.
    pub fn read_frame(&self) -> Result<Option<PowerBoardFrame>, Box<dyn Error>> {
        let frame = match self.socket.read_frame() {
            Ok(f) => f,
            Err(e) if e.kind() == std::io::ErrorKind::WouldBlock => {
                // Timed out (no frame within read_timeout)
                return Ok(None);
            }
            Err(e) => return Err(Box::new(e)),
        };
        Ok(Self::parse_power_board_message(&frame))
    }
}

/// Parse the 0x1003 data payload into `PowerBoardGeneralFrame`.
fn parse_status_frame_1003(data: &[u8]) -> PowerBoardGeneralFrame {
    // Byte0-1: Battery Voltage (big-endian, /100)
    let battery_voltage_raw = ((data[0] as u16) << 8) | (data[1] as u16);
    let battery_voltage = battery_voltage_raw as f32 / 100.0;

    // Byte2-3: Motor Voltage (big-endian, /100)
    let motor_voltage_raw = ((data[2] as u16) << 8) | (data[3] as u16);
    let motor_voltage = motor_voltage_raw as f32 / 100.0;

    // Byte4-5: Current (big-endian, /100)
    let current_raw = ((data[4] as u16) << 8) | (data[5] as u16);
    let current = current_raw as f32 / 100.0;

    // Byte6-7: Fault Status (bitfield)
    let fault_raw = ((data[6] as u16) << 8) | (data[7] as u16);

    PowerBoardGeneralFrame {
        battery_voltage,
        motor_voltage,
        current,
        fault_raw,
        power_chip_oc: (fault_raw & (1 << 0)) != 0,
        power_chip_ot: (fault_raw & (1 << 1)) != 0,
        power_chip_sc: (fault_raw & (1 << 2)) != 0,
        sampling_oc:   (fault_raw & (1 << 3)) != 0,
        vbus_ov:       (fault_raw & (1 << 4)) != 0,
        vbus_uv:       (fault_raw & (1 << 5)) != 0,
        vmbus_ov:      (fault_raw & (1 << 6)) != 0,
        vmbus_uv:      (fault_raw & (1 << 7)) != 0,
        raw_data: data.to_vec(),
    }
}

/// Parse the 0x1004 data payload into `PowerBoardLimbFrame`.
fn parse_limb_power_frame(data: &[u8]) -> PowerBoardLimbFrame {
    let left_leg_raw = ((data[0] as u16) << 8) | (data[1] as u16);
    let left_leg_power = left_leg_raw as f32 / 100.0;

    let right_leg_raw = ((data[2] as u16) << 8) | (data[3] as u16);
    let right_leg_power = right_leg_raw as f32 / 100.0;

    let left_arm_raw = ((data[4] as u16) << 8) | (data[5] as u16);
    let left_arm_power = left_arm_raw as f32 / 100.0;

    let right_arm_raw = ((data[6] as u16) << 8) | (data[7] as u16);
    let right_arm_power = right_arm_raw as f32 / 100.0;

    PowerBoardLimbFrame {
        left_leg_power,
        right_leg_power,
        left_arm_power,
        right_arm_power,
        raw_data: data.to_vec(),
    }
}
