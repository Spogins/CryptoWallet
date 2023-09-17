import asyncio
import time
import httpx
from httpx import Limits, Response, ConnectTimeout

LIMITS = Limits(max_connections=10000, max_keepalive_connections=10000)


# async def fetch():
#     urls = ['https://www.google.com/search/about/'] * 10000
#
#     async with httpx.AsyncClient(limits=LIMITS) as client:
#         reqs = [client.get(url) for url in urls]
#         results = await asyncio.gather(*reqs)
#
#     for result in results:
#         if result.status_code != 302:
#             return False
#     return True


async def run_delivery():
    return await delivery(200, 'https://www.google.com/search/about/')

async def bound_fetch(semaphore, url, client):
    async with semaphore:
        return await fetch(url, client)


async def fetch(url, client):
    try:

        response: Response = await client.get(url, timeout=50)
        return True if response.status_code == 200 else False
    except:
        return False



async def delivery(ct, url):
    tasks = []
    semaphore = asyncio.Semaphore(1000)
    async with httpx.AsyncClient(limits=Limits(max_connections=10000, max_keepalive_connections=10000)) as client:
        for x in range(ct):
            task = asyncio.ensure_future(bound_fetch(semaphore, url.format(x), client))
            tasks.append(task)
        responses = asyncio.gather(*tasks)
        result = all(list(await responses))
        return result



if __name__ == '__main__':
    res = asyncio.run(run_delivery())
    print(res)


