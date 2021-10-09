# Hycord Discord Bot

<p align="center">
  <a href="https://github.com/ProfessorPiggos/HyCord/search?l=Python">
    <img src="https://img.shields.io/badge/language-python-blue?color=ffd343" alt="Python" />
  </a>
  <a href="https://github.com/ProfessorPiggos/HyCord/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/ProfessorPiggos/HyCord" alt="License" />
  </a>
  <a href="https://github.com/ProfessorPiggos/HyCord/stargazers">
    <img src="https://img.shields.io/github/stars/ProfessorPiggos/HyCord" alt="Stars" />
  </a>
  <a href="https://github.com/ProfessorPiggos/HyCord/network/members">
    <img src="https://img.shields.io/github/forks/ProfessorPiggos/HyCord" alt="Forks" />
  </a>
  <a href="https://github.com/ProfessorPiggos/HyCord/stargazers">
    <img src="https://img.shields.io/static/v1?label=%F0%9F%8C%9F&message=If%20You%20Find%20This%20Useful!&style=style=flat&color=33ff33" alt="Leave a Star!"/>
  </a>
</p>

#### TLDR: Provides player notifications in Discord DMs, and much more with the Hypixel API.

###### Longer Explanation:
As the TLDR says above, this bot provides player notifications via Discord DMs. This is only available to self host, due to the nature of the bot maxing out a Hypixel API key. The bot is currently capable of tracking 32 players at a time, with 25 players allowed to be online at a time. You can change these numbers inside of the bot if you would like, but you will need to stay under the Hypixel and Mojang API limits. Per user notification limit is set to 10, unless they are set up as owner. This is again easily changable by editing code. If you edit any code, you must make sure you are following the terms of the license for this project (GNU AFFERO v3). Instructions for how to do this are at the top of hycord.py

## Bot Configuration
#### All bot configuration is done in the file \app\\.env
Just swap out the values after the equal sign.
### Required:
###### TOKEN
You must put a Discord bot token here. Google "Discord bot key tutorial" for info on how to get this token.
### Optional:
###### PREFIX
Default = ","
Swap out the comma with something else if you want a different prefix.
###### OWNERID
Required for owner features (bypass max user limit, and be able to stop bot). Leave empty if you don't want these features. Look up "how to get Discord user id" for info on how to get this.
###### NOTIFICATIONS
Set to "on" if you want the notification service enabled (player notifs in dms), set to "off" if you want the notification service to be disabled.
###### APIKEY
Required for notification service. Look up "How to get hypixel api key" for info on how to get this. Minecraft account is required.

## Requirements
### Python 3.8+
Programmed in Python 3.8.5. You must have at least 3.8, this is a dependency of the nextcord library.
### Discord account
(obviously)
### Minecraft Account
Needed for acquiring Hypixel API Key