from wanderwise_app import app
from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# i made sure to use well descriptive function and variable names to ensure readability
# Caching climate data to reduce API calls
climate_cache = {}

# Access the API keys
api_key_openweather = os.getenv('API_KEY_OPENWEATHER')
api_key_opentripmap = os.getenv('API_KEY_OPENTRIPMAP')
api_key_spoonacular = os.getenv('API_KEY_SPOONACULAR')
 
# Main function or helper function
def get_climate_data(country_name):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={country_name}&appid={api_key_openweather}&units=metric"
    if country_name in climate_cache:
        return climate_cache[country_name]
    try:
        response = requests.get(api_url)
        data = response.json()
        if response.status_code == 200:
            temperature = data['main']['temp']
            weather_description = data['weather'][0]['description'].lower()
            climate = None
            if temperature >= 30:
                climate = "Tropical"
            elif "desert" in weather_description or (temperature >= 25 and temperature < 30):
                climate = "Dry"
            elif (temperature >= 15 and temperature < 25):
                climate = "Temperate"
            elif temperature < 15:
                climate = "Cold"
            climate_cache[country_name] = climate
            return climate
    except Exception as e:
        print(f"Error fetching climate data: {e}")
        return None  

# function to get the countries latitude and longitude to enable get notable places in the country
def get_country_lat_lon(country_name):
    api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(api_url)
        data = response.json()
        country_data = data[0]
        latlng = country_data.get('latlng', [None, None])
        return latlng
    except Exception as e:
        print(f"Error fetching latitude and longitude from RestCountries: {e}")
        return [None, None] 

