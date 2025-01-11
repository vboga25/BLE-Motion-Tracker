#scan for BLE devices and print addresses

import asyncio
from bleak import BleakScanner

async def scan_ble_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device: {device.name}, MAC Address: {device.address}")

if __name__ == "__main__":
    asyncio.run(scan_ble_devices())