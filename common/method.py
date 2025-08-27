import flet as ft
import time


class CommonMethod:
    """
    共通メソッド
    """

    def center_non_update(arg_page: ft.Page):
        """
        非更新中央寄せ
        """
        arg_page._set_attr("windowCenter", str(time.time()))

    def on_resize(arg_overlay, arg_page: ft.Page):
        """
        画面サイズ変更
        """
        arg_overlay.controls[0].width = arg_page.window.width
        arg_overlay.controls[0].height = arg_page.window.height
