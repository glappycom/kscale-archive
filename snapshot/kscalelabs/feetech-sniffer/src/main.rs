use std::error::Error;
use std::fs::File;
use std::io::{self, BufReader};
use csv::ReaderBuilder;
use serde::Serialize;
use csv::Writer;



#[derive(Debug)]
#[repr(u8)]
enum InstructionType {
    Ping = 0x01,
    Read = 0x02,
    Write = 0x03,
    RegWrite = 0x04,
    Action = 0x05,
    Reset = 0x06,
    SyncWrite = 0x83,
    Unknown(u8),
}

impl InstructionType {
    fn from_byte(b: u8) -> Self {
        match b {
            0x01 => InstructionType::Ping,
            0x02 => InstructionType::Read,
            0x03 => InstructionType::Write,
            0x04 => InstructionType::RegWrite,
            0x05 => InstructionType::Action,
            0x06 => InstructionType::Reset,
            0x83 => InstructionType::SyncWrite,
            other => InstructionType::Unknown(other),
        }
    }

    fn to_byte(&self) -> u8 {
        match self {
            InstructionType::Ping => 0x01,
            InstructionType::Read => 0x02,
            InstructionType::Write => 0x03,
            InstructionType::RegWrite => 0x04,
            InstructionType::Action => 0x05,
            InstructionType::Reset => 0x06,
            InstructionType::SyncWrite => 0x83,
            InstructionType::Unknown(b) => *b,
        }
    }

    fn as_str(&self) -> String {
        match self {
            InstructionType::Ping => "Ping".to_string(),
            InstructionType::Read => "Read".to_string(),
            InstructionType::Write => "Write".to_string(),
            InstructionType::RegWrite => "RegWrite".to_string(),
            InstructionType::Action => "Action".to_string(),
            InstructionType::Reset => "Reset".to_string(),
            InstructionType::SyncWrite => "SyncWrite".to_string(),
            InstructionType::Unknown(b) => format!("Unknown({:#X})", b),
        }
    }
}

#[derive(Debug)]
enum ChecksumType {
    Correct(u8),
    Incorrect {
        expected: u8,
        received: u8,
    },
}

impl std::fmt::Display for ChecksumType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ChecksumType::Correct(c) => write!(f, "Correct({:#X})", c),
            ChecksumType::Incorrect { expected, received } => {
                write!(f, "Incorrect(expected: {:#X}, received: {:#X})", expected, received)
            }
        }
    }
}

#[derive(Debug)]
struct InstructionPacket {
    start_time: f64,
    duration: f64,
    id: u8,
    length: u8,
    instruction_type: InstructionType,
    data: Vec<u8>,
    checksum: ChecksumType,
    raw: Vec<u8>,
}

#[derive(Debug)]
enum InstructionError {
    NotEnoughData,
    ChecksumMismatch,
    ChecksumMismatchAndNext,
    InvalidLength(u8),
    InvalidHeader,
    InvalidId(u8),
}


fn correct_header(byte_stream: &[TimestampedByte]) -> Result<usize, InstructionError> {
    // check first two bytes
    // return number of bites that are unset

    if byte_stream.len() < 2 {
        return Err(InstructionError::NotEnoughData);
    }
    
    let mut ret = 0usize;

    ret += 8usize - (byte_stream[0].byte.count_ones() as usize);
    ret += 8usize - (byte_stream[1].byte.count_ones() as usize);

    if ret > 0 {
        println!("Header correction: {} bits", ret);
    }
    Ok(ret)
}


fn closest_valid_id(id: u8) -> Result<(u8, usize), InstructionError> {
    // find the closest valid id to the given id
    // valid ids are 0x01 to 0x50 and 0xFE

    let valid_ids = [
        11..=14,
        21..=24,
        31..=34,
        41..=44,
        0xFE..=0xFE,
    ].into_iter().flatten().collect::<Vec<_>>();

    let mut min_flips = 8;
    let mut ret = 0xFF;
    for valid_id in valid_ids {
        let flips = valid_id ^ id;
        if flips.count_ones() < min_flips {
            min_flips = flips.count_ones();
            ret = valid_id;
        }
    }

    if id != ret {
        println!("ID correction: {:#02X} -> {:#02X}, corrections: {}", id, ret, min_flips);
    } else {
        println!("ID correction: {:#02X}, no corrections", id);
    }

    Ok((ret, min_flips as usize))
}


