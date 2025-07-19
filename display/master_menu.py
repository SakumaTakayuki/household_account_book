import flet as ft
from common.my_control import My_Control
from common.const import Const
from common.method import CommonMethod
from config import Config


# 一括登録画面
class Master_Menu(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # ヘッダ部エリア作成
        self.header = My_Control.Header_Area(Const.Display.MASTER_MENU)
        self.header.back_button.on_click = lambda e: self.back()
        # 店舗マスタボタン作成
        # ボタンクリックで店舗マスタ画面に遷移する
        self.shop_master_button = ft.FilledButton(
            content=ft.Text("店舗マスタ", size=18),
            width=150,
            height=40,
            on_click=lambda e: self.go_shop_master_page(),
        )
        # マスタボタン作成
        # ボタンクリックでマスタ画面に遷移する
        self.master_button = ft.FilledButton(
            content=ft.Text("マスタ", size=18),
            width=150,
            height=40,
            on_click=lambda e: self.go_master_page(),
        )
        # CSV取込マスタボタン作成
        # ボタンクリックでCSV取込マスタ画面に遷移する
        self.CSV_master_button = ft.FilledButton(
            content=ft.Text("CSV取込マスタ", size=18),
            width=150,
            height=40,
            on_click=lambda e: self.go_CSV_master_page(),
        )
        # ユーザーマスタボタン作成
        # ボタンクリックでユーザーマスタ画面に遷移する
        self.user_button = ft.FilledButton(
            content=ft.Text("ユーザーマスタ", size=18),
            width=150,
            height=40,
            on_click=lambda e: self.go_user_page(),
        )
        # controlsに作成したコントロールを追加する
        controls = [
            ft.Column(
                controls=[
                    self.header.control,
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[
                                        self.shop_master_button,
                                        self.master_button,
                                        self.CSV_master_button,
                                        self.user_button,
                                    ],
                                    spacing=50,
                                ),
                            ],
                            spacing=15,
                        ),
                        border=ft.border.all(2.0, ft.Colors.BLACK),
                        padding=20,
                        height=285,
                    ),
                ],
                expand=True,
            ),
            self.overlay,
        ]
        # ウィンドウサイズと表示位置を設定
        self.page.window.width = Config.window_size.master_menu.width
        self.page.window.height = Config.window_size.master_menu.height
        CommonMethod.center_non_update(self.page)
        # "/master_menu"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/master_menu", controls)

    def back(self):
        """
        家計簿一覧に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        self.page.views.pop()
        self.page.window.width = Config.window_size.HAB_list.width
        self.page.window.height = Config.window_size.HAB_list.height
        CommonMethod.center_non_update(self.page)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.go("/back")

    def go_shop_master_page(self):
        """
        店舗マスタ画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # 店舗マスタ画面を表示する
        self.page.go("/shop_master")

    def go_master_page(self):
        """
        マスタ画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # マスタ画面を表示する
        self.page.go("/master")

    def go_CSV_master_page(self):
        """
        CSV取込マスタ画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # CSV取込マスタ画面を表示する
        self.page.go("/CSV_master")

    def go_user_page(self):
        """
        ユーザーマスタ画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # ユーザーマスタ画面を表示する
        self.page.go("/user")