# function to get notable places in a country
def get_notable_places_opentripmap(country_name, lat, lon):
    api_url = f"https://api.opentripmap.com/0.1/en/places/radius"
    params = {
        'radius': 50000,  # 50 km radius
        'lon': lon,
        'lat': lat,
        'kinds': 'interesting_places',
        'format': 'json',
        'apikey': api_key_opentripmap
        
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        notable_places = [item['name'] for item in data[:12]]
        return notable_places if notable_places else ["No notable places found. Please check with a local"]
    except Exception as e:
        print(f"Error fetching notable places from OpenTripMap: {e}")
        return ["Information currently unavailable."]
 
# this is to help me clean up the code returned by wikivoyageapi
def clean_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup.get_text() 

# function to get country description using wikivoyageapi
def get_country_description_wikivoyage(country_name):
    api_url = f"https://en.wikivoyage.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'extracts',
        'format': 'json',
        'titles': country_name,
        'explaintext': True
        
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        extract = page.get('extract', '')
        paragraphs = extract.split('\n')
        # limit to seven paragraphs.
        limited_paragraphs = paragraphs[:5]
        cleaned_extract = '\n'.join(limited_paragraphs)
        
        return cleaned_extract if cleaned_extract else "Check the official website for more information."
    except Exception as e:
        print(f"Error fetching description from WikiVoyage: {e}")
        return "Information currently unavailable."
 
# function to get local food recommendations using spoonocularapi
def get_food_recommendations(country_name):
    country_to_cuisine = {
        # this is to ensure i get the right cuisine based on the country_name
        # ... your country-to-cuisine mapping ...
        'Sierra Leone': 'African',
        'United States': 'American',
        'Italy': 'Italian',
        'Mexico': 'Mexican',
        'India': 'Indian',
        'China': 'Chinese',
        'France': 'French',
        'Japan': 'Japanese',
        'Thailand': 'Thai',
        'Vietnam': 'Vietnamese',
        'Russia': 'Eastern European',
        'Brazil': 'Latin American',
        'Germany': 'German',
        'Greece': 'Greek',
        'Spain': 'Spanish',
        'Ireland': 'Irish',
        'South Korea': 'Korean',
        'United Kingdom': 'British',
        'Morocco': 'Middle Eastern',
        'Turkey': 'Middle Eastern',
        'Israel': 'Middle Eastern',
        'Sweden': 'Nordic',
        'Norway': 'Nordic',
        'Denmark': 'Nordic',
        'Cajun/Creole': 'Cajun',
        'Jamaica': 'Caribbean',
        'Cuba': 'Caribbean',
        'Argentina': 'Latin American',
        'Chile': 'Latin American',
        'Peru': 'Latin American',
        'Australia': 'Australian',
        'South Africa': 'South African',
        'New Zealand': 'New Zealand',
        'Belgium': 'Belgian',
        'Netherlands': 'Dutch',
        'Switzerland': 'Swiss',
        'Poland': 'Polish',
        'Portugal': 'Portuguese',
        'Hungary': 'Hungarian',
        'Ukraine': 'Ukrainian',
        'Egypt': 'Egyptian',
        'Lebanon': 'Lebanese',
        'Jordan': 'Middle Eastern',
        'Saudi Arabia': 'Middle Eastern',
        'Iran': 'Persian',
        'Pakistan': 'Pakistani',
        'Bangladesh': 'Bangladeshi',
        'Sri Lanka': 'Sri Lankan',
        'Nepal': 'Nepalese',
        'Mongolia': 'Mongolian',
        'Kazakhstan': 'Kazakh',
        'Uzbekistan': 'Uzbek',
        'Azerbaijan': 'Azerbaijani',
        'Armenia': 'Armenian',
        'Georgia': 'Georgian',
        'Myanmar': 'Burmese',
        'Malaysia': 'Malaysian',
        'Singapore': 'Singaporean',
        'Philippines': 'Filipino',
        'Brunei': 'Bruneian',
        'Laos': 'Laotian',
        'Cambodia': 'Cambodian',
        'Timor-Leste': 'Timorese',
        'Papua New Guinea': 'Papuan',
        'Fiji': 'Fijian',
        'Solomon Islands': 'Solomon Islands',
        'Vanuatu': 'Vanuatuan',
        'Tuvalu': 'Tuvaluan',
        'Samoa': 'Samoan',
        'Tonga': 'Tongan',
        'Kiribati': 'Kiribati',
        'Marshall Islands': 'Marshallese',
        # Additional European countries and their cuisines
        'France': 'French',
        'Germany': 'German',
        'Italy': 'Italian',
        'Spain': 'Spanish',
        'Portugal': 'Portuguese',
        'Greece': 'Greek',
        'Belgium': 'Belgian',
        'Netherlands': 'Dutch',
        'Switzerland': 'Swiss',
        'Poland': 'Polish',
        'Hungary': 'Hungarian',
        'Austria': 'Austrian',
        'Czech Republic': 'Czech',
        'Slovakia': 'Slovak',
        'Croatia': 'Croatian',
        'Serbia': 'Serbian',
        'Bulgaria': 'Bulgarian',
        'Romania': 'Romanian',
        'Turkey': 'Turkish',
        'Cyprus': 'Cypriot',
        'Ireland': 'Irish',
        'Norway': 'Norwegian',
        'Sweden': 'Swedish',
        'Denmark': 'Danish',
        'Finland': 'Finnish',
        'Estonia': 'Estonian',
        'Latvia': 'Latvian',
        'Lithuania': 'Lithuanian',
        'Malta': 'Maltese',
        'Andorra': 'Andorran',
        'Liechtenstein': 'Liechtensteiner',
        'Monaco': 'Monacan',
        # Additional North American countries and their cuisines
        'Canada': 'Canadian',
        'Mexico': 'Mexican',
        'United States': 'American',
        'Guatemala': 'Guatemalan',
        'Honduras': 'Honduran',
        'El Salvador': 'Salvadoran',
        'Nicaragua': 'Nicaraguan',
        'Costa Rica': 'Costa Rican',
        'Panama': 'Panamanian',
        'Cuba': 'Cuban',
        'Dominican Republic': 'Dominican',
        'Haiti': 'Haitian',
        'Jamaica': 'Jamaican',
        'Bahamas': 'Bahamian',
        'Barbados': 'Barbadian',
        'Trinidad and Tobago': 'Trinidadian',
        'Saint Lucia': 'Saint Lucian',
        'Grenada': 'Grenadian',
        'Saint Vincent and the Grenadines': 'Vincentian',
        'Antigua and Barbuda': 'Antiguan',
        'Saint Kitts and Nevis': 'Kittitian',
        # Additional South American countries and their cuisines
        'Argentina': 'Argentinian',
        'Bolivia': 'Bolivian',
        'Brazil': 'Brazilian',
        'Chile': 'Chilean',
        'Colombia': 'Colombian',
        'Ecuador': 'Ecuadorian',
        'Guyana': 'Guyanese',
        'Paraguay': 'Paraguayan',
        'Peru': 'Peruvian',
        'Suriname': 'Surinamese',
        'Uruguay': 'Uruguayan',
        'Venezuela': 'Venezuelan',
        # Additional Australian countries and their cuisines
        'Australia': 'Australian',
        'New Zealand': 'New Zealand',
        'Papua New Guinea': 'Papuan',
        'Fiji': 'Fijian',
        'Solomon Islands': 'Solomon Islands',
        'Vanuatu': 'Vanuatuan',
        'Samoa': 'Samoan',
        'Tonga': 'Tongan',
        'Kiribati': 'Kiribati',
    }

    cuisine = country_to_cuisine.get(country_name)
    if cuisine is None:
        return [f"No cuisine available for {country_name}."]

    api_url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'apiKey': api_key_spoonacular,
        'cuisine': cuisine,
        'number': 5,
        'addRecipeInformation': True
    }
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        recipes = [recipe['title'] for recipe in data.get('results', [])]
        return recipes if recipes else [f"No food recommendations found for {cuisine} cuisine. Please check with a local."]
    except Exception as e:
        print(f"Error fetching food recommendations from Spoonacular: {e}")
        return ["Information currently unavailable."] 

