import os
import sys
import time
import requests
import concurrent.futures
import aiohttp
import asyncio


# Функция для скачивания изображения с использованием многопоточности
def download_image_thread(url, directory):
    filename = os.path.join(directory, url.split('/')[-1])
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename, time.time()


# Функция для скачивания изображения с использованием многопроцессорности
def download_image_process(url, directory):
    filename = os.path.join(directory, url.split('/')[-1])
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename, time.time()


# Функция для скачивания изображения с использованием асинхронности
async def download_image_async(url, session, directory):
    filename = os.path.join(directory, url.split('/')[-1])
    async with session.get(url) as response:
        with open(filename, 'wb') as f:
            f.write(await response.read())
    return filename, time.time()


async def main():
    urls = sys.argv[1:]
    directory = "images"  # Путь к директории, где будут сохраняться изображения
    os.makedirs(directory, exist_ok=True)  # Создаем директорию, если она не существует
    start_time = time.time()

    # Многопоточный подход
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = list(executor.map(download_image_thread, urls, [directory]*len(urls)))

    # Многопроцессорный подход
    with concurrent.futures.ProcessPoolExecutor() as executor:
        process_results = list(executor.map(download_image_process, urls, [directory]*len(urls)))

    # Асинхронный подход
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(url, session, directory) for url in urls]
        async_results = await asyncio.gather(*tasks)

    end_time = time.time()

    # Вывод информации о времени скачивания и общем времени выполнения программы
    print("Результат многопоточного подхода:")
    for result in thread_results:
        print(f"Изображение {result[0]} загружено за {result[1] - start_time} секунд")

    print("Результат мультипроцессорного подхода:")
    for result in process_results:
        print(f"Изображение {result[0]} загружено за {result[1] - start_time} секунд")

    print("Результат асинхронного подхода:")
    for result in async_results:
        print(f"Изображение {result[0]} загружено за {result[1] - start_time} секунд")

    print("Общее время выполнения:", end_time - start_time)

if __name__ == "__main__":
    asyncio.run(main())
