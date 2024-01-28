from fastapi.security import APIKeyHeader
from llama_hub.tools.weather import OpenWeatherMapToolSpec
from fastapi import FastAPI, Query, Security, HTTPException

app = FastAPI()

api_key_header = APIKeyHeader(name='Api-key', auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail='Could not validate credentials')
    return api_key


@app.get('/weather/today', summary="Get Current Weather At Location", tags=["Weather"])
async def get_weather_at_location(
        location: str = Query(..., description="The name of the location to get the weather for."),
        api_key: str = Security(get_api_key)
):
    """
    Fetches the current weather at the specified location using OpenWeatherMap API.

    Parameters:
    - location: Name of the location (city, region)

    Returns:
    - WeatherReport: The current weather conditions at the specified location.
    """
    tool_spec = OpenWeatherMapToolSpec(key=api_key)

    weather_document = tool_spec.weather_at_location(location)

    weather_content = weather_document[0].get_content()

    return weather_content


@app.get('/weather/tomorrow', summary="Get Weather Forecast for Tomorrow at Location", tags=["Forecast"])
async def get_forecast_tomorrow_at_location(
        location: str = Query(..., description="The name of the location to get the forecast for."),
        api_key: str = Security(get_api_key)
):
    """
    Fetches the weather forecast for tomorrow at the specified location using OpenWeatherMap API.

    Parameters:
    - location: Name of the location (city, region)s

    Returns:
    - ForecastReport: The weather forecast for tomorrow at the specified location.
    """
    tool_spec = OpenWeatherMapToolSpec(key=api_key)

    forecast_document = tool_spec.forecast_tommorrow_at_location(location)

    forecast_content = forecast_document[0].get_content()

    return forecast_content
