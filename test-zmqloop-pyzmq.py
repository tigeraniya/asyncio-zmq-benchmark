import asyncio
import zmq.asyncio
import time
import os

ctx = zmq.asyncio.Context()

async def pushing():
    server = ctx.socket(zmq.PUSH)
    server.bind('tcp://*:9000')
    for i in range(5000):
        await server.send(b'Hello %d' % i)
    await server.send(b'exit')

async def pulling():
    client = ctx.socket(zmq.PULL)
    client.connect('tcp://127.0.0.1:9000')
    with open(os.devnull, 'w') as null:
        while True:
            greeting = await client.recv_multipart()
            if greeting[0] == b'exit': break
            print(greeting[0], file=null)

async def main():
    loop = asyncio.get_running_loop()
    loop.create_task(pushing())
    try:
        begin = time.monotonic()
        await pulling()
        end = time.monotonic()
        print('zmqloop + pyzmq: {:.6f} sec.'.format(end - begin))
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    asyncio.run(main())

