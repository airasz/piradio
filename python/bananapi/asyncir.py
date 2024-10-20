# import asyncio, evdev
#
# ir = evdev.InputDevice('/dev/input/event1')
# def get_ir_values():
#     devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
#     for device in devices:
#         print(device.name)
#         if device.name == "sunxi-ir":
#             print("Using device", device.path, "\n")
#             return device
#         # print("No device found!")
#
# dev = get_ir_values()
#
# async def print_events(dev):
#     async for event in dev.async_read_one():
#         if event:
#             print(event.value)
#         # print(device.path, evdev.categorize(event), sep=': ')
#
# # for device in ir:
# #     asyncio.ensure_future(print_events(device))
#
# loop = asyncio.get_event_loop()
# loop.run_forever()


import asyncio
from evdev import InputDevice

dev = InputDevice('/dev/input/event1')

async def main(dev):
        async for ev in dev.async_read_loop():
            print(repr(ev))
            print(ev.value)

asyncio.run(main(dev))