# function to help me get the country name and details using restcountriesapi
def get_country_details(country_name):
    api_url = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response = requests.get(api_url)
        data = response.json()
        country_data = data[0]
        flag = country_data.get('flags', {}).get('png', 'No flag available')
        capital = country_data.get('capital', ['No capital available'])[0]
        currency = ', '.join(country_data.get('currencies', {}).keys()) or 'No currency available'
        calling_code = country_data.get('idd', {}).get('root', '') + ''.join(country_data.get('idd', {}).get('suffixes', []))
        return flag, capital, currency, calling_code
    except Exception as e:
        print(f"Error fetching country details from RestCountries: {e}")
        return 'No flag available', 'No capital available', 'No currency available', 'No calling code available' 


# flask template rendering

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    preferences = { 
        "continent": request.form.get('continent'),
        "climate": request.form.get('climate')
    }
    return redirect(url_for('recommendations', continent=preferences['continent'], climate=preferences['climate']))

@app.route('/recommendations')
def recommendations():
    continent = request.args.get('continent')
    selected_climate = request.args.get('climate')
    
    region_mapping = {
        "Africa": "Africa",
        "Asia": "Asia",
        "Europe": "Europe",
        "North America": "Americas",
        "South America": "Americas",
        "Australia": "Oceania",
        "Antarctica": "Antarctic"
    }
    
    region = region_mapping.get(continent)
    if region:
        api_url = f"https://restcountries.com/v3.1/region/{region}"
        response = requests.get(api_url)
        countries = response.json()
    else:
        countries = []

    country_names = [country['name']['common'] for country in countries]
    
    filtered_countries = []
    suggestions_country = {}

    for country_name in country_names:
        latitude, longitude = get_country_lat_lon(country_name)
        climate = get_climate_data(country_name)
        
        if climate == selected_climate and latitude is not None and longitude is not None:
            filtered_countries.append(country_name)
            
            notable_place_opentripmap = get_notable_places_opentripmap(country_name, latitude, longitude)
            country_description_wikivoyage = get_country_description_wikivoyage(country_name)
            food_recommendations = get_food_recommendations(country_name)
            
            flag, capital, currency, calling_code = get_country_details(country_name)
            
            suggestions_country[country_name] = {
                'OpenTripMap': notable_place_opentripmap,
                'WikiVoyage': country_description_wikivoyage,
                'Food': food_recommendations,
                'Flag': flag,
                'Capital': capital,
                'Currency': currency,
                'Calling Code': calling_code
            }
    
    return render_template('recommendations.html', continent=continent,
                           filtered_countries=filtered_countries,
                           climate=selected_climate,
                           suggestions_country=suggestions_country)



