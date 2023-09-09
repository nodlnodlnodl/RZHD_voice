import flet as ft
from text_to_speech import greetings
from speech_to_text import bot_activation

class Message():
    def __init__(self, user_name: str, text: str, message_type: str):
        self.user_name = user_name
        self.text = text
        self.message_type = message_type
        self.min_lines = 1

class ChatMessage(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment="start"
        self.controls=[
                ft.CircleAvatar(
                    content=ft.Text(self.get_initials(message.user_name)),
                    color=ft.colors.WHITE,
                    bgcolor= ft.colors.BROWN,
                 ),
                ft.Column(
                    [
                        ft.Text(wrap_text(message.text, max_length = 70), selectable=True, overflow=70, max_lines=2),
                    ],
                    tight=True,
                    spacing=5,
                   
                ),
            ]
    def get_initials(self, user_name: str):
            return "М"


class ChatMessageAI(ft.Row):
    def __init__(self, message: Message):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls = [
            ft.CircleAvatar(
                content=ft.Text(self.get_initials(message.user_name)),
                color=ft.colors.WHITE,
                bgcolor=ft.colors.YELLOW,
            ),
            ft.Column(
                [
                    ft.Text(wrap_text(message.text, max_length=70), selectable=True, overflow=70, max_lines=2),
                ],
                tight=True,
                spacing=5,

            ),
        ]

    def get_initials(self, user_name: str):
        return "AI"

def wrap_text(text, max_length):
    """
    Функция для разбиения текста на части по определенной длине.
    """
    return '\n'.join([text[i:i+max_length] for i in range(0, len(text), max_length)])

def main(page: ft.Page):
    page.window_height=400,
    page.window_width = 400,
    page.update(),
    page.horizontal_alignment = "stretch"
    page.title = "Помощник"
    c1 = ft.Container(
        ft.Text(style=ft.TextThemeStyle.HEADLINE_MEDIUM),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        border_radius= 100,
        bgcolor=ft.colors.BLUE_100,
    )
    c2 = ft.Container(
        ft.Text("Говорите!", size=30),
        alignment=ft.alignment.center,
        width=200,
        height=200,
        border_radius= 100,
        bgcolor=ft.colors.BLUE_300,
    )
    c = ft.AnimatedSwitcher(
        c1,
        transition=ft.AnimatedSwitcherTransition.SCALE,
        duration=500,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
        switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
    )
#запись голоса по кнопке
    def Voice_rec(e):
        c.content = c2 if c.content == c1 else c1
        c.update()
        greetings()

        print("записть идет")

#new_massage.value - значение сообщения
    def send_message_click(e):
        if new_message.value != "":
            page.pubsub.send_all(Message(page.session.get("user_name"), new_message.value, message_type="chat_message"))
            #запись сообщения в файл(каждое новое сообщение перезаписывает файл)
            new_message.value = ""
            new_message.focus()
            page.update()

    def on_message(message: Message):
        ItsUser = 0
        if ItsUser == 0:
            m = ChatMessage(message)
        else:
            m = ChatMessageAI(message)
        chat.controls.append(m)
        page.update()

    # def on_message(message: Message):
    #     if message.message_type == "chat_message":
    #         m = ChatMessage(message)
    #     elif message.message_type == "login_message":
    #         m = ft.Text(message.text, italic=True, color=ft.colors.BLACK45, size=16)
    #     chat.controls.append(m)
    #     page.update()
    page.pubsub.subscribe(on_message)

    # Сообщения чата
    chat = ft.ListView(
        width= 300,
        height= 300,
        expand=True,
        spacing=10,
        auto_scroll=True,
        
    )
    #Поле ввода ссобщений
    new_message = ft.TextField(
        hint_text="Задайте вопрос",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )
    #Добавление элементов
    page.add(c,
        ft.Container(
            width= 300,
            height= 300,
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
        ),
        ft.Row(
            [
                new_message,
                ft.Divider(),
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Отправить сообщение",
                    on_click=send_message_click,
                ),
            ]
        ),
         ft.IconButton(
                    icon=ft.icons.MIC,
                    tooltip="Записать сообщение",
                    on_click=Voice_rec,
                    style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=30),
                    icon_size= 150,
                ),
    )
ft.app(target=main)