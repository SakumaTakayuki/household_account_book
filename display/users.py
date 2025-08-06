import flet as ft
from db.models import User
from common.my_control import My_Control
from common.const import Const
from common.method import CommonMethod
from db.users_adapter import Users_Adapter
from db.models import User
from common.message import Message
from config.config import Config


# ユーザーマスタ画面
class Users_Display(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        self.config = Config()
        self.fill_users_list = None
        self.isAddition = False
        self.update_version = None
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # ユーザーマスタアダプターをインスタンス化
        self.users_adapter = Users_Adapter()
        # ユーザーマスタ一覧作成
        self.users_list = My_Control.HAB_LIST(self.page)
        self.users_list.details_button_setting = False
        set_return = self.users_list_data_set()
        # ユーザーマスタ一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(set_return)
        else:
            # ヘッダ部エリア作成
            self.header = My_Control.Header_Area(Const.Display.USERS)
            self.header.back_button.on_click = lambda e: self.back()
            # 追加ボタン作成
            # ボタンクリックで追加モードに切り替える
            self.addition_button = ft.FilledButton(
                content=ft.Text("追加", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.addition(),
            )
            # 編集ボタン作成
            # ボタンクリックで追加モードに切り替える
            self.edit_button = ft.FilledButton(
                content=ft.Text("編集", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.edit(),
            )
            # ボタンエリア作成
            self.button_area = ft.Row(
                controls=[self.addition_button, self.edit_button],
                alignment=ft.MainAxisAlignment.END,
            )
            # ユーザーIDテキストボックス
            self.user_id_textField = ft.TextField(
                label=ft.Text("ユーザーID", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=250,
                max_length=20,
                text_size=18,
                input_filter=ft.InputFilter(
                    regex_string=r"^[0-9a-zA-Z!-/:-@[-´{-~]*$", replacement_string=""
                ),
            )
            # 名前テキストボックス
            self.name_text_textField = ft.TextField(
                label=ft.Text("名前", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
            )
            # パスワードテキストボックス
            self.password_textField = ft.TextField(
                label=ft.Text("パスワード", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=250,
                max_length=20,
                text_size=18,
                input_filter=ft.InputFilter(
                    regex_string=r"^[0-9a-zA-Z!-/:-@[-´{-~]*$", replacement_string=""
                ),
            )
            # 削除チェックボックス
            self.del_flg_checkbox = ft.Checkbox(
                label=ft.Text(
                    value="削除",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                ),
                value=False,
                check_color=ft.Colors.RED,
                active_color=ft.Colors.WHITE,
            )
            # 登録ボタン作成
            # ボタンクリックで入力したユーザーマスタを登録する
            self.entry_button = ft.FilledButton(
                content=ft.Text("登録", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.user_entry_check(),
            )
            # 入力エリア作成
            self.edit_area = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                self.user_id_textField,
                                self.password_textField,
                            ]
                        ),
                        self.name_text_textField,
                        ft.Row(
                            controls=[self.entry_button, self.del_flg_checkbox],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                    ],
                    spacing=15,
                ),
                border=ft.border.all(2.0, ft.Colors.BLACK),
                padding=20,
                disabled=True,
            )
            # controlsに作成したコントロールを追加する
            controls = [
                ft.Column(
                    controls=[
                        self.header.control,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.users_list.control,
                                    self.button_area,
                                    self.edit_area,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                expand=True,
                            ),
                            border=ft.border.all(2.0, ft.Colors.BLACK),
                            padding=20,
                        ),
                    ],
                    expand=True,
                ),
                self.overlay,
            ]
        # ウィンドウサイズと表示位置を設定
        self.page.window.width = self.config.window_size.users.width
        self.page.window.height = self.config.window_size.users.height
        self.page.window.center()
        # "/master"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/users", controls)

    def users_list_data_set(self):
        """
        ユーザーマスタ一覧のデータをセット
        """
        # ユーザーマスタ一覧取得
        fill_users = self.users_adapter.fill_users(self.page.data[0].user_id)
        self.fill_users_list = fill_users.return_row
        column_name = []
        row_list = []
        if fill_users.return_message_box.message_id is None:
            # 一覧の列名取得
            column_name = self.config.users_column_name.column_name
            users_row: User
            # 取得したユーザーマスタ一覧をself.users_listにデータをセットできるように加工
            for users_row in fill_users.return_row:
                row = [
                    users_row.user_id,
                    users_row.user_id,
                    users_row.name,
                    users_row.del_flg,
                ]
                row_list.append(row)
            # self.users_listにデータをセットする
            self.users_list.set_data_list(column_name, row_list, False)
            return None
        else:
            # fill_users.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_users.return_message_box.message_id,
                fill_users.return_message_box.message_text,
            )
            return msg

    def back(self):
        """
        ユーザーマスタメニューに遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        self.page.views.pop()
        self.page.window.width = self.config.window_size.master_menu.width
        self.page.window.height = self.config.window_size.master_menu.height
        CommonMethod.center_non_update(self.page)
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        self.page.go("/back")

    def addition(self):
        """
        追加モードに切り替える
        """
        # 画面を非活性にする
        self.overlay.visible = True
        # 追加フラグを変更する
        self.isAddition = True
        # 入力エリアを活性にする
        self.edit_area.disabled = False
        # 入力エリアのコントロールを入力制御する
        self.user_id_textField.read_only = False
        self.del_flg_checkbox.disabled = True
        # 入力エリアを初期化する
        self.user_id_textField.value = Const.Const_Text.TEXT_BLANK
        self.name_text_textField.value = Const.Const_Text.TEXT_BLANK
        self.password_textField.value = Const.Const_Text.TEXT_BLANK
        self.del_flg_checkbox.value = False
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def edit(self):
        """
        編集モードに切り替える
        """
        # 画面を非活性にする
        self.overlay.visible = True
        # 追加フラグを変更する
        self.isAddition = False
        # 行を選択していない場合
        if self.users_list.selected_row_value is None:
            # 編集する行を選択するメッセージを表示する
            msg = My_Control.Msgbox("HAB008C", Message.Message_Box.HAB008C)
            self.page.open(msg)
        else:
            # 入力エリアを活性にする
            self.edit_area.disabled = False
            # 入力エリアのコントロールを入力制御する
            self.user_id_textField.read_only = True
            self.del_flg_checkbox.disabled = False
            # 入力エリアのコントロールに選択行のデータをセットする
            selected_row = int(self.users_list.selected_row_value)
            self.user_id_textField.value = self.fill_users_list[selected_row].user_id
            self.name_text_textField.value = self.fill_users_list[selected_row].name
            self.password_textField.value = Const.Const_Text.TEXT_BLANK
            if (
                self.fill_users_list[selected_row].del_flg
                == Const.Const_Text.TEXT_BLANK
            ):
                self.del_flg_checkbox.value = False
            else:
                self.del_flg_checkbox.value = True
            self.update_version = self.fill_users_list[selected_row].update_version
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def user_entry_check(self):
        """
        削除処理か判定
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        if self.del_flg_checkbox.value:
            msg = My_Control.Msgbox("HAB005I", Message.Message_Box.HAB005I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.user_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
            self.page.open(msg)
        else:
            # 入力値チェック
            return_msg = self.value_check()
            self.page.open(return_msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def value_check(self):
        """
        入力値チェック
        """
        # 入力値チェック
        if self.user_id_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("ユーザーID")
            )
        elif self.name_text_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("名前")
            )
        elif (
            self.password_textField.value == "" and self.del_flg_checkbox.value == False
        ):
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("パスワード")
            )
        else:
            msg = My_Control.Msgbox("HAB004I", Message.Message_Box.HAB004I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.user_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
        return msg

    def user_entry(self, arg_msg):
        """
        ユーザーマスタを登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # ユーザーマスタに登録するデータを作成する
        users_row = User()
        users_row.user_id = self.user_id_textField.value
        # 削除にチェックがある場合
        if self.del_flg_checkbox.value:
            users_row.update_user_id = self.page.data[0].user_id
            users_row.update_version = self.update_version
            return_users = self.users_adapter.delete_users(users_row)
        else:
            users_row.name = self.name_text_textField.value
            users_row.password = self.password_textField.value
            if self.isAddition:
                users_row.entry_user_id = self.page.data[0].user_id
                # ユーザーマスタアダプターを使用し、新規登録を行う
                # return_usersには登録成功かエラーのメッセージが代入されている
                return_users = self.users_adapter.create_users(
                    users_row, self.page.data[0].user_id
                )
            else:
                if self.del_flg_checkbox.value:
                    users_row.del_flg = Const.Del_flg.DELETE
                else:
                    users_row.del_flg = Const.Del_flg.NON_DELETE
                users_row.update_user_id = self.page.data[0].user_id
                users_row.update_version = self.update_version
                # ユーザーマスタアダプターを使用し、更新を行う
                # return_usersには登録成功かエラーのメッセージが代入されている
                return_users = self.users_adapter.update_users(users_row)
        # return_users.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_users.return_message_box.message_id,
            return_users.return_message_box.message_text,
        )
        # メッセージ情報が登録完了の場合
        if return_users.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.entry_msg_yes(msg))
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def entry_msg_yes(self, arg_msg):
        """
        ユーザーマスター登録完了メッセージ用
        ユーザーマスタ一覧更新
        """
        self.page.close(arg_msg)
        # ユーザーマスタ一覧を更新する
        msg = self.users_list_data_set()
        # ユーザーマスタ一覧に表示するデータが取得できなかった場合
        if msg is not None:
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(msg)
        else:
            # ユーザーマスタ一覧コントロールを更新する
            self.controls[0].controls[1].content.controls[0] = self.users_list.control
            # 入力エリアを非活性にする
            self.edit_area.disabled = True
            # 入力エリアのコントロールを入力制御する
            self.del_flg_checkbox.disabled = True
            # 入力エリアを初期化する
            self.user_id_textField.value = Const.Const_Text.TEXT_BLANK
            self.name_text_textField.value = Const.Const_Text.TEXT_BLANK
            self.password_textField.value = Const.Const_Text.TEXT_BLANK
            self.del_flg_checkbox.value = False
            self.users_list.selected_row_value = None
        self.page.update()
