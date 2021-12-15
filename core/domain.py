import datetime
import calendar
import pytz
import requests, json

class Utils():
    @staticmethod
    def teste():
        from django.contrib.auth.models import User
        user = User.objects.create_user(username='', password='', is_superuser=True, is_staff=True)

    @staticmethod
    def convert_to_local_datetime(date):
        date_local = datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S')
        local_tz = pytz.timezone('America/Sao_Paulo')
        local_dt = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_dt

    @staticmethod
    def convert_int_to_local_datetime(date_int):
        date = datetime.datetime.fromtimestamp(date_int).strftime('%Y-%m-%d %H:%M:%S')
        local_tz = pytz.timezone('America/Sao_Paulo')
        local_dt = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.utc).astimezone(local_tz)
        return local_dt

class CommunicationWithServerWeatherForecast():

    def convert_item_response_in_data_internal(self, item, city):

        date = str(Utils().convert_int_to_local_datetime(item['dt']))
        date_week = str(calendar.day_name[Utils().convert_int_to_local_datetime(item['dt']).weekday()])
        today = str(1 if Utils().convert_int_to_local_datetime(item['dt']).day == datetime.datetime.today().day else 0)
        tomorrow = str(1 if Utils().convert_int_to_local_datetime(item['dt']).day == (datetime.datetime.today().day + 1) else 0)
        temperature = str(item['main']['temp']) + ' Cº'
        wind = str(item['wind']['speed']) + ' m/s'
        cloudness = str(item['weather'][0]['description'])
        pressure = str(item['main']['pressure']) + ' hpa'
        humidity = str(item['main']['humidity']) +' %'
        sunrise = str(Utils().convert_int_to_local_datetime(city['sunrise']))
        sunset = str(Utils().convert_int_to_local_datetime(city['sunset']))
        geo_coords = '[' + str(city['coord']['lat']) + ',' + str(city['coord']['lat']) + ']'

        data = {
            'date': date,
            'date_week': date_week,
            'today': today,
            'tomorrow': tomorrow,
            'temperature': temperature,
            'wind': wind,
            'cloudness': cloudness,
            'pressure': pressure,
            'humidity': humidity,
            'sunrise': sunrise,
            'sunset': sunset,
            'geo_coords': geo_coords,
        }
        return data

    def month_url_forecast_for_city(self, city):
        url = 'https://api.openweathermap.org/data/2.5/forecast?q=%s&units=%s&mode=%s&appid=%s' % \
              (city, 'metric', 'json', '07e65dc66dc29a55e8fa6a3df62731dd')
        return url

    def verify_closer_hour(self):
        hours_request = [0, 3, 6, 9, 12, 15, 18, 21, 24]
        current_hour = datetime.datetime.today().hour

        for hour in hours_request:
            if (current_hour - hour) <= 0:
                return hour

    def get_forecast_for_city(self, city):
        url = self.month_url_forecast_for_city(city)
        response = json.loads(requests.get(url).text)

        info_city = response['city']
        closer_hour = self.verify_closer_hour()

        list_itens = []
        for item in response['list']:
            item_internal = {}
            date_item = Utils().convert_int_to_local_datetime(item['dt'])

            if (date_item.day != datetime.datetime.today().day):
                if date_item.hour == closer_hour:
                    item_internal = self.convert_item_response_in_data_internal(item, info_city)
            else:
                if len(list_itens) <= 0:
                    item_internal = self.convert_item_response_in_data_internal(item, info_city)

            if item_internal:
                list_itens.append(item_internal)

        return list_itens


