from django.shortcuts import render
from django.contrib import messages
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Indore'  # Default city if not provided

    weather_api_key = 'c6786e23ccbafe185bc781b223c40daf'
    custom_search_api_key = 'AIzaSyDj68i2H6HIqqZ_bIw5-wGPFbKBk79GA-c'
    search_engine_id = '91252bf21f1f9442c'

    # Fetch weather information
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=c6786e23ccbafe185bc781b223c40daf'
    weather_params = {'units': 'metric'}

    try:
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()  # Raise an exception for HTTP errors
        weather_data = weather_response.json()

        # Extract weather details
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()
    except requests.exceptions.RequestException as e:
        # Handle weather API errors
        messages.error(request, f'Failed to fetch weather information: {e}')
        description = 'Unknown'
        icon = '01d'  # Default icon
        temp = '--'  # Default temperature
        day = datetime.date.today()

    # Fetch image URL using Google Custom Search API
    query = f'{city} 1920x1080'
    search_url = f"https://www.googleapis.com/customsearch/v1?key={custom_search_api_key}&cx={search_engine_id}&q={query}&searchType=image&imgSize=xlarge"

    try:
        search_response = requests.get(search_url)
        search_response.raise_for_status()  # Raise an exception for HTTP errors
        search_data = search_response.json()
        search_items = search_data.get("items")

        if search_items:
            image_url = search_items[0]['link']  # Use the first image URL
        else:
            image_url = None
    except requests.exceptions.RequestException as e:
        # Handle Google Custom Search API errors
        messages.error(request, f'Failed to fetch image URL: {e}')
        image_url = None

    return render(request, 'index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'exception_occurred': False if description != 'Unknown' else True,
        'image_url': image_url
    })
