# vindinium-python

An awesome python client for Vindinium.

Vindinium is an online and continuous competition where you control a bot in a turn-based game, consult [the site](http://vindinium.org) to know more.

This library provides a simple bot, helper structures and common algorithms that allow you to create bots in an easy and fast way, focusing on the strategy and specific techniques of your bot.

The library has the following features:

- Bots:
  - MinerBot: a bot that looks for mines continuously.
  - AggressiveBot: a bot that only goes after other bots.

- Models (used by base bot to create the game structure):
  - Game: stores all other models.
  - Map: stores static information about the map.
  - Mine: represents a mine in the map.
  - Hero: represents a hero in the game.
  - Tavern: represents a tavern in the game.

Note: this client fixes the inconsistent axis of the server, so you don't have to worry about that (if you're using the game model).

## Setup

- install python (https://www.python.org/ftp/python/2.7.12/python-2.7.12.amd64.msi)
- make sure python and pip are in the path
- pip install requests

- go to http://aigamesvm:9000 and create a bot
- replace the key in main.py

## Usage

    python .\main.py