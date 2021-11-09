from aiohttp import web
from dask.distributed import Client
import time
import random


client = None

async def hello(request):

    global client


    a  = random.randint(1, 10)

    def func(x):

        time.sleep(5)

        return x + 1

    # future = client.submit(func, a)

    future = client.submit(func, a)
    result = await future

    return web.Response(text="Hello, world")


async def hello2(request):

    return web.Response(text="Hello, world2")


async def app_init():

    global client

    client = await Client(processes= True, n_workers=10, scheduler_port=8786, asynchronous=True, host="0.0.0.0")

    app = web.Application()
    app.add_routes([web.get('/', hello)])
    app.add_routes([web.get('/h', hello2)])

    return app


if __name__ == "__main__":    

    web.run_app(app_init())