import sys
from datetime import datetime, timedelta
import aiohttp
import asyncio
import platform


class HttpError(Exception):
    pass


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    res = await resp.json()
                    return res
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            raise HttpError(f'Connection error: {url}', str(err))


async def main(count: int):
    response = []
    for d in [datetime.now() - timedelta(days=d) for d in range(count)]:
        try:
            response.append({d.strftime('%d.%m.%Y'): await request(
                f'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5&date={d.strftime('%d.%m.%Y')}')})
        except HttpError as err:
            return None

    return response


if __name__ == '__main__':
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    count = int(sys.argv[1])

    if count < 1 or count > 10:
        print('Max number of days must be between 1 and 10')
    else:
        print(asyncio.run(main(count)))
