import flet as ft
from common.my_control import My_Control
from common.message import Message
from common.const import Const
from common.method import CommonMethod
from config.config import Config
from db.common.INSERT import Insert
from db.create_table import Create_Table
from db.users_adapter import Users_Adapter
import os


# 起動確認
class Startup_Confirmation(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        # コンフィグファイルがない
        if not os.path.isfile("config/config.ini"):
            msg = My_Control.Msgbox("STARTUP001W", Message.Message_Box.STARTUP001W)
            self.page.open(msg)
        else:
            # dbファイル存在チェック
            if os.path.isfile("db/household_account_book.db"):
                self.page.go("/login")
            else:
                msg = My_Control.Msgbox("STARTUP001I", Message.Message_Box.STARTUP001I)
                msg.actions = [
                    ft.TextButton("はい", on_click=lambda e: self.create_db(msg)),
                    ft.TextButton(
                        "いいえ", on_click=lambda e: self.page.window.close()
                    ),
                ]
                self.page.open(msg)
        control = [
            ft.Container(),
        ]
        # ウィンドウサイズと表示位置を設定
        arg_page.window.width = 505
        arg_page.window.height = 320
        CommonMethod.center_non_update(arg_page)
        # "/startup_confirmation"が呼び出された時にcontrolが表示されるように設定
        super().__init__("/startup_confirmation", control)

    def create_db(self, arg_msg):
        """
        OK押したらログイン画面に遷移する
        """
        # with open(file="db/household_account_book00.db", mode="w") as f:
        #    pass
        self.page.close(arg_msg)
        try:
            create_table = Create_Table()
            isCreate = create_table.create_table()
            if isCreate:
                user_adapter = Users_Adapter()
                return_user = user_adapter.fill_users(Const.Admin.USER_ID)
                if len(return_user.return_row) == 0:
                    create_table.create_user()

                Insert.insert()

                msg = My_Control.Msgbox("STARTUP002I", Message.Message_Box.STARTUP002I)
                msg.actions = [
                    ft.TextButton(
                        "はい", on_click=lambda e: self.msg_STARTUP002I_ok(msg)
                    ),
                ]
                self.page.open(msg)
            else:
                msg = My_Control.Msgbox("STARTUP002W", Message.Message_Box.STARTUP002W)
                self.page.open(msg)
        except Exception as e:
            msg = My_Control.Msgbox("STARTUP002W", Message.Message_Box.STARTUP002W)
            self.page.open(msg)

    def msg_STARTUP002I_ok(self, arg_msg):
        """
        データベース作成後、ログイン画面遷移
        """
        self.page.close(arg_msg)
        self.page.go("/login")
