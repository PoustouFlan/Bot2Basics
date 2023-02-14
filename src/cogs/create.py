from typing import List, Optional

import discord
from discord import ui
from discord.ext import commands
from discord import app_commands
from bot_utils import guild_object

from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, "fr_FR")

from data.models import *

import logging
log = logging.getLogger("Bot2Basics")

class CreateTimeModal(ui.Modal, title = "Horaire du cours"):
    date = ui.TextInput(
        label = "📆 Date",
        style = discord.TextStyle.short,
        placeholder = "31/01/1970",
        required = True,
        min_length = 8,
        max_length = 10,
    )
    time = ui.TextInput(
        label = "⏰ Heure",
        style = discord.TextStyle.short,
        placeholder = "08h00",
        required = True,
        min_length = 2,
        max_length = 5,
    )
    duration = ui.TextInput(
        label = "⏳ Durée",
        style = discord.TextStyle.short,
        placeholder = "2h30",
        required = True,
        min_length = 2,
        max_length = 5,
    )

    def __init__(self, view):
        self.view = view
        super().__init__()

    async def on_submit(self, interaction):
        await self.view.modal_time(interaction, self)

class CreateSubjectModal(ui.Modal, title = "Sujet du cours"):
    topic = ui.TextInput(
        label = "📣 Intitulé",
        style = discord.TextStyle.short,
        placeholder = "Équations différentielles",
        required = True,
    )
    mode = ui.TextInput(
        label = "💻 Distanciel/Présentiel",
        style = discord.TextStyle.short,
        placeholder = "Les deux",
        required = True,
    )

    def __init__(self, view):
        self.view = view
        super().__init__()

    async def on_submit(self, interaction):
        await self.view.modal_subject(interaction, self)


class CreateView(ui.View):
    start:    Optional[datetime]             = None
    duration: Optional[int]                  = None
    semester: Optional[int]                  = None
    subject:  Optional[str]                  = None
    topic:    Optional[str]                  = None
    mode:     Optional[str]                  = None
    teachers: Optional[List[discord.Member]] = None

    @ui.button(
        label = "Sélectionner l'horaire",
        row = 0,
    )
    async def button_time(self, interaction, button):
        modal = CreateTimeModal(self)
        await interaction.response.send_modal(modal)

    async def modal_time(self, interaction, modal):
        day, month, year = map(int, modal.date.value.split('/'))

        if modal.time.value[-1] == 'h':
            hour = int(modal.time.value[:-1])
            minute = 0
        else:
            hour, minute = map(int, modal.time.value.split('h'))

        start = datetime(year, month, day, hour, minute)

        if modal.duration.value[-1] == 'h':
            hours = int(modal.duration.value[:-1])
            minutes = 0
        else:
            hours, minutes = map(int, modal.duration.value.split('h'))

        duration = hours * 60 + minutes

        self.start = start
        self.duration = duration

        start_str = start.strftime("%A %d %B %Y à %Hh%M")
        duration_str = f"{hours}h{minutes:02d}"

        button = self.children[0]
        button.style = discord.ButtonStyle.green
        button.label = f"{start_str}, {duration_str}"
        await interaction.response.edit_message(
            view = self
        )

    @ui.button(
        label = "Sélectionner le sujet",
        row = 0,
    )
    async def button_subject(self, interaction, button):
        modal = CreateSubjectModal(self)
        await interaction.response.send_modal(modal)

    async def modal_subject(self, interaction, modal):
        self.topic = modal.topic
        self.mode  = modal.mode

        button = self.children[1]
        button.style = discord.ButtonStyle.green
        button.label = f"{modal.topic}, {modal.mode}"

        await interaction.response.edit_message(
            view = self
        )

    @ui.select(
        placeholder = "Semestre concerné",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(label = "S1"),
            discord.SelectOption(label = "S2"),
            discord.SelectOption(label = "S3"),
            discord.SelectOption(label = "S4"),
        ],
        row = 1,
    )
    async def select_semester(self, interaction, select):
        self.semester = int(select.values[0][-1])
        await interaction.response.defer()

    @ui.select(
        placeholder = "📚 Matière enseignée",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(label = "Algorithmique"),
            discord.SelectOption(label = "Architecture"),
            discord.SelectOption(label = "Électronique"),
            discord.SelectOption(label = "Mathématiques"),
            discord.SelectOption(label = "Physique"),
            discord.SelectOption(label = "Programmation"),
        ],
        row = 2,
    )
    async def select_subject(self, interaction, select):
        self.subject = select.values[0]
        await interaction.response.defer()

    @ui.select(
        cls = ui.UserSelect,
        placeholder = "👾 Professeur",
        min_values = 1,
        max_values = 3,
        row = 3,
    )
    async def select_teacher(self, interaction, select):
        self.teachers = select.values
        await interaction.response.defer()

    @ui.button(
        style = discord.ButtonStyle.primary,
        label = "Ça part en prod !",
        row = 4,
    )
    async def on_submit(self, interaction, button):
        if self.start is None or self.duration is None:
            await interaction.response.send_message(
                "L'horaire du cours n'est pas renseignée !",
                ephemeral = True
            )
            return
        if self.mode is None or self.topic is None:
            await interaction.response.send_message(
                "Le sujet du cours n'est pas renseigné !",
                ephemeral = True
            )
            return
        if self.semester is None:
            await interaction.response.send_message(
                "Le semestre n'est pas renseigné !",
                ephemeral = True
            )
            return
        if self.subject is None:
            await interaction.response.send_message(
                "La matière n'est pas renseignée !",
                ephemeral = True
            )
            return
        if self.teachers is None:
            await interaction.response.send_message(
                "Les professeurs ne sont pas renseignés !",
                ephemeral = True
            )
            return

        teachers = []
        for member in self.teachers:
            student = await Student.get_student(member)
            if student is None:
                await interaction.response.send_message(
                    f"{member.mention} n'est pas enregistré !"
                )
                return
            teachers.append(student)

        course = Course(
            start = self.start,
            duration = self.duration,
            semester = self.semester,
            subject = self.subject,
            topic = self.topic,
            mode = self.mode,
        )

        await course.save()
        await course.teachers.add(*teachers)

        # TODO
        await interaction.response.defer()


class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sync(self, ctx):
        log.info("Syncing...")
        fmt = await ctx.bot.tree.sync(guild = ctx.guild)
        s = "" if len(fmt) < 2 else "s"
        log.info("Sync complete")
        await ctx.send(f"{len(fmt)} commande{s} synchronisée{s}.")

    @app_commands.command(
        name = "create",
        description = "Créée un nouveau cours"
    )
    async def create(self, interaction):
        await interaction.response.send_message(
            view = CreateView()
        )

async def setup(bot):
    await bot.add_cog(Create(bot), guilds = [guild_object])
