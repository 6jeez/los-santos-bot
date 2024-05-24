import aiohttp


class WeatherService:
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key

    async def get_weather(self, city_name):
        async with aiohttp.ClientSession() as session:
            params = {"q": city_name, "appid": self.api_key, "units": "metric"}
            async with session.get(self.BASE_URL, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                    }
                else:
                    return None

    async def city_exists(self, city_name):
        async with aiohttp.ClientSession() as session:
            params = {"q": city_name, "appid": self.api_key}
            async with session.get(self.BASE_URL, params=params) as response:
                return response.status == 200
