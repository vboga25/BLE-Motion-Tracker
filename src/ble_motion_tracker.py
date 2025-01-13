import asyncio
from bleak import BleakScanner

# Main BLE Scanner Logic
async def main(scan_duration):
    print("Scanning for BLE devices...")
    try:
        devices = await BleakScanner.discover()
        prev_accel = (0.0, 0.0, 0.0)  # Initialize previous accelerometer values

        for device in devices:
            print(f"Device: {device.address}, Name: {device.name}")
            # Example packet for demonstration
            packet = "0x0201060303E1FF1216E1FFA10364FFF4000FFF003772A33F23AC"
            if parse_ibeacon_data(packet):  # Check if it's an iBeacon packet
                curr_accel = parse_accelerometer_data(packet)  # Extract accelerometer data
                if curr_accel:
                    detect_motion(prev_accel, curr_accel)
                    prev_accel = curr_accel  # Update previous accelerometer values
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scan_duration = 5  # Example duration in seconds
    asyncio.run(main(scan_duration))


def fixed_point_to_decimal(hex_value):
    value = int(hex_value, 16)                  # Convert hex to 16-bit integer
    if value & 0x8000:                          # Check if number is negative (first bit is 1)
        value = value - 0x10000                 # Convert to negative value using two's complement
    return value / 256                          # Divide by 256 (2^8) to account for 8 fractional bits


# Parse Accelerometer Data
def parse_accelerometer_data(packet):
    try:
        if packet.startswith("0x0201060303E1FF1216E1FF"):  # Accelerometer frame prefix
            accel_data = packet[28:40]  # Extract accelerometer data from 28th to 39th half-byte

            # Extract x, y, z raw data
            x_raw = int(accel_data[0:3], 16)
            y_raw = int(accel_data[4:7], 16)
            z_raw = int(accel_data[8:11], 16)

            # Convert 8.8 fixed-point format to float
            x = fixed_point_to_decimal(x_raw)
            y = fixed_point_to_decimal(y_raw)
            z = fixed_point_to_decimal(z_raw)

            print(f"Parsed Accelerometer Data - X: {x}g, Y: {y}g, Z: {z}g")
            return x, y, z
    except Exception as e:
        print(f"Error parsing accelerometer data: {e}")
    return None

# Parse iBeacon Data
def parse_ibeacon_data(packet):
    try:
        if packet.startswith("0x0201061AFF4C000215"):  # iBeacon frame prefix
            uuid = packet[18:50]  # Extract UUID from 18th to 49th half-byte
            print(f"Parsed iBeacon UUID: {uuid}")
            return True
        return False
    except Exception as e:
        print(f"Error parsing iBeacon data: {e}")
        return False


# Detect Motion Based on Accelerometer Data
def detect_motion(prev_accel, curr_accel, threshold=0.5):
    try:
        # Calculate differences between successive accelerometer values
        diff_x = abs(curr_accel[0] - prev_accel[0])
        diff_y = abs(curr_accel[1] - prev_accel[1])
        diff_z = abs(curr_accel[2] - prev_accel[2])

        # Check if the difference exceeds the threshold on any axis
        if diff_x > threshold or diff_y > threshold or diff_z > threshold:
            print(f"Device is moving. Differences - X: {diff_x}, Y: {diff_y}, Z: {diff_z}")
            return True
        else:
            print(f"Device is stationary. Differences - X: {diff_x}, Y: {diff_y}, Z: {diff_z}")
            return False
    except Exception as e:
        print(f"Error detecting motion: {e}")
    return False