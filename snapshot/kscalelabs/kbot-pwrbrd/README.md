# kbot-pwrbrd

A Rust library for interfacing with the K-Bot power board over CAN.

## Usage

```rust
use kbot_pwrbrd::PowerBoard;

if let board = PowerBoard::new("can0").is_ok() {
    println!("Board initialized successfully");
} else {
    println!("Failed to initialize board");
}
```
