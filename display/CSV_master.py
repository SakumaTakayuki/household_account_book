import flet as ft
from db.models import User
from common.my_control import My_Control
from common.const import Const
from common.method import CommonMethod
from db.CSV_master_adapter import CSV_Master_Adapter
from db.models import CSV_Master
from common.message import Message
from config.config import Config


# CSVマスタ画面
class CSV_Master_Display(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        self.config = Config()
        self.fill_CSV_master_list = None
        self.isAddition = False
        self.update_version = None
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # CSVマスタアダプターをインスタンス化
        self.CSV_master_adapter = CSV_Master_Adapter()
        # CSVマスタ一覧作成
        self.CSV_master_list = My_Control.HAB_LIST(self.page)
        self.CSV_master_list.details_button_setting = False
        set_return = self.CSV_master_list_data_set()
        # CSVマスタ一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(set_return)
        else:
            # ヘッダ部エリア作成
            self.header = My_Control.Header_Area(Const.Display.CSV_MASTER)
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
            # コードテキストボックス
            self.code_textField = ft.TextField(
                label=ft.Text("コード", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
                input_filter=ft.InputFilter(
                    regex_string=r"^[0-9a-zA-Z!-/:-@[-´{-~]*$", replacement_string=""
                ),
            )
            # 利用日時テキストボックス
            self.HAB_at_text_textField = ft.TextField(
                label=ft.Text("利用日時", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
            )
            # 金額テキストボックス
            self.amount_text_textField = ft.TextField(
                label=ft.Text("金額", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
            )
            # 家計簿詳細テキストボックス
            self.HABdetail_text_textField = ft.TextField(
                label=ft.Text("家計簿詳細", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
            )
            # 文字コードテキストボックス
            self.character_code_textField = ft.TextField(
                label=ft.Text("文字コード", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
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
            # ボタンクリックで入力したCSVマスタを登録する
            self.entry_button = ft.FilledButton(
                content=ft.Text("登録", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.CSV_master_entry_check(),
            )
            # 入力エリア作成
            self.edit_area = ft.Container(
                content=ft.Column(
                    controls=[
                        self.code_textField,
                        ft.Row(
                            controls=[
                                self.HAB_at_text_textField,
                                self.amount_text_textField,
                                self.HABdetail_text_textField,
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.character_code_textField,
                            ]
                        ),
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
                                    self.CSV_master_list.control,
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
        self.page.window.width = self.config.window_size.CSV_master.width
        self.page.window.height = self.config.window_size.CSV_master.height
        CommonMethod.center_non_update(self.page)
        # "/CSV_master"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/CSV_master", controls)

    def CSV_master_list_data_set(self):
        """
        CSVマスタ一覧のデータをセット
        """
        # CSVマスタ一覧取得
        fill_CSV_master = self.CSV_master_adapter.fill_CSV_master(
            self.page.data[0].user_id
        )
        self.fill_CSV_master_list = fill_CSV_master.return_row
        column_name = []
        row_list = []
        if fill_CSV_master.return_message_box.message_id is None:
            # 一覧の列名取得
            column_name = self.config.CSV_master_column_name.column_name
            CSV_master_row: CSV_Master
            # 取得したCSVマスタ一覧をself.CSV_master_listにデータをセットできるように加工
            for CSV_master_row in fill_CSV_master.return_row:
                row = [
                    CSV_master_row.code,
                    CSV_master_row.code,
                    CSV_master_row.HAB_at_text,
                    CSV_master_row.amount_text,
                    CSV_master_row.HABdetail_text,
                    CSV_master_row.character_code,
                    CSV_master_row.del_flg,
                ]
                row_list.append(row)
            # self.CSV_master_listにデータをセットする
            self.CSV_master_list.set_data_list(column_name, row_list, False)
            return None
        else:
            # fill_CSV_master.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_CSV_master.return_message_box.message_id,
                fill_CSV_master.return_message_box.message_text,
            )
            return msg

    def back(self):
        """
        CSVマスタメニューに遷移する
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
        self.code_textField.read_only = False
        self.del_flg_checkbox.disabled = True
        # 入力エリアを初期化する
        self.code_textField.value = Const.Const_Text.TEXT_BLANK
        self.HAB_at_text_textField.value = Const.Const_Text.TEXT_BLANK
        self.amount_text_textField.value = Const.Const_Text.TEXT_BLANK
        self.HABdetail_text_textField.value = Const.Const_Text.TEXT_BLANK
        self.character_code_textField.value = Const.Const_Text.TEXT_BLANK
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
        if self.CSV_master_list.selected_row_value is None:
            # 編集する行を選択するメッセージを表示する
            msg = My_Control.Msgbox("HAB008C", Message.Message_Box.HAB008C)
            self.page.open(msg)
        else:
            # 入力エリアを活性にする
            self.edit_area.disabled = False
            # 入力エリアのコントロールを入力制御する
            self.code_textField.read_only = True
            self.del_flg_checkbox.disabled = False
            # 入力エリアのコントロールに選択行のデータをセットする
            selected_row = int(self.CSV_master_list.selected_row_value)
            self.code_textField.value = self.fill_CSV_master_list[selected_row].code
            self.HAB_at_text_textField.value = self.fill_CSV_master_list[
                selected_row
            ].HAB_at_text
            self.amount_text_textField.value = self.fill_CSV_master_list[
                selected_row
            ].amount_text
            self.HABdetail_text_textField.value = self.fill_CSV_master_list[
                selected_row
            ].HABdetail_text
            self.character_code_textField.value = self.fill_CSV_master_list[
                selected_row
            ].character_code
            if (
                self.fill_CSV_master_list[selected_row].del_flg
                == Const.Const_Text.TEXT_BLANK
            ):
                self.del_flg_checkbox.value = False
            else:
                self.del_flg_checkbox.value = True
            self.update_version = self.fill_CSV_master_list[selected_row].update_version
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def CSV_master_entry_check(self):
        """
        削除処理か判定
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        if self.del_flg_checkbox.value:
            msg = My_Control.Msgbox("HAB005I", Message.Message_Box.HAB005I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.CSV_master_entry(msg)),
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
        if self.code_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("コード")
            )
        elif self.HAB_at_text_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("利用日時")
            )
        elif self.amount_text_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("金額")
            )
        elif self.HABdetail_text_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("家計簿詳細")
            )
        elif self.character_code_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("文字コード")
            )
        else:
            msg = My_Control.Msgbox("HAB004I", Message.Message_Box.HAB004I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.CSV_master_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
        return msg

    def CSV_master_entry(self, arg_msg):
        """
        CSVマスタを登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # CSVマスタに登録するデータを作成する
        CSV_master_row = CSV_Master()
        CSV_master_row.code = self.code_textField.value
        # 削除にチェックがある場合
        if self.del_flg_checkbox.value:
            CSV_master_row.update_user_id = self.page.data[0].user_id
            CSV_master_row.update_version = self.update_version
            return_CSV_master = self.CSV_master_adapter.delete_CSV_master(
                CSV_master_row
            )
        else:
            CSV_master_row.HAB_at_text = self.HAB_at_text_textField.value
            CSV_master_row.amount_text = self.amount_text_textField.value
            CSV_master_row.HABdetail_text = self.HABdetail_text_textField.value
            CSV_master_row.character_code = self.character_code_textField.value
            if self.isAddition:
                CSV_master_row.entry_user_id = self.page.data[0].user_id
                # CSVマスタアダプターを使用し、新規登録を行う
                # return_CSV_masterには登録成功かエラーのメッセージが代入されている
                return_CSV_master = self.CSV_master_adapter.create_CSV_master(
                    CSV_master_row, self.page.data[0].user_id
                )
            else:
                if self.del_flg_checkbox.value:
                    CSV_master_row.del_flg = Const.Del_flg.DELETE
                else:
                    CSV_master_row.del_flg = Const.Del_flg.NON_DELETE
                CSV_master_row.update_user_id = self.page.data[0].user_id
                CSV_master_row.update_version = self.update_version
                # CSVマスタアダプターを使用し、更新を行う
                # return_CSV_masterには登録成功かエラーのメッセージが代入されている
                return_CSV_master = self.CSV_master_adapter.update_CSV_master(
                    CSV_master_row
                )
        # return_CSV_master.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_CSV_master.return_message_box.message_id,
            return_CSV_master.return_message_box.message_text,
        )
        # メッセージ情報が登録完了の場合
        if return_CSV_master.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.entry_msg_yes(msg))
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def entry_msg_yes(self, arg_msg):
        """
        CSVマスター登録完了メッセージ用
        CSVマスタ一覧更新
        """
        self.page.close(arg_msg)
        # CSVマスタ一覧を更新する
        msg = self.CSV_master_list_data_set()
        # CSVマスタ一覧に表示するデータが取得できなかった場合
        if msg is not None:
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(msg)
        else:
            # CSVマスタ一覧コントロールを更新する
            self.controls[0].controls[1].content.controls[
                0
            ] = self.CSV_master_list.control
            # 入力エリアを非活性にする
            self.edit_area.disabled = True
            # 入力エリアのコントロールを入力制御する
            self.del_flg_checkbox.disabled = True
            # 入力エリアを初期化する
            self.code_textField.value = Const.Const_Text.TEXT_BLANK
            self.HAB_at_text_textField.value = Const.Const_Text.TEXT_BLANK
            self.amount_text_textField.value = Const.Const_Text.TEXT_BLANK
            self.HABdetail_text_textField.value = Const.Const_Text.TEXT_BLANK
            self.character_code_textField.value = Const.Const_Text.TEXT_BLANK
            self.del_flg_checkbox.value = False
            self.CSV_master_list.selected_row_value = None
        self.page.update()
