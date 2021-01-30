from bs4 import BeautifulSoup
import requests

surf_url = 'https://www.surfline.com/surf-report/la-jolla-shores/5842041f4e65fad6a77088cc'
html_text = requests.get(surf_url).text
soup = BeautifulSoup(html_text, 'html.parser')

surf_height_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--surf-height' })
height_container = surf_height_container.findChildren('span', { 'class' : 'quiver-surf-height'})[0]
height_description = surf_height_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]

tide_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--tide'})
tide_height_container = tide_container.findChildren('span', { 'class' : 'quiver-reading'})[0]
tide_description_container = tide_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]

water_temp_container = soup.find('div', { 'class' : 'quiver-water-temp'}).findChildren('div')[0]
air_temp_container = soup.find('div', { 'class' : 'quiver-weather-stats'}).findChildren('div')[0]

print('Surf height: ' + height_container.getText().strip())
print(height_description.getText(separator=" ").strip())
print('Tide: ' + tide_height_container.getText().strip())
print(tide_description_container.getText(separator=" ").strip())
print("Water Temp: " + water_temp_container.getText().strip())
print("Air Temp: " + air_temp_container.getText().strip())
