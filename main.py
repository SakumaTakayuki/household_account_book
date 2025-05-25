import flet as ft
from engine import Engine

# from user_adapter import User_Adapter
from test_adapter import User_Adapter


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    db_engine = Engine()
    db_engine.create_table()

    user_adapter = User_Adapter()
    create_row = user_adapter.user_row
    create_row.user_id = "999"
    create_row.name = "998"
    create_row.password = "997"
    user_adapter.create_row(create_row)
    row = user_adapter.fill_row("test104")

    txt_number = ft.TextField(
        value=row.user_id, text_align=ft.TextAlign.RIGHT, width=100
    )

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.Icons.ADD, on_click=plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )


ft.app(main)
