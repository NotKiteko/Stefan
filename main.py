# Bazowany na OtOTPzUN 2
#
#
#

import logging
import sys
import os
from typing import Optional
from nextcord.interactions import Interaction

from nextcord.utils import MISSING

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

if not os.path.exists("data/"):
    os.makedirs("data")

if os.path.exists("data/latest.log"):
    os.remove("data/latest.log")
    
if not os.path.exists("data/pldata.log"):
    f = open("data/pldata.txt", "a")
    f.close()
    
file_handler = logging.FileHandler('data/latest.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


import discord
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from dotenv import load_dotenv
load_dotenv()

from mcrcon import MCRcon

    

intents = nextcord.Intents.default()
intents.message_content = True

help_command = commands.DefaultHelpCommand(no_category='Commands')  
bot = commands.Bot(intents=intents, help_command=help_command, description='', activity=nextcord.Game(name='Stary jest podczas wstawania...'), status=nextcord.Status.idle)

class verification(nextcord.ui.View):
    def __init__(self, *, auto_defer: bool = True) -> None:
        super().__init__(timeout=None, auto_defer=auto_defer)
    
    @nextcord.ui.button(
        label="Wpisz się", style=nextcord.ButtonStyle.primary,emoji= "🪑", 
        custom_id="verification-button"
        )
    async def verbtn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        
        """ await interaction.response.send_message('*Test Passed*', ephemeral=True)   """
        modal = vermod()
        await interaction.response.send_modal(modal)
        
class vermod(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Wpisz się na whiteliste",
            timeout=None
        )
        
        self.name = nextcord.ui.TextInput(
            label="Twoja nazwa w minecraft",
            min_length=3,
            max_length=16,
        )
        self.add_item(self.name)
        
    async def callback(self, interaction: nextcord.Interaction) -> None:
        user = interaction.user.id
        
        f = open("data/pldata.txt", "r")
        a = []
        a = f.read()
        f.close
        a = a.split()

        
        if str(user) in a:
            await interaction.response.send_message("Dodałeś już swoją nazwę do whitelisty! \nJeżeli się pomyliłeś lub chcesz ją zmienić napisz do administracji.", ephemeral=True)
        else:  
            rcon_host = str(os.getenv("RCON_IPADR"))
            rcon_passwd = str(os.getenv("RCON_PASSWD"))
            rcon_port = int(os.getenv("RCON_PORT"))
            print(rcon_host, rcon_passwd, rcon_port)
            with MCRcon(rcon_host, rcon_passwd, rcon_port) as mcr:
                resp = mcr.command("whitelist add "+self.name.value)
                print(resp)
            f = open("data/pldata.txt", "a")
            f.write(str(user)+" ")
            f.close()
            await interaction.response.send_message("Nick "+self.name.value+" został pomyślnie dodany do whitelisty. (Zaktualizowanie może potrwać parę minut).\nJeżeli tak się nie stanie napisz do administracji.", ephemeral=True)
        
                

@bot.slash_command(name="wl2325")
async def wl2325(interaction: Interaction, desc):
    if interaction.user.guild_permissions.administrator == 1:
        view = verification()
        await interaction.channel.send(desc, view=view)
    else:
        await interaction.response.send_message("Nie masz do tego permisji!", ephemeral=True)
    
    
    
logging.info("Stary zaczyna wstawać...")

@bot.event
async def on_ready():
    logging.info("Stary wstał!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Furry Gay Polska 🪑"), status=nextcord.Status.online)

TOKEN = os.getenv('DISCORD_TOKEN')

if __name__ == '__main__':
    bot.run(TOKEN)