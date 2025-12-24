from dotenv import load_dotenv
import os
import requests
import textwrap

# API setup
weather_url = "http://api.weatherapi.com/v1/forecast.json?"
news_url = "https://gnews.io/api/v4/search?"
pop_url = "http://api.geonames.org/searchJSON?"
funfact_url = "https://uselessfacts.jsph.pl/api/v2/facts/random"

load_dotenv('API_Keys.env')
weather_api: str = os.getenv('weather')
news_api: str = os.getenv('news')
pop_api: str = os.getenv('pop')

#Loop for re-using the input:
while True:
    city = input("Please enter the city's name (or 'quit' to exit): ")

    if city.lower() == 'quit':
        print("Thanks for using our services, good bye!")
        break

    # Handling the possibility of incorrect city spelling/non existent city:
    try:
        # Weather parameters
        weather_response = requests.get(
        weather_url + "key=" + weather_api + "&q=" + city + "&days=1&aqi=no&alerts=no").json()
        current_temp = weather_response['current']['temp_c']
        feels_like_temp = weather_response['current']['feelslike_c']
        humidity = weather_response['current']['humidity']
        weather_description = weather_response['current']['condition']['text']
        min_temp = weather_response['forecast']['forecastday'][0]['day']['mintemp_c']
        max_temp = weather_response['forecast']['forecastday'][0]['day']['maxtemp_c']
        wind_state = weather_response['current']['wind_kph']
        current_time = weather_response['location']['localtime']

        # News parameters
        news_response = requests.get(news_url + "q=" + city + "&token=" + news_api + "&lang=en&max=1").json()
        news_title = news_response['articles'][0]['title']
        news_desc = news_response['articles'][0]['description']
        news_source = news_response['articles'][0]['url']

        # Population parameters
        pop_response = requests.get(pop_url + "q=" + city + "&maxRows=1&username=" + pop_api).json()
        population = pop_response['geonames'][0]['population']
        country = pop_response['geonames'][0]['countryName']

         # Historical facts parameters
        historical_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{city.replace(' ', '_')}"
        historical_headers = {'User-Agent': 'Daily city insights',
                              'Accept': 'application/json'}
        historical_response = requests.get(historical_url, headers=historical_headers)
        historical_data = historical_response.json()
        historical_info = historical_data.get('extract')

        # Fun Fact parameters
        funfact_response = requests.get(funfact_url).json()
        fun_fact = funfact_response['text']

         # Wrapping the news, fun fact and historical info
        def format_text_content(fun_fact, news_title, news_desc, historical_info, content_width=60, max_sentences=2):
            sentences = historical_info.split('. ')
            valid_sentences = [s.strip() for s in sentences if s.strip()]
            if len(valid_sentences) > max_sentences:
                summary = '. '.join(valid_sentences[:max_sentences]) + "."
            else:
                summary = historical_info
            wrapped_funfact = textwrap.fill(fun_fact, width=content_width, initial_indent=' ' * 18,
                                            subsequent_indent=' ' * 18)
            wrapped_news_title = textwrap.fill(news_title, width=content_width, initial_indent=' ' * 18,
                                               subsequent_indent=' ' * 18)
            wrapped_news_desc = textwrap.fill(news_desc, width=content_width, initial_indent=' ' * 18,
                                              subsequent_indent=' ' * 18)
            wrapped_historical_summary = textwrap.fill(summary, width=content_width, initial_indent=' ' * 18,
                                                       subsequent_indent=' ' * 18)
            return wrapped_funfact, wrapped_news_title, wrapped_news_desc, wrapped_historical_summary

        formatted_funfact, formatted_news_title, formatted_news_desc, formatted_historical = format_text_content(
            fun_fact, news_title, news_desc, historical_info)

        # printing all of the info
        print(' ' * 11 + f"TODAY'S INSIGHT IN {city.upper()}, {country.upper()}\n"
                         f"{'=' * 60}\n"
                         f"Current temperature: {current_temp}°C\n"
                         f"Feels like: {feels_like_temp}°C\n"
                         f"Today's temperature range: {max_temp} - {min_temp}°C\n"
                         f"Humidity: {humidity}%\n"
                         f"Wind speed: {wind_state}km/h\n"
                         f"Condition: {weather_description.lower()}\n"
                         f"{'=' * 60}\n"
                         f"Current population in {city.capitalize()} is {format(population, ',')}\n"
                         f"{'=' * 60}\n"
                         f"{city.capitalize()}'s info: \n"
                         f"{formatted_historical}\n"
                         f"{'=' * 60}\n"
                         f"Today's fun fact: \n"
                         f"{formatted_funfact}\n"
                         f"{'=' * 60}\n"
                         f"Latest news title: \n"
                         f"{formatted_news_title}.\n"
                         f"{'=' * 60}\n"
                         f"News description: \n"
                         f"{formatted_news_desc}\n"
                         f"For more info: {news_source}\n"
                         f"{'=' * 60}\n")

    except Exception as e:
        print(f"Unfortunately we could not provide info for a city with the name {city}. \n"
              "This could be due to a spelling error, or that it does not exist in the databases, please try again.")
