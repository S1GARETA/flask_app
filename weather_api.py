import requests

def get_weather_data(city):
    api_key = '95d80fd73fbbe197f5d1b3a1df1222b5'
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}&lang=ru'
    # https://api.openweathermap.org/data/2.5/forecast?q=Moscow&units=metric&appid=95d80fd73fbbe197f5d1b3a1df1222b5&lang=ru

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            print("Ошибка при запросе данных о погоде:", data.get('message', 'Неизвестная ошибка'))
            return None

        weather_data = []
        for forecast in data['list']:
            if '12:00:00' in forecast['dt_txt']:
                weather_data.append({
                    'date': forecast['dt_txt'],
                    'temp_day': forecast['main']['temp'],
                    'temp_night': forecast['main']['temp_min'],
                    'description': forecast['weather'][0]['description']
                })

            if len(weather_data) == 3:
                break

        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None