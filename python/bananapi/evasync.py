import asyncio, evdev
from evdev import ecodes
#ir = evdev.InputDevice('/dev/input/event1')
#keybd = evdev.InputDevice('/dev/input/event2')

async def print_events(device):
    async for event in device.async_read_loop():
        #print(device.path, evdev.categorize(event), sep=': ')
        #print(device.path, event.value, sep=': ')
        print(event.code)
        
#for device in ir, keybd:
    #asyncio.ensure_future(print_events(device))

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print(device.name)
    if device.name == "sunxi-ir":
        print("Using device", device.path, "\n")
        #return device
    # print("No device found!")
    asyncio.ensure_future(print_events(device))


loop = asyncio.get_event_loop()
loop.run_forever()