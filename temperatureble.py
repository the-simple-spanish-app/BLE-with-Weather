import math
from time import time, sleep
import requests
import sys
import platform
import asyncio
import logging

from bleak import BleakClient
characteristic_light = "characteristic"
ADDRESS = "(BLE ADRDESS)"

city_name = "City Name , Country name"
api_key= "your api key"

def get_weather(api_key, city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url).json()
    allinfo = response['main']
    temp = response['main']['temp']
    humidity = response['main']['humidity']
    feel = int(response['main']['feels_like'])
    print(float(temp))
    print(allinfo)


    print(feel)
    fahr = ((feel - 273.15) * 9/5 + 32)
    if(fahr >= 75):
        red = round(fahr*2)
        blue = round(fahr/2)
    else:
        red = round(fahr/2)
        blue = round(fahr*2)
    print(red, blue)
    print('feels like', fahr)
    get_weather.feelarray = bytearray([0x56, red, blue, 0, 0,0xf0, 0xaa ])


async def main(address):
    async with BleakClient(address) as client:
        weatherinf = get_weather(api_key, 'Kingston')
        print(str(get_weather.feelarray))
        print(f"Connected: {client.is_connected}")

        paired = await client.pair(protection_level=2)
        print(f"Paired: {paired}")

        print("Turning Light off...")
        await client.write_gatt_char(characteristic_light, get_weather.feelarray)
        await asyncio.sleep(1.0)
        print("Turning Light on...")

        await asyncio.sleep(1.0)

if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))
