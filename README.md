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

### TLDR: Provides player notifications in Discord DMs, and much more with the Hypixel API.
As the TLDR says above, this bot provides player notifications via Discord DMs. This is only available to self host, due to the nature of the bot maxing out a Hypixel API key. The bot is currently capable of tracking 32 players at a time, with 25 players allowed to be online at a time. The bot does save it's data around every 10 minutes, as well as every time the stop command is used by the owner. You can change these numbers inside of the bot if you would like, but you will need to stay under the Hypixel and Mojang API limits. Per user notification limit is set to 10, unless they are set up as owner. This is again easily changable by editing code. If you edit any code, you must make sure you are following the terms of the license for this project (GNU AFFERO v3). Instructions for how to do this are at the top of hycord.py

## Installation
### General Installation
1. Make a folder for the repository.
2. For all installation methods you will  need the ".env" file in the root of the repository. For Docker installation, that can be downloaded [here](https://github.com/ProfessorPiggos/HyCord/blob/master/.env). You can get this while cloning the repository with the manual method.
3. Edit the values in the ".env" file. You can do this by editing the values after the equals sign. Information on each value can be found below.
#### Required:
###### TOKEN
You must put a Discord bot token here. Google "Discord bot key tutorial" for info on how to get this token.
#### Optional:
###### PREFIX
Default = ","
Swap out the comma with something else if you want a different prefix.
###### OWNERID
Required for owner features (bypass max user limit, and be able to stop bot). Leave empty if you don't want these features. Look up "how to get Discord user id" for info on how to get this.
###### NOTIFICATIONS
Set to "on" if you want the notification service enabled (player notifs in dms), set to "off" if you want the notification service to be disabled.
###### APIKEY
Required for notification service. Look up "How to get hypixel api key" for info on how to get this. Minecraft account is required.

### Docker (Recommended)
This is the reccomended method of installation. You must install docker, but docker-compose isn't required.
In the folder with your ".env" file, run the command `docker run -d --env-file ./.env professorpiggos/hycord:latest`. That's all that you have to do. If you run this command when a new release has been added, it will automatically update. Releases are added on all sizeable feature updates, minor fixes aren't published.

You can also build your own image using the Dockerfile in the repository, or download an image from GitHub Packages. The packages on Github Packages are beta builds.  They may have more features, but may also be buggier. 
If you build directly from the development branch (this would be similar to an "alpha"), there is a chance that the code just flat-out won't work, as there is no QC on this branch.
### Manual
This isn't recommended as you won't get automatic updates on restart, but you can do it. 
1. Run the command `git clone https://github.com/ProfessorPiggos/HyCord/`.
2. Run the command `pip install -r requirements.txt`.
3. Run `python ./app/hycord.py`. If running on a server, run this inside of a `screen` instance.
## Requirements
### Python 3.8+
Programmed in Python 3.8.5. You must have at least 3.8, this is a dependency of the nextcord library.
### Discord account
(obviously)
### Minecraft Account
Needed for acquiring Hypixel API Key
### Docker (optional)
Only if you are using the docker installation method.
