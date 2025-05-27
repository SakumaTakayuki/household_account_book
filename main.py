import flet as ft

from db.create_table import Create_Table
from db.user_adapter import User_Adapter


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    create_table = Create_Table()
    isCreate = create_table.create_table()
    if isCreate:
        create_table.create_user()

    user_adapter = User_Adapter()
    user_adapter.user_row.user_id = "admin"
    user_adapter.user_row.entry_user_id = "admin"
    return_user = user_adapter.fill_user(user_adapter.user_row)

    txt_number = ft.TextField(
        value=return_user.return_user_row[0].user_id,
        text_align=ft.TextAlign.RIGHT,
        width=100,
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
