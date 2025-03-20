import aiohttp

async def validate_url(url: str) -> bool:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False, timeout=5) as response:
                return True
        except:
            return False