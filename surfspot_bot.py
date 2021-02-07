from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from bs4 import BeautifulSoup
import requests
import re

def surf(update, context):
  search = ' '.join(context.args)
  # search for surf spot name
  search_url = f'https://www.surfline.com/search/{search}'
  search_page_html = requests.get(search_url).text
  search_soup = BeautifulSoup(search_page_html, 'html.parser')

  # retrieve first search result
  first_result_container = search_soup.find('div', { 'class' : 'result'})

  # return if no surf spots found
  if (first_result_container is None):
    update.message.reply_text(f'No surf spots found for: {search}')
    return

  # grab link to first surf spot result and parse page
  first_result_link = first_result_container.findChildren('a')[0]
  surf_url = first_result_link['href']
  html_text = requests.get(surf_url).text
  soup = BeautifulSoup(html_text, 'html.parser')

  # scrape information for surf spot
  # surf spot title
  title_container = soup.find('h1', { 'class' : 'sl-forecast-header__main__title'})

  # surf height
  surf_height_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--surf-height' })
  height_container = surf_height_container.findChildren('span', { 'class' : 'quiver-surf-height'})[0]
  height_description = surf_height_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]
  
  # tide height
  tide_container = soup.find('div', { 'class' : 'quiver-spot-forecast-summary__stat-container--tide'})
  tide_height_container = tide_container.findChildren('span', { 'class' : 'quiver-reading'})[0]
  tide_description_container = tide_container.findChildren('span', { 'class' : 'quiver-reading-description'})[0]
  
  # water and air temp
  water_temp_container = soup.find('div', { 'class' : 'quiver-water-temp'}).findChildren('div')[0]
  air_temp_container = soup.find('div', { 'class' : 'quiver-weather-stats'}).findChildren('div')[0]

  surf_message = constructMessage(
    title_container.getText().strip()[:-23], # Removing the text 'Surf Report & Forecast'
    surf_url,
    height_container.getText().strip(),
    height_description.getText(separator=' ').strip(),
    tide_height_container.getText().strip(),
    tide_description_container.getText(separator=' ').strip(),
    water_temp_container.getText().strip(),
    air_temp_container.getText().strip())

  # write to telegram
  update.message.reply_text(surf_message, parse_mode=ParseMode.HTML)

def constructMessage(title, url, surfHeight, surfHeightDesc, tideHeight, tideDesc, waterTemp, airTemp):
  return f'''<b>🏄{title}🏄</b>
<pre>
Surf Height:   {surfHeight}
{surfHeightDesc}
  
Tide Height:   {tideHeight}
{tideDesc}

Water Temp:    {waterTemp}
Air Temp:      {airTemp}</pre>

<a href="{url}">More Information at Surfline</a>'''


def main():
  updater = Updater('1568311946:AAEDnZVePDCh2DwkVd1jnK5g3icusDYiPyE')
  dp = updater.dispatcher
  dp.add_handler(CommandHandler('surf', surf, pass_args=True))
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()