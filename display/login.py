import flet as ft
from db.login_adapter import Login_Adapter
from common.my_control import My_Control


class Login(ft.View):
    def __init__(self):
        self.user_adapter = Login_Adapter()
        self.display_label = ft.Container(
            content=ft.Text(
                "ログイン",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),
            alignment=ft.alignment.center,
        )
        self.id_TextField = ft.TextField(
            label=ft.Text("ユーザーID", size=18), bgcolor=ft.Colors.WHITE
        )
        self.password_TextField = ft.TextField(
            label=ft.Text("パスワード", size=18), password=True, bgcolor=ft.Colors.WHITE
        )
        self.submit = ft.FilledButton(
            content=ft.Text("ログイン", size=18),
            width=100,
            height=40,
            disabled=False,
            on_click=lambda e: Login.login_submit_click(self, e),
        )
        control = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        self.id_TextField,
                        self.password_TextField,
                        self.submit,
                    ]
                ),
                border=ft.border.all(2.0, ft.Colors.BLACK),
                padding=20,
            )
        ]
        super().__init__("/login", control)

    def login_submit_click(self, arg_e):
        id = self.controls[0].content.controls[0].value
        password = self.controls[0].content.controls[1].value
        user_row = self.user_adapter.login(
            self.user_adapter.const.Fill_Kbn.FIRST,
            id,
            password,
            self.user_adapter.const.Login.USER_ID,
        )
        if user_row.return_row is None:
            msg = My_Control.Msgbox(
                user_row.return_message_box.message_id,
                user_row.return_message_box.message_text,
            )
            self.page.open(msg)
        else:
            arg_e.page.go("/HAB_list")


def main(page: ft.Page):
    t = Login(page)
    page.title = "家計簿アプリ"
    page.window.width = 505
    page.window.height = 315
    page.window.min_width = 500
    page.window.min_height = 275
    page.bgcolor = ft.Colors.LIGHT_BLUE_50
    page.window.center()
    page.add(t.display_label, t.control)


if __name__ == "__main__":
    ft.app(target=main)
