import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
APP_VERSION = os.getenv("APP_VERSION", "v1")


@app.route("/")
def index():
    return jsonify({
        "message": "Weather API is running",
        "example": "/weather?city=Moscow",
        "version": APP_VERSION
    })


@app.route("/weather")
def get_weather():
    city = request.args.get("city", "Moscow")
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        return jsonify({
            "error": "OPENWEATHER_API_KEY is not set"
        }), 500

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return jsonify({
                "error": "OpenWeather request failed",
                "details": data
            }), response.status_code

        return jsonify({
            "version": APP_VERSION,
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature_c": data.get("main", {}).get("temp"),
            "feels_like_c": data.get("main", {}).get("feels_like"),
            "description": data.get("weather", [{}])[0].get("description"),
            "wind_m_s": data.get("wind", {}).get("speed")
        })

    except requests.RequestException as error:
        return jsonify({
            "error": "Request error",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
