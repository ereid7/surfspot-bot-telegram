from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding
from rich.emoji import Emoji
import sys
import requests


if __name__ == "__main__":
  console = Console()

  if (len(sys.argv) < 2):
      console.print(f"Search argument required to find surf spot", style="cyan")
      sys.exit()
      
  with console.status("", spinner='shark') as status:

    search = sys.argv[1]

    # search for surf spot name
    search_url = f"https://www.surfline.com/search/{search}"
    search_page_html = requests.get(search_url).text
    search_soup = BeautifulSoup(search_page_html, 'html.parser')

    # retrieve first search result
    first_result_container = search_soup.find('div', { 'class' : 'result'})

    if (first_result_container is None):
      console.print(f"No surf spots found for: {search}", style="cyan")
      sys.exit()
  
    first_result_link = first_result_container.findChildren('a')[0]


    surf_url = first_result_link['href']
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

  console.print(title_padding)
  console.print(table)
