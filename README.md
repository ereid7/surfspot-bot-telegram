# Surf Spot Bot

Surf Spot Bot is a Telegram bot used for getting current surf report for a given surf spot. The bot does not get it's information from any API, but rather scrapes the information from Surfline using the BeautifulSoup.

---

## Usage

To retrieve a surf report from the bot, use the `/surf <..spotname>` command. The arguments will be parsed as strings and used to search for a surf spot.

For example,
```/surf la jolla shores```
will search surfline.com for "la jolla shores" and retrieve the surf report for the first search result.

---

## Requirements
- python3 
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot "python-telegram-bot")
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/ "beautifulsoup4")

---

## Running the Bot
- Install the above requirements using `pip`
- Set the variable `TELEGRAM_TOKEN` in `src/main.py` to your telegram bot token
- Start the bot with `python main.py`


## Screenshot

![SurfSpotBot](surfspotbot_example.png "SurfSpotBot")
