from typing import Optional
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=',', intents=intents)

# Наследуем модальное окно
class MyModal(disnake.ui.Modal):
    def __init__(self):
        # Детали модального окна и его компонентов
        components = [
            disnake.ui.TextInput(
                label="Ваш игровой никнейм",
                custom_id="Ваш игровой никнейм",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Ваш возвраст",
                custom_id="Ваш возвраст",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Чем планируете заниматься на сервере?",
                custom_id="Чем планируете заниматься на сервере?",
                style=TextInputStyle.paragraph,
                max_length=1024,
            ),
            disnake.ui.TextInput(
                label="Расскажите о себе, своих увлечениях",
                custom_id="Расскажите о себе, своих увлечениях",
                style=TextInputStyle.paragraph,
                max_length=1024,
            ),
        ]
        super().__init__(
            title="Заявка на сервер",
            custom_id="1",
            components=components,
        )

    # Обработка ответа, после отправки модального окна
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(color=0x2F3136)
        embed.set_author(name=f"{inter.author.name}#{inter.author.tag}",icon_url=inter.author.avatar)
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        message = await bot.get_channel(1041712732497510521).send(embed=embed)
        await message.add_reaction('✅')
        await inter.author.send("Вы заполнили анкету. Ожидайте проверки.")
        role = disnake.utils.get(inter.author.guild.roles, id = 1051269043090370680)
        await inter.author.add_roles(role)
        await inter.response.edit_message()
        payload = await bot.wait_for('raw_reaction_add', timeout=0)
        if str(payload.emoji) == '✅':
            role2 = disnake.utils.get(inter.author.guild.roles, id = 1012095465031999498)
            await inter.author.add_roles(role2)
            role = disnake.utils.get(inter.author.guild.roles, id = 1051506901344604231)
            await inter.author.remove_roles(role)
            await inter.author.send("Вы приняты!")

class Confirm(disnake.ui.View):

        def __init__(self):
            super().__init__(timeout=0)

        @disnake.ui.button(label="Подать заявку", style=disnake.ButtonStyle.green)
        async def confirm(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
            await inter.response.send_modal(modal=MyModal())

@bot.command()
async def tags(inter: disnake.AppCmdInter):
    if inter.channel.id == 1051497039084650608:
        view = Confirm()

        await inter.send("Заполни заявку", view=view)
    else:
        pass

bot.run("MTA0MTAyNzEzMTczNzY1NzQyNA.G4wwcI.FtXrUF7t9CA9Fk9_dH6JuwVuYh8K6XbdV47NJE")