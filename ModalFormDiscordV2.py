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
            title="Заявка на сервер", #название формы
            custom_id="1",
            components=components,
        )

    # Обработка ответа, после отправки модального окна
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(color=0x2F3136) #дизайн embed'a
        embed.set_author(name=f"{inter.author.name}#{inter.author.tag}",icon_url=inter.author.avatar) #от кого идёт заявка

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            ) #результаты
        
        await bot.get_channel("id канала").send(embed=embed) #id канала куда приходят результаты
        await inter.author.send("Вы заполнили анкету. Ожидайте проверки.") # сообщение в лс после отправления анкеты
        role = disnake.utils.get(inter.author.guild.roles, id = "id роли") #получаем айди роли
        await inter.author.add_roles(role) #добавляем роль человеку который отправил форму, чтобы он повторно ее не проходил
        await inter.response.edit_message() #чтобы не было ошибки "чтото не так. повторите попытку"

class Confirm(disnake.ui.View):

        def __init__(self):
            super().__init__(timeout=0)

        @disnake.ui.button(label="Подать заявку", style=disnake.ButtonStyle.green) #имя и цвет кнопки
        async def confirm(self, button: disnake.ui.Button, inter: disnake.AppCmdInter):
            await inter.response.send_modal(modal=MyModal()) #при нажатии на кнопку отправляет форму

@bot.slash_command()
async def tags(inter: disnake.AppCmdInter):
    view = Confirm()

    await inter.send("Заполни заявку", view=view) #показ кнопки

bot.run("TOKEN")