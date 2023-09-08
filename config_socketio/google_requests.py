import asyncio
import time
import httpx
from httpx import Limits, Response

LIMITS = Limits(max_connections=10000, max_keepalive_connections=10000)


async def fetch():
    urls = ['https://www.google.com'] * 10000

    async with httpx.AsyncClient(limits=LIMITS) as client:
        reqs = [client.get(url) for url in urls]
        results = await asyncio.gather(*reqs)

    for result in results:
        if result.status_code != 302:
            return False
    return True

# if __name__ == '__main__':
#     start = time.perf_counter()
#     res = asyncio.run(fetch())
#     end = time.perf_counter()
#
#     print(res)
#     print(f"Time: {end-start:0.2f}")

