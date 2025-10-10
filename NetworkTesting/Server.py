import socket
import bleak
import asyncio


'''s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 25313))
data, address = s.recvfrom(1024)
print(data)
print(data[0])'''
# broadcasting wasn't working

# from gemini

async def discover_bluetooth_devices():
    devices = await bleak.BleakScanner.discover()
    for device in devices:
        print(f"Device found!")
        print(device.name)
    if not devices:
        print("No devices found")

asyncio.run(discover_bluetooth_devices())

