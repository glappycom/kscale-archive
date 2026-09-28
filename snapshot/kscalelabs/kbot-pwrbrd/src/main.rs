use kbot_pwrbrd::{PowerBoard, PowerBoardFrame};
use std::thread;
use std::time::{Duration, Instant};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let board = PowerBoard::new("can0")?;
    board.configure_board()?;

    // Store latest frame data and timestamps
    let mut latest_general = None;
    let mut latest_limbs = None;
    let mut general_time = None;
    let mut limbs_time = None;

    // Clear screen once at start
    print!("\x1B[2J\x1B[1;1H");

    loop {
        if let Some(frame) = board.read_frame()? {
            match frame {
                PowerBoardFrame::General(status) => {
                    latest_general = Some(status);
                    general_time = Some(Instant::now());
                }
                PowerBoardFrame::Limbs(status) => {
                    latest_limbs = Some(status);
                    limbs_time = Some(Instant::now());
                }
                PowerBoardFrame::Unknown(id, data) => {
                    println!("Received unhandled frame: 0x{:X} {:?}", id, data);
                }
            }
        }

        // Move cursor to top-left and print both frames
        print!("\x1B[1;1H");
        println!("=== Power Board Status ===");
        println!("┌──────────────────────────┐  ┌──────────────────────────┐");
        
        if let Some(general) = &latest_general {
            println!("│     General Status      │  │      Limbs Status       │");
            println!("│ Last update: {:4}ms    │  │ Last update: {:4}ms    │",
                    general_time.map_or(9999, |t| t.elapsed().as_millis().min(9999)),
                    limbs_time.map_or(9999, |t| t.elapsed().as_millis().min(9999)));
            println!("│ Battery: {:6.2} V      │  │ Left Leg:  {:6.2} W    │", 
                    general.battery_voltage,
                    latest_limbs.as_ref().map_or(0.0, |l| l.left_leg_power));
            println!("│ Motor:   {:6.2} V      │  │ Right Leg: {:6.2} W    │", 
                    general.motor_voltage,
                    latest_limbs.as_ref().map_or(0.0, |l| l.right_leg_power));
            println!("│ Current: {:6.2} A      │  │ Left Arm:  {:6.2} W    │", 
                    general.current,
                    latest_limbs.as_ref().map_or(0.0, |l| l.left_arm_power));
            println!("│ Faults:  0x{:04X}       │  │ Right Arm: {:6.2} W    │", 
                    general.fault_raw,
                    latest_limbs.as_ref().map_or(0.0, |l| l.right_arm_power));
        } else {
            println!("│     Waiting for data    │  │     Waiting for data    │");
        }
        
        println!("└──────────────────────────┘  └──────────────────────────┘");
        
        thread::sleep(Duration::from_millis(100));
    }
}
