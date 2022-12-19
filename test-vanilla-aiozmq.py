import asyncio
import zmq
import aiozmq
import time
import os

async def pushing():
    server = await aiozmq.create_zmq_stream(zmq.PUSH,
                                            bind='tcp://*:9000')
    for i in range(5000):
        server.write([b'Hello %d' % i])
    server.write([b'exit'])
    await server.drain()

async def pulling():
    client = await aiozmq.create_zmq_stream(zmq.PULL,
                                            connect='tcp://127.0.0.1:9000')
    with open(os.devnull, 'w') as null:
        while True:
            greeting = await client.read()
            if greeting[0] == b'exit': break
            print(str(greeting[0]), file=null)

async def main():
    loop = asyncio.get_running_loop()
    loop.create_task(pushing())
    try:
        begin = time.monotonic()
        await pulling()
        end = time.monotonic()
        print('asyncio + aiozmq: {:.6f} sec.'.format(end - begin))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    asyncio.run(main())