fn closest_valid_instruction(instruction: u8) -> Result<(InstructionType, usize), InstructionError> {
    // find the closest valid instruction to the given instruction
    // valid instructions are 0x01 to 0x06 and 0x83

    let valid_instructions = [
        0x00..=0x06,
        0x83..=0x83,
    ].into_iter().flat_map(|r| r).collect::<Vec<_>>();

    let mut min_flips = 8;
    let mut ret = InstructionType::Unknown(0);
    for valid_instruction in valid_instructions {
        let flips = valid_instruction ^ instruction;
        if flips.count_ones() < min_flips {
            min_flips = flips.count_ones();
            ret = InstructionType::from_byte(valid_instruction);
        }
    }
    
    if instruction != ret.to_byte() {
        println!("Instruction correction: {:#02X} -> {:#02X}, corrections: {}", instruction, ret.to_byte(), min_flips);
    } else {
        println!("Instruction correction: {:#02X}, no corrections", instruction);
    }
    println!("Instruction type: {:?}", ret);


    Ok((ret, min_flips as usize))
}



fn valid_packet_greedy(
    byte_stream: &[TimestampedByte]
) -> Result<(InstructionPacket, usize), InstructionError> {

    // check if bytestream has at least one packet
    if byte_stream.len() < 6 {
        return Err(InstructionError::NotEnoughData);
    }
    // find a valid packet at current position in the bytestream
    // with minimum number of bit flips

    let mut ret = 0usize;
    ret += correct_header(byte_stream)?;

    if ret > 0 {
        return Err(InstructionError::InvalidHeader);
    }

    let mut id = byte_stream[2].byte;
    let inc;
    (id, inc) = closest_valid_id(id)?;
    ret += inc;

    // we have the closest valid id
    let mut length = byte_stream[3].byte;
    let (instruction, mut inc) = closest_valid_instruction(byte_stream[4].byte)?;
    ret += inc;
    // based on the instruction, check if length is valid, if not correct it
    println!("raw length {}, corrections: {}", length, ret);
    inc = 0;
    length = match instruction {
        InstructionType::Read => {
            // length has to be 2 + 2, calculate bit flips
            let expected_length = 2 + 2;
            inc = (expected_length as u8 ^ length).count_ones() as usize;
            expected_length
        },
        _ => { length },
    };
    ret += inc;
    println!("corrected length {}, correction {}", length, ret);

    if byte_stream.len() < (2 + 1 + 1 + length as usize) {
        return Err(InstructionError::InvalidLength(length));
    }
    let param_len = length as usize - 2; // instruction (1) + checksum (1)
    let parameters = byte_stream[5..5 + param_len].to_vec();

    let calc_crc = calc_checksum(
        id,
        length,
        instruction.to_byte(),
        &parameters,
    );

    let read_crc = byte_stream[4 + length as usize - 1].byte;
    // since we have fixed everything, we can correct checksum

    let checksum_type = if calc_crc != read_crc {
        ret += (calc_crc ^ read_crc).count_ones() as usize;
        ChecksumType::Incorrect {
            expected: calc_crc,
            received: read_crc,
        }
    } else {
        ChecksumType::Correct(calc_crc)
    };
    let raw = byte_stream[0..(2 + 1 + 1 + length as usize)].to_vec();

    let duration: f64 = raw.iter().map(|b| b.duration).sum();
    Ok((InstructionPacket {
        start_time: byte_stream[0].start_time,
        duration,
        id,
        length,
        instruction_type: instruction,
        data: parameters.iter().map(|b| b.byte).collect(),
        checksum: checksum_type,
        raw: raw.iter().map(|b| b.byte).collect(),
    }, ret))
}

fn calc_checksum(
    id: u8,
    length: u8,
    instruction: u8,
    parameters: &[TimestampedByte],
) -> u8 {
    let mut val: u16 = id as u16 + length as u16 + instruction as u16;
    for param in parameters {
        val += param.byte as u16;
    }
    !(val as u8)
}














fn parse_one_packet(byte_stream: &[TimestampedByte]) -> Result<InstructionPacket, InstructionError> {
    parse_one_packet_val(byte_stream, true)
}



fn try_correct_length(byte_stream: &[TimestampedByte], length: u8) -> Result<u8, InstructionError> {
    // try all possible lengths by bit flipping all 8 bits one by one
    for i in 0..8 {
        let mut new_length = length;
        new_length ^= 1 << i;

        println!("Trying new length: {}", new_length);
        // check if the new length is valid
        if byte_stream.len() >= (2 + 1 + 1 + new_length as usize) && parse_one_packet_val(&byte_stream[4 + new_length as usize..], false).is_ok() {
            // we found a corrected length, use this length instead
            return Ok(new_length);
        }
    }
    Err(InstructionError::InvalidLength(length))
}

