import asyncio
import logging
import random

from nextion import Nextion, EventType

class App:
    def __init__(self):
        self.client = Nextion('/dev/ttyUSB0', 9600, self.event_handler)

    # Note: async event_handler can be used only in versions 1.8.0+ (versions 1.8.0+ supports both sync and async versions)
    async def event_handler(self, type_, data):
        if type_ == EventType.STARTUP:
            print('We have booted up!')
        elif type_ == EventType.TOUCH:
            print('A button (id: %d) was touched on page %d' % (data.component_id, data.page_id))

        logging.info('Event %s data: %s', type, str(data))

        print(await self.client.get('field1.txt'))

    async def run(self):
        await self.client.connect()

        # await client.sleep()
        # await client.wakeup()

        # await client.command('sendxy=0')

        print(await self.client.get('sleep'))
        print(await self.client.get('field1.txt'))

        await self.client.set('field1.txt', "%.1f" % (random.randint(0, 1000) / 10))
        await self.client.set('field2.txt', "%.1f" % (random.randint(0, 1000) / 10))

        await self.client.set('field3.txt', random.randint(0, 100))

        print('finished')

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.DEBUG,
        handlers=[
            logging.StreamHandler()
        ])
    loop = asyncio.get_event_loop()
    app = App()
    asyncio.ensure_future(app.run())
    loop.run_forever()
