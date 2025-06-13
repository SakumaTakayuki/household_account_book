import flet as ft
from db.login_adapter import Login_Adapter
from common.my_control import My_Control
from common.message import Message
from common.const import Const


# ログイン画面
class Login(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        # ログインアダプターをインスタンス化
        self.login_adapter = Login_Adapter()
        # 画面ラベル作成
        self.display_label = ft.Container(
            content=ft.Text(
                "ログイン",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),
            alignment=ft.alignment.center,
        )
        # ユーザーID入力エリア作成
        self.id_TextField = ft.TextField(
            label=ft.Text("ユーザーID", size=18), bgcolor=ft.Colors.WHITE, text_size=18
        )
        # パスワード入力エリア作成
        # password=Trueで入力した値がマスクされるように設定
        self.password_TextField = ft.TextField(
            label=ft.Text("パスワード", size=18),
            password=True,
            bgcolor=ft.Colors.WHITE,
            text_size=18,
        )
        # ログインボタン作成
        # ボタンクリック時にlogin_submit_clickを呼び出す
        self.submit = ft.FilledButton(
            content=ft.Text("ログイン", size=18),
            width=100,
            height=40,
            disabled=False,
            on_click=lambda e: Login.login_submit_click(self),
        )
        # controlに作成したコントロールを追加する
        # ユーザーID入力エリア、パスワード入力エリア、ログインボタンは縦並びかつ枠線内にあるデザインにするため
        # ft.Container内にft.Column(縦並び)で配置し、ft.Containerに枠線を設定する
        control = [
            self.display_label,
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
            ),
        ]
        # ウィンドウサイズと表示位置を設定
        arg_page.window.width = 505
        arg_page.window.height = 320
        arg_page.window.center()
        # "/login"が呼び出された時にcontrolが表示されるように設定
        super().__init__("/login", control)

    def login_submit_click(self):
        """
        ログインボタンクリックイベント
        """
        # 画面を非活性にする
        self.disabled = True
        self.update()
        # idにユーザーIDを代入する
        id = self.controls[1].content.controls[0].value
        # idの入力値チェック
        if id == "":
            msg = My_Control.Msgbox(
                "HAB005C",
                Message.Message_Box.HAB005C.format("ユーザーID"),
            )
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(msg)
            # 画面を活性にする
            self.disabled = False
            self.update()
            return
        # passwordにパスワードを代入する
        password = self.controls[1].content.controls[1].value
        # passwordの入力値チェック
        if password == "":
            msg = My_Control.Msgbox(
                "HAB005C",
                Message.Message_Box.HAB005C.format("パスワード"),
            )
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(msg)
            # 画面を活性にする
            self.disabled = False
            self.update()
            return
        # ログインアダプターを使用し、ログイン認証を行う
        # user_rowにはユーザー情報、ログイン失敗メッセージが代入されている
        user_row = self.login_adapter.login(
            id,
            password,
        )
        # user_row.return_rowにユーザー情報がない場合
        if user_row.return_row is None:
            # user_row.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                user_row.return_message_box.message_id,
                user_row.return_message_box.message_text,
            )
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(msg)
            # 画面を活性にする
            self.disabled = False
            self.update()
        else:
            # self.page.dataにユーザー情報を代入し、どの画面でもユーザー情報を参照できるようにする
            self.page.data = user_row.return_row
            # 家計簿一覧画面を表示する
            self.page.go("/HAB_list")
