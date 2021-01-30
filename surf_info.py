from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding
from rich.emoji import Emoji

import requests

console = Console()

# TODO take beach names as arguments and search surfline - get first link

with console.status("", spinner='shark') as status:
  surf_url = 'https://www.surfline.com/surf-report/la-jolla-shores/5842041f4e65fad6a77088cc'
  html_text = requests.get(surf_url).text
  soup = BeautifulSoup(html_text, 'html.parser')

  title_container = soup.find('h1', { 'class' : 'sl-forecast-header__main__title'})

  surf_height_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--surf-height' })
  height_container = surf_height_container.findChildren('span', { 'class' : 'quiver-surf-height'})[0]
  height_description = surf_height_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]

  tide_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--tide'})
  tide_height_container = tide_container.findChildren('span', { 'class' : 'quiver-reading'})[0]
  tide_description_container = tide_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]

  water_temp_container = soup.find('div', { 'class' : 'quiver-water-temp'}).findChildren('div')[0]
  air_temp_container = soup.find('div', { 'class' : 'quiver-weather-stats'}).findChildren('div')[0]

  title = Text(title_container.getText().strip())
  title.stylize("bold magenta")
  title_padding = Padding(title, (1, 0))

  table = Table.grid(expand=True)
  table.add_column(style='bold cyan', no_wrap=True)
  table.add_column(style='magenta')
  table.add_row('Surf Height', height_container.getText().strip())
  table.add_row('', height_description.getText(separator=' ').strip())
  table.add_row()
  table.add_row('Tide Height', tide_height_container.getText().strip())
  table.add_row('', tide_description_container.getText(separator=' ').strip())
  table.add_row()
  table.add_row('Water Temp', water_temp_container.getText().strip())
  table.add_row()
  table.add_row('Air Temp', air_temp_container.getText().strip())


console = Console()
console.print(title_padding)
console.print(table)
