import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

from data.models import *

import logging
log = logging.getLogger("Bot2Basics")

class LoginModal(ui.Modal, title = "Inscrivez votre login"):
    login = ui.TextInput(
        label = "Indiquez votre login CRI",
        placeholder = "joseph.marchand",
        min_length = 3,
        max_length = 255,
    )

    async def on_submit(self, interaction):
        await Login.set_login(interaction, self.login.value)

class Login(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "login",
        description = "enregistre le login d'un utilisateur"
    )
    async def login(self, interaction, login: str = ""):
        if login == "":
            modal = LoginModal()
            await interaction.response.send_modal(modal)
        else:
            await Login.set_login(interaction, login)


    @staticmethod
    async def set_login(interaction, login):
        created = await Student.create_student_or_update(
            interaction.user,
            login
        )
        if created:
            await interaction.response.send_message(
                "Utilisateur enregistré avec succès !"
            )
        else:
            await interaction.response.send_message(
                "Login mis à jour avec succès !"
            )


async def setup(bot):
    await bot.add_cog(Login(bot), guilds = [guild_object])
