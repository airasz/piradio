import asyncio
import tornado.ioloop
import tornado.web
import tornado.websocket
from evdev import InputDevice, categorize, ecodes

# WebSocket handler
class WSHandler(tornado.websocket.WebSocketHandler):
    clients = set()

    def open(self):
        print("WebSocket opened")
        self.clients.add(self)

    def on_close(self):
        print("WebSocket closed")
        self.clients.remove(self)

    @classmethod
    async def send_message(cls, message):
        for client in cls.clients:
            if client.ws_connection:  # Check if the client is still connected
                await client.write_message(message)

# Event reader
async def read_events(device):
    async for event in device.async_read_loop():
        if event.type == ecodes.EV_KEY:  # Check for key events
            message = categorize(event)
            print(f"Received event: {message}")
            await WSHandler.send_message(str(message))

# Tornado application setup
def make_app():
    return tornado.web.Application([
        (r"/websocket", WSHandler),
    ])

if __name__ == "__main__":
    device_path = '/dev/input/eventX'  # Change this to your evdev device path
    device = InputDevice(device_path)

    app = make_app()
    app.listen(8888)

    # Start reading events from the evdev device
    asyncio.ensure_future(read_events(device))

    # Start the Tornado I/O loop
    tornado.ioloop.IOLoop.current().start()
