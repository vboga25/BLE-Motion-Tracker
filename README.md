# BLE-Motion-Tracker
 This project reads accelerometer data from a real BLE Tag and detects whether the tag is moving or stationary

## Prerequisites

- Python 3.8 or higher
- Bluetooth adapter (compatible with both Linux and Mac)

## Installation

1. Clone the repository:
```bash
git clone <https://github.com/vboga25/BLE-Motion-Tracker.git>
cd BLE-Motion_Tracker
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:
```bash
python src/ble_motion_tracker.py
```

The program will:
1. Start scanning for BLE devices
2. Process accelerometer data from matching devices
3. Display movement status in real-time

## How It Works

### **1. BLE Scanning**
- The program uses the `Bleak` library to scan for nearby BLE devices.
- The program processes packet data for further analysis for each device detected.

### **2. iBeacon Detection**
- Identifies packets with the iBeacon prefix (`0x0201061AFF4C000215`).
- Extracts the UUID from valid iBeacon packets for validation and logging.

### **3. Accelerometer Data Parsing**
- Processes packets matching the accelerometer broadcast prefix (`0x0201060303E1FF1216E1FF`).
- Extracts appropriate data, representing the X, Y, and Z axes in 8.8 fixed-point format.
- Converts hex data into signed decimal format.

### **4. Motion Detection**
- Compares current accelerometer readings to the previous readings.
- Calculates differences for each axis (X, Y, Z).
- If the difference on any axis exceeds the defined threshold (default `0.5g`), the device seems to be moving.

### **5. Output**
- Prints device information (address and name).
- Logs parsed accelerometer data and the motion detection status.

## Error Handling

The program includes error handling for:
- Invalid packet formats
- Connection issues
- Data parsing errors

## Development

This project follows good git practices with regular commits at meaningful checkpoints.
