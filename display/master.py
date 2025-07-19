import flet as ft
from common.my_control import My_Control
from common.const import Const
from common.method import CommonMethod
from db.master_adapter import Master_Adapter
from db.models import Master
from common.message import Message
from config import Config


# マスタ画面
class Master_Display(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        self.fill_master_list = None
        self.isAddition = False
        self.update_version = None
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # マスタアダプターをインスタンス化
        self.master_adapter = Master_Adapter()
        # マスタ一覧作成
        self.master_list = My_Control.HAB_LIST(self.page)
        self.master_list.details_button_setting = False
        set_return = self.master_list_data_set()
        # マスタ一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(set_return)
        else:
            # ヘッダ部エリア作成
            self.header = My_Control.Header_Area(Const.Display.MASTER)
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
            # IDドロップダウン
            self.m_id_dropdown = My_Control.MyDropdown(
                label=ft.Text(value="ID", size=18, weight=ft.FontWeight.BOLD),
                width=250,
            )
            id_list = []
            for id in self.master_list.data_list:
                id_list.append(id[0])
            id_list = list(dict.fromkeys(id_list))
            m_id_options = []
            for id in id_list:
                m_id_options.append(
                    ft.DropdownOption(
                        key=id,
                        content=ft.Text(id, size=18),
                        data=id,
                    )
                )
            self.m_id_dropdown.options = m_id_options
            self.m_id_dropdown.value = id_list[0]
            self.m_id_dropdown.data = id_list[0]
            self.m_id_dropdown.on_change = lambda e: self.m_id_dropdown.change_dropdown(
                e
            )
            # コードテキストボックス
            self.m_code_textField = ft.TextField(
                label=ft.Text("コード", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=250,
                max_length=20,
                text_size=18,
            )
            # 名称テキストボックス
            self.m_text_textField = ft.TextField(
                label=ft.Text("店舗名", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=350,
                max_length=20,
                text_size=18,
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
            # ボタンクリックで入力したマスタを登録する
            self.entry_button = ft.FilledButton(
                content=ft.Text("登録", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.master_entry_check(),
            )
            # 入力エリア作成
            self.edit_area = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                self.m_id_dropdown,
                                self.m_code_textField,
                            ]
                        ),
                        ft.Row(
                            controls=[
                                self.m_text_textField,
                                self.del_flg_checkbox,
                            ]
                        ),
                        self.entry_button,
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
                                    self.master_list.control,
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
        self.page.window.width = Config.window_size.master.width
        self.page.window.height = Config.window_size.master.height
        CommonMethod.center_non_update(self.page)
        # "/master"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/master", controls)

    def master_list_data_set(self):
        """
        マスタ一覧のデータをセット
        """
        # マスタ一覧取得
        fill_master = self.master_adapter.fill_master(self.page.data[0].user_id)
        self.fill_master_list = fill_master.return_row
        column_name = []
        row_list = []
        if fill_master.return_message_box.message_id is None:
            # 一覧の列名取得
            column_name = Config.master_column_name.column_name
            master_row: Master
            # 取得したマスタ一覧をself.master_listにデータをセットできるように加工
            for master_row in fill_master.return_row:
                row = [
                    [master_row.m_id, master_row.m_code],
                    master_row.m_id,
                    master_row.m_code,
                    master_row.m_text,
                    master_row.del_flg,
                ]
                row_list.append(row)
            # self.master_listにデータをセットする
            self.master_list.set_data_list(column_name, row_list)
            return None
        else:
            # fill_master.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_master.return_message_box.message_id,
                fill_master.return_message_box.message_text,
            )
            return msg

    def back(self):
        """
        マスタメニューに遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        self.page.views.pop()
        self.page.window.width = Config.window_size.master_menu.width
        self.page.window.height = Config.window_size.master_menu.height
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
        self.m_id_dropdown.disabled = False
        self.m_code_textField.disabled = False
        self.del_flg_checkbox.disabled = True
        # 入力エリアを初期化する
        self.m_id_dropdown.value_clear()
        self.m_code_textField.value = Const.Const_Text.TEXT_BLANK
        self.m_text_textField.value = Const.Const_Text.TEXT_BLANK
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
        if self.master_list.selected_row_value is None:
            # 編集する行を選択するメッセージを表示する
            msg = My_Control.Msgbox("HAB008C", Message.Message_Box.HAB008C)
            self.page.open(msg)
        else:
            # 入力エリアを活性にする
            self.edit_area.disabled = False
            # 入力エリアのコントロールを入力制御する
            self.m_id_dropdown.disabled = True
            self.m_code_textField.disabled = True
            self.del_flg_checkbox.disabled = False
            # 入力エリアのコントロールに選択行のデータをセットする
            selected_row = int(self.master_list.selected_row_value)
            self.m_id_dropdown.value = self.fill_master_list[selected_row].m_id
            self.m_id_dropdown.data = self.fill_master_list[selected_row].m_id
            self.m_code_textField.value = self.fill_master_list[selected_row].m_code
            self.m_text_textField.value = self.fill_master_list[selected_row].m_text
            if (
                self.fill_master_list[selected_row].del_flg
                == Const.Const_Text.TEXT_BLANK
            ):
                self.del_flg_checkbox.value = False
            else:
                self.del_flg_checkbox.value = True
            self.update_version = self.fill_master_list[selected_row].update_version
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def master_entry_check(self):
        """
        削除処理か判定
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        if self.del_flg_checkbox.value:
            msg = My_Control.Msgbox("HAB005I", Message.Message_Box.HAB005I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.master_entry(msg)),
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
        if self.m_code_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("コード")
            )
        elif self.m_text_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("名称")
            )
        else:
            msg = My_Control.Msgbox("HAB004I", Message.Message_Box.HAB004I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.master_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
        return msg

    def master_entry(self, arg_msg):
        """
        マスタを登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # マスタに登録するデータを作成する
        master_row = Master()
        master_row.m_id = self.m_id_dropdown.data
        master_row.m_code = self.m_code_textField.value
        # 削除にチェックがある場合
        if self.del_flg_checkbox.value:
            master_row.update_user_id = self.page.data[0].user_id
            master_row.update_version = self.update_version
            return_master = self.master_adapter.delete_master(master_row)
        else:
            master_row.m_text = self.m_text_textField.value
            if self.isAddition:
                master_row.entry_user_id = self.page.data[0].user_id
                # マスタアダプターを使用し、新規登録を行う
                # return_masterには登録成功かエラーのメッセージが代入されている
                return_master = self.master_adapter.create_master(
                    master_row, self.page.data[0].user_id
                )
            else:
                if self.del_flg_checkbox.value:
                    master_row.del_flg = Const.Del_flg.DELETE
                else:
                    master_row.del_flg = Const.Del_flg.NON_DELETE
                master_row.update_user_id = self.page.data[0].user_id
                master_row.update_version = self.update_version
                # マスタアダプターを使用し、更新を行う
                # return_masterには登録成功かエラーのメッセージが代入されている
                return_master = self.master_adapter.update_master(master_row)
        # return_master.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_master.return_message_box.message_id,
            return_master.return_message_box.message_text,
        )
        # メッセージ情報が登録完了の場合
        if return_master.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.entry_msg_yes(msg))
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def entry_msg_yes(self, arg_msg):
        """
        マスター登録完了メッセージ用
        マスタ一覧更新
        """
        self.page.close(arg_msg)
        # マスタ一覧を更新する
        msg = self.master_list_data_set()
        # マスタ一覧に表示するデータが取得できなかった場合
        if msg is not None:
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(msg)
        else:
            # マスタ一覧コントロールを更新する
            self.controls[0].controls[1].content.controls[0] = self.master_list.control
            # 入力エリアを非活性にする
            self.edit_area.disabled = True
            # 入力エリアのコントロールを入力制御する
            self.m_id_dropdown.disabled = False
            self.m_code_textField.disabled = False
            self.del_flg_checkbox.disabled = True
            # 入力エリアを初期化する
            self.m_id_dropdown.value_clear()
            self.m_code_textField.value = Const.Const_Text.TEXT_BLANK
            self.m_text_textField.value = Const.Const_Text.TEXT_BLANK
            self.del_flg_checkbox.value = False
            self.master_list.selected_row_value = None
        self.page.update()
