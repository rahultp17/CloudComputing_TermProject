from flask import Blueprint, request, jsonify, current_app
import requests

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return jsonify({'error': data.get('message', 'Failed to fetch weather data')}), response.status_code

        # Cleaned output
        result = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
