import flet as ft
from common.my_control import My_Control
from common.const import Const
from common.method import CommonMethod
from db.shop_master_adapter import Shop_Master_Adapter
from db.models import Shop_Master
from common.message import Message
from config.config import Config


# 店舗マスタ画面
class Shop_Master_Display(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        self.config = Config()
        self.fill_shop_master_list = None
        self.update_version = None
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # 店舗マスタアダプターをインスタンス化
        self.shop_master_adapter = Shop_Master_Adapter()
        # 店舗マスタ一覧作成
        self.shop_master_list = My_Control.HAB_LIST(self.page)
        self.shop_master_list.details_button_setting = False
        set_return = self.shop_master_list_data_set()
        # 店舗マスタ一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(set_return)
        else:
            # ヘッダ部エリア作成
            self.header = My_Control.Header_Area(Const.Display.SHOP_MASTER)
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
            # Noテキストボックス
            self.No_textField = ft.TextField(
                label=ft.Text("No", size=18, weight=ft.FontWeight.BOLD),
                border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
                bgcolor=ft.Colors.WHITE,
                width=100,
                max_length=20,
                text_size=18,
                read_only=True,
            )
            # 詳細種類コンボ
            self.HABkinds_dropdown = My_Control.HABkinds_Dropdown()
            # 店舗名テキストボックス
            self.name_textField = ft.TextField(
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
            # ボタンクリックで入力した家計簿を登録する
            self.entry_button = ft.FilledButton(
                content=ft.Text("登録", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.shop_master_entry_check(),
            )
            # 入力エリア作成
            self.edit_area = ft.Container(
                content=ft.Column(
                    controls=[
                        self.No_textField,
                        ft.Row(
                            controls=[
                                self.HABkinds_dropdown,
                                self.name_textField,
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
                                    self.shop_master_list.control,
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
        self.page.window.width = self.config.window_size.shop_master.width
        self.page.window.height = self.config.window_size.shop_master.height
        self.page.window.center()
        # "/shop_master"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/shop_master", controls)

    def shop_master_list_data_set(self):
        """
        店舗マスタ一覧のデータをセット
        """
        # 店舗マスタ一覧取得
        fill_shop_master = self.shop_master_adapter.fill_shop_master(
            self.page.data[0].user_id,
        )
        self.fill_shop_master_list = fill_shop_master.return_row
        column_name = []
        row_list = []
        if fill_shop_master.return_message_box.message_id is None:
            # 一覧の列名取得
            column_name = self.config.shop_master_column_name.column_name
            shop_master_row: Shop_Master
            # 取得した家計簿一覧をself.shop_master_listにデータをセットできるように加工
            for shop_master_row in fill_shop_master.return_row:
                row = [
                    shop_master_row.seq,
                    shop_master_row.seq,
                    shop_master_row.code_text,
                    shop_master_row.name,
                    shop_master_row.del_flg,
                ]
                row_list.append(row)
            # self.shop_master_listにデータをセットする
            self.shop_master_list.set_data_list(column_name, row_list, False)
            return None
        else:
            # fill_shop_master.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_shop_master.return_message_box.message_id,
                fill_shop_master.return_message_box.message_text,
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
        # 入力エリアを活性にする
        self.edit_area.disabled = False
        # 入力エリアを初期化する
        self.No_textField.value = len(self.fill_shop_master_list) + 1
        self.HABkinds_dropdown.value_clear()
        self.name_textField.value = Const.Const_Text.TEXT_BLANK
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
        # 行を選択していない場合
        if self.shop_master_list.selected_row_value is None:
            # 編集する行を選択するメッセージを表示する
            msg = My_Control.Msgbox("HAB008C", Message.Message_Box.HAB008C)
            self.page.open(msg)
        else:
            # 入力エリアを活性にする
            self.edit_area.disabled = False
            # 入力エリアのコントロールに選択行のデータをセットする
            selected_row = int(self.shop_master_list.selected_row_value)
            self.No_textField.value = self.fill_shop_master_list[selected_row][0]
            self.HABkinds_dropdown.value = self.fill_shop_master_list[selected_row][1]
            for option in self.HABkinds_dropdown.options:
                if option.key == self.HABkinds_dropdown.value:
                    self.HABkinds_dropdown.data = option.data
                    break
            self.name_textField.value = self.fill_shop_master_list[selected_row][2]
            if (
                self.fill_shop_master_list[selected_row][3]
                == Const.Const_Text.TEXT_BLANK
            ):
                self.del_flg_checkbox.value = False
            else:
                self.del_flg_checkbox.value = True
            self.update_version = self.fill_shop_master_list[selected_row][4]
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def shop_master_entry_check(self):
        """
        削除処理か判定
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        if self.del_flg_checkbox.value:
            msg = My_Control.Msgbox("HAB005I", Message.Message_Box.HAB005I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.shop_master_entry(msg)),
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
        if self.name_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("店舗名")
            )
        else:
            msg = My_Control.Msgbox("HAB004I", Message.Message_Box.HAB004I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.shop_master_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
        return msg

    def shop_master_entry(self, arg_msg):
        """
        店舗マスタを登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 店舗マスタに登録するデータを作成する
        shop_master_row = Shop_Master()
        shop_master_row.seq = int(self.No_textField.value)
        # 削除にチェックがある場合
        if self.del_flg_checkbox.value:
            shop_master_row.update_user_id = self.page.data[0].user_id
            shop_master_row.update_version = self.update_version
            return_shop_master = self.shop_master_adapter.delete_shop_master(
                shop_master_row
            )
        else:
            shop_master_row.code = self.HABkinds_dropdown.data
            shop_master_row.name = self.name_textField.value
            if int(self.No_textField.value) > len(self.fill_shop_master_list):
                shop_master_row.entry_user_id = self.page.data[0].user_id
                # 店舗マスタアダプターを使用し、新規登録を行う
                # return_shop_masterには登録成功かエラーのメッセージが代入されている
                return_shop_master = self.shop_master_adapter.create_shop_master(
                    shop_master_row, self.page.data[0].user_id
                )
            else:
                if self.del_flg_checkbox.value:
                    shop_master_row.del_flg = Const.Del_flg.DELETE
                else:
                    shop_master_row.del_flg = Const.Del_flg.NON_DELETE
                shop_master_row.update_user_id = self.page.data[0].user_id
                shop_master_row.update_version = self.update_version
                # 店舗マスタアダプターを使用し、更新を行う
                # return_shop_masterには登録成功かエラーのメッセージが代入されている
                return_shop_master = self.shop_master_adapter.update_shop_master(
                    shop_master_row
                )
        # return_shop_master.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_shop_master.return_message_box.message_id,
            return_shop_master.return_message_box.message_text,
        )
        # メッセージ情報が登録完了の場合
        if return_shop_master.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.entry_msg_yes(msg))
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def entry_msg_yes(self, arg_msg):
        """
        店舗マスター登録完了メッセージ用
        店舗マスタ一覧更新
        """
        self.page.close(arg_msg)
        # 店舗マスタ一覧を更新する
        msg = self.shop_master_list_data_set()
        # 店舗マスタ一覧に表示するデータが取得できなかった場合
        if msg is not None:
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(msg)
        else:
            # 店舗マスタ一覧コントロールを更新する
            self.controls[0].controls[1].content.controls[
                0
            ] = self.shop_master_list.control
            # 入力エリアを非活性にする
            self.edit_area.disabled = True
            # 入力値を初期化する
            self.No_textField.value = None
            self.HABkinds_dropdown.value_clear()
            self.name_textField.value = None
            self.del_flg_checkbox.value = False
            self.shop_master_list.selected_row_value = None
        self.page.update()