fn parse_one_packet_val(byte_stream: &[TimestampedByte], validate_length: bool) -> Result<InstructionPacket, InstructionError> {

    // check if bytestream has at least one packet
    if byte_stream.len() < 6 {
        return Err(InstructionError::NotEnoughData);
    }

    if byte_stream[0].byte != 0xFF || byte_stream[1].byte != 0xFF {
        return Err(InstructionError::InvalidHeader);
    }

    let id = byte_stream[2].byte;

    // check if id is valid
    if id > 0x50 && id != 0xFE {
        return Err(InstructionError::InvalidId(id));
    }

    println!("ID: {:#X}", id);

    let mut length = byte_stream[3].byte;




    // Header (2) + ID (1) + Length (1) + Length bytes = total expected length
    if byte_stream.len() < (2 + 1 + 1 + length as usize) {
        return Err(InstructionError::InvalidLength(length));
    }
    // verify length if valid by checking if the next packet is valid
    // if validate_length {
    //     println!("Validating length... {}", length);
    //     if parse_one_packet_val(&byte_stream[4 + length as usize..], false).is_err() {
    //         println!("Attempting to correct length...");
    //         match try_correct_length(byte_stream, length) {
    //             Ok(new_length) => {
    //                 println!("Corrected length: {}", new_length);
    //                 length = new_length;
    //             }
    //             Err(e) => {
    //                 return Err(e);
    //             }
    //         }
    //     }
    //     println!("Validated length: {}", length);
    // }
    println!("Length: {}", length);


    let instruction = byte_stream[4].byte;
    let instruction_type = InstructionType::from_byte(instruction);
    println!("Instruction: {:#X} ({:?})", instruction, instruction_type);

    let param_len = length as usize - 2; // instruction (1) + checksum (1)
    let parameters = byte_stream[5..5 + param_len].to_vec();
    println!("Parameters: {:?}", parameters.iter().map(|b| format!("{:02X}", b.byte)).collect::<Vec<_>>());

    let checksum = byte_stream[4 + length as usize - 1].byte;

    let mut val: u16 = id as u16 + length as u16 + instruction as u16;
    for param in &parameters {
        val += param.byte as u16;
    }

    let calculated_checksum = !(val as u8);

    let checksum_type = if calculated_checksum == checksum {
        ChecksumType::Correct(checksum)
    } else {
        ChecksumType::Incorrect {
            expected: calculated_checksum,
            received: checksum,
        }
    };

    if calculated_checksum != checksum {
        println!(
            "Checksum mismatch calc({:#X}) != recv'd ({:#X})",
            calculated_checksum, checksum
        );

        // // most dangerous case is if length of this packet is bad.
        // // check by trying to parse next packet
        // if parse_one_packet(&byte_stream[4 + length as usize..]).is_err() {
        //     // if next packet is also an error, we will attempt length correction to fix this
        //     // packet, we will xor each bit in the length and check if it is valid

        //     println!("Attempting to correct length...");
        //     // try all possible lengths by bit flipping all 8 bits one by one
        //     for i in 0..8 {
        //         let mut new_length = length;
        //         new_length ^= 1 << i;

        //         println!("Trying new length: {}", new_length);
        //         // check if the new length is valid
        //         if byte_stream.len() >= (2 + 1 + 1 + new_length as usize) && parse_one_packet(&byte_stream[4 + new_length as usize..]).is_ok() {
        //             // we found a corrected length, use this length instead
        //             length = new_length;
        //             println!("Corrected length: {}", length);
        //         }
        //     }
        // }
    }

    let raw = byte_stream[0..(2 + 1 + 1 + length as usize)].to_vec();

    let duration: f64 = raw.iter().map(|b| b.duration).sum();

    Ok(InstructionPacket {
        start_time: byte_stream[0].start_time,
        duration,
        id,
        length,
        instruction_type,
        data: parameters.iter().map(|b| b.byte).collect(),
        checksum: checksum_type,
        raw: raw.iter().map(|b| b.byte).collect(),
    })
}

// parse a bytestream by parsing one packet and then next packet. If next packet is an error, check
// if current packet is also an error.

