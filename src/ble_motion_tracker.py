import asyncio
from bleak import BleakScanner

async def scan_ble_devices():                   #scan for BLE devices and print addresses
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, MAC Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(scan_ble_devices())

def fixed_point_to_decimal(hex_value):
    value = int(hex_value, 16)                  # Convert hex to 16-bit integer
    if value & 0x8000:                          # Check if number is negative (first bit is 1)
        value = value - 0x10000                 # Convert to negative value using two's complement
    return value / 256                          # Divide by 256 (2^8) to account for 8 fractional bits


# Parse Accelerometer Data
def parse_accelerometer_data(packet):
    try:
        if packet.startswith("0x0201060303E1FF1216E1FF"):  # Accelerometer frame prefix
            accel_data = packet[28:39]  # Extract accelerometer data 

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
