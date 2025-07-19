import flet as ft
from display import (
    login,
    HAB_list,
    HAB_detail,
    bulk_registration,
    master_menu,
    shop_master,
    master,
    CSV_master,
    users,
)


def main(page: ft.Page):
    page.title = "家計簿アプリ"
    page.window.resizable = False

    def route_change(e: ft.RouteChangeEvent):
        if page.route == "/login":
            page.views.append(login.Login(page))
        elif page.route == "/HAB_list":
            page.views.append(HAB_list.HAB_List(page, page.views[-1].data))
        elif page.route == "/bulk_registration":
            page.views.append(bulk_registration.Bulk_Registration(page))
        elif page.route == "/HAB_detail":
            page.views.append(HAB_detail.HAB_detail(page, page.views[-1].data))
        elif page.route == "/master_menu":
            page.views.append(master_menu.Master_Menu(page))
        elif page.route == "/shop_master":
            page.views.append(shop_master.Shop_Master_Display(page))
        elif page.route == "/master":
            page.views.append(master.Master_Display(page))
        elif page.route == "/CSV_master":
            page.views.append(CSV_master.CSV_Master_Display(page))
        elif page.route == "/user":
            page.views.append(users.Users_Display(page))
        page.update()

    page.on_route_change = route_change
    page.go("/login")


if __name__ == "__main__":
    ft.app(target=main)