fn parse_bytestream(bytestream: &[TimestampedByte]) -> Result<Vec<InstructionPacket>, InstructionError> {
    let mut packets = Vec::new();
    let mut offset = 0;

    while offset < bytestream.len() {
        // Check if we have enough bytes for a packet
        if bytestream.len() - offset < 6 {
            break;
        }

        println!();


        match valid_packet_greedy(&bytestream[offset..]) {

            Ok((packet, corrections)) => {
                // get the start time for this byte
                let packet_size = 2 + 1 + 1 + packet.length as usize;
                offset += packet_size;
                packets.push(packet);
            },
            Err(e) => {
                println!("Error parsing packet: {:?}", e);
                break;
            }
        }

        // // Try to parse a packet
        // match parse_one_packet(&bytestream[offset..]) {

        //     Ok(packet) => {
        //         // get the start time for this byte
        //         let packet_size = 2 + 1 + 1 + packet.length as usize;
        //         offset += packet_size;
        //         packets.push(packet);
        //     }
        //     Err(e) => {
        //         println!("Error parsing packet: {:?}", e);
        //         match e {
        //             InstructionError::ChecksumMismatch => {
        //                 println!("Checksum mismatch, skipping this packet.");
        //                 // print last packet raw bytes, and then this packet raw bytes
        //                 if let Some(last_packet) = packets.last() {
        //                     println!("Last packet raw: {:?}", 
        //                         last_packet.raw.iter().map(|b| format!("{:02X}", b)).collect::<Vec<_>>());
        //                 }
        //                 // print 50 bytes of the bytestream
        //                 let end = std::cmp::min(offset + 50, bytestream.len());
        //                 println!("Bytestream: {:?}", 
        //                     &bytestream[offset..end].iter().map(|b| format!("{:02X}", b.byte)).collect::<Vec<_>>());
        //             },
        //             _ => {
        //                 // For other errors, we can just break
        //                 println!("Error: {:?}", e);
        //                 break;
        //             }
        //         }
        //         break;
        //     }
        // }
    }

    Ok(packets)
}


#[derive(Debug, Clone)]
struct TimestampedByte {
    start_time: f64,
    duration: f64,
    byte: u8,
}


fn main() -> Result<(), Box<dyn Error>> {
    // Open the CSV file
    let file = File::open("../snap1.csv")?;
    let mut rdr = ReaderBuilder::new()
        .has_headers(true) // No headers in your snippet
        .from_reader(BufReader::new(file));

    // Byte buffer to collect the data
    let mut bytestream: Vec<TimestampedByte> = Vec::new();

    for result in rdr.records() {
        let record = result?;
        // The "data" column is index 4 (0-based)
        let mut bd: u8 = 0;
        let mut start_time: f64 = 0.0;
        let mut duration: f64 = 0.0;

        if let Some(hex_str) = record.get(4) {
            // Trim and remove the "0x" prefix
            let trimmed = hex_str.trim().trim_start_matches("0x");
            // Parse the hex into a u8
            if let Ok(byte) = u8::from_str_radix(trimmed, 16) {
                bd = byte;
            }
        }

        // The "start_time" column is index 2 (0-based)
        if let Some(start_time_str) = record.get(2) {
            // Parse the start time
            if let Ok(st) = start_time_str.parse::<f64>() {
                start_time = st; 
            }
        }

        // The "duration" column is index 3 (0-based)
        if let Some(duration_str) = record.get(3) {
            // Parse the duration
            if let Ok(dur) = duration_str.parse::<f64>() {
                duration = dur;
            }
        }
        // Add the byte to the bytestream
        bytestream.push(TimestampedByte {
            start_time,
            duration,
            byte: bd,
        });
    }

    let parsed_packets = parse_bytestream(&bytestream).unwrap();
    // println!("Parsed packets: {:?}", parsed_packets);
    // Write packets to CSV
    write_packets_to_csv(parsed_packets, "output.csv")?;

    // Print result as hex
    // println!("Bytestream (hex): {:02X?}", bytestream);
    Ok(())
}

#[derive(Debug, Serialize)]
struct CsvPacket {
    start_time: f64,
    duration: f64,
    id: String,
    length: u8,
    instruction: String,
    instruction_name: String,
    parameters: String,
    checksum: String,
    raw: String,
}

fn to_csv_record(pkt: InstructionPacket) -> CsvPacket {
    CsvPacket {
        start_time: pkt.start_time,
        duration: pkt.duration,
        // id: format!("{:#02X}", pkt.id),
        id: pkt.id.to_string(),
        length: pkt.length,
        instruction: format!("{:#02X}", pkt.instruction_type.to_byte()),
        instruction_name: pkt.instruction_type.as_str(),
        parameters: pkt.data.iter().map(|b| format!("{:02X}", b)).collect::<Vec<_>>().join(","),
        checksum: format!("{:}", pkt.checksum),
        raw: pkt.raw.iter().map(|b| format!("{:02X}", b)).collect::<Vec<_>>().join(","),
    }
}

fn write_packets_to_csv(packets: Vec<InstructionPacket>, path: &str) -> Result<(), Box<dyn Error>> {
    let mut writer = Writer::from_path(path)?;

    for pkt in packets.into_iter().map(to_csv_record) {
        writer.serialize(pkt)?;
    }

    writer.flush()?;
    Ok(())
}
