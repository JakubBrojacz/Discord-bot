import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import emoji

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

description = '''
Bot for setting up Valorant team
'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?',
                   description=description, intents=intents)


async def btn_all(self, interaction: discord.Interaction, button: discord.ui.Button):
    button.label = interaction.user.display_name
    button.disabled = True
    button.style = discord.ButtonStyle.success
    await interaction.message.edit(view=self)
    await interaction.response.defer()


class DeleteEmbedView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.chair = []

    @discord.ui.button(label='1', style=discord.ButtonStyle.primary)
    async def btn_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        await btn_all(self, interaction, button)

    @discord.ui.button(label='2', style=discord.ButtonStyle.primary)
    async def btn_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await btn_all(self, interaction, button)

    @discord.ui.button(label='3', style=discord.ButtonStyle.primary)
    async def btn_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await btn_all(self, interaction, button)

    @discord.ui.button(label='4', style=discord.ButtonStyle.primary)
    async def btn_4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await btn_all(self, interaction, button)

    @discord.ui.button(label='5', style=discord.ButtonStyle.primary)
    async def btn_5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await btn_all(self, interaction, button)

    @discord.ui.button(label='0', style=discord.ButtonStyle.primary, emoji=emoji.emojize(':chair:'))
    async def btn_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.chair.append((interaction.user.id, interaction.user.display_name))
        button.label = f'{len(self.chair)}'
        await interaction.message.edit(view=self)
        await interaction.response.defer()

    @discord.ui.button(label='Call', style=discord.ButtonStyle.grey, emoji=emoji.emojize(':chair:'))
    async def btn_call_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not any(self.chair):
            await interaction.response.send_message('Nikogo na ławeczce...')
            return
        
        first_chair = self.chair[0]
        self.chair.pop(0)
        self.btn_chair.label = f'{len(self.chair)}'
        await interaction.message.edit(view=self)
        await interaction.response.send_message(f'Choć grać <@{first_chair[0]}>!')

    @discord.ui.button(label='Display all', style=discord.ButtonStyle.grey, emoji=emoji.emojize(':chair:'))
    async def btn_disp_chair(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Gracze na ławeczce:\n' + '\n'.join([
            f'{user[1]}'
            for user in self.chair
        ]))


@bot.command()
async def team(ctx):
    """Creates team voting."""
    role_id = discord.utils.get(ctx.guild.roles, name="Valoranciarze").id
    await ctx.send(f"Zbieramy drużynę <@&{role_id}>!", view=DeleteEmbedView())


bot.run(TOKEN)
