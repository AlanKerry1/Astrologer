import os
import aiohttp
import asyncio
from dotenv import load_dotenv
import logging

load_dotenv()
os.environ['NO_PROXY'] = '127.0.0.1'

# Настройка логгирования
logging.basicConfig(level=logging.INFO)


async def make_async_request(url: str, data: dict):
    """Асинхронная функция для выполнения POST-запроса."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
                return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Error during HTTP request to {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error during HTTP request to {url}: {e}")
        return None


async def getTaro(name: str, question: str, cardsNumber: str):
    """Асинхронная функция для получения расклада Таро."""
    url = os.getenv("GADALKA_API_URL") + "/taro"
    data = {"name": name, "question": question, "cardsNumber": cardsNumber}
    return await make_async_request(url, data)


async def getHoroscope(zodiak: str):
    """Асинхронная функция для получения гороскопа."""
    url = os.getenv("GADALKA_API_URL") + "/horoscope"
    data = {"zodiak": zodiak}
    return await make_async_request(url, data)


async def getCompatibility(name1: str, name2: str, zodiak1: str, zodiak2: str):
    """Асинхронная функция для получения совместимости."""
    url = os.getenv("GADALKA_API_URL") + "/compatibility"
    data = {"name1": name1, "name2": name2, "zodiak1": zodiak1, "zodiak2": zodiak2}
    return await make_async_request(url, data)