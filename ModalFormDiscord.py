from typing import Optional
import disnake
from disnake.ext import commands
from disnake import TextInputStyle

bot = commands.Bot(command_prefix="!")

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
        embed = disnake.Embed(title="Заявка", color=0x2F3136)
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        await bot.get_channel("Айди канала").send(embed=embed)
        await inter.author.send("вы заполнили заявку")
        await inter.response.send_message("")

class Confirm(disnake.ui.View):

        def __init__(self):
            super().__init__(timeout=0)

        @disnake.ui.button(label="Подать заявку", style=disnake.ButtonStyle.green)
        async def confirm(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
            await inter.response.send_modal(modal=MyModal())

@bot.slash_command()
async def tags(inter: disnake.AppCmdInter):
    view = Confirm()

    await inter.send("Заполни заявку", view=view)

bot.run("Токен")