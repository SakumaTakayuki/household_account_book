import flet as ft
from db.HAB_detail_adapter import HAB_Detail_Adapter
from common.my_control import My_Control
from common.message import Message
from common.const import Const
from common.method import CommonMethod
from db.models import HAB_Detail
from config.config import Config
import datetime


# 家計簿詳細画面
class HAB_detail(My_Control.MyView):
    def __init__(self, arg_page: ft.Page, arg_SEQ):
        self.page = arg_page
        self.config = Config()
        self.seq = arg_SEQ
        self.update_version = None
        self.is_update = False
        # 家計簿詳細アダプターをインスタンス化
        self.HAB_detail_adapter = HAB_Detail_Adapter()
        # ヘッダ部エリア作成
        self.header = My_Control.Header_Area(Const.Display.HAB_DETAIL)
        self.header.back_button.on_click = lambda e: self.back()
        # 利用日時入力ドロップダウン作成
        self.datetime_dropdown = My_Control.Datetime_Dropdown(self.page)
        self.datetime_dropdown.search.visible = False
        # 入出金区分コンボ
        self.HAB_kbn_dropdown = My_Control.HAB_Kbn_Dropdown()
        # 金額テキストボックス
        # 数字入力時に整数値に変換する
        self.amount_textField = ft.TextField(
            label=ft.Text("金額", size=18, weight=ft.FontWeight.BOLD),
            border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            width=130,
            max_length=10,
            text_size=18,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        # 詳細種類コンボ
        self.HABkinds_dropdown = My_Control.HABkinds_Dropdown()
        # 家計簿詳細テキストボックス
        self.HABdetail_textField = ft.TextField(
            label=ft.Text("詳細", size=18, weight=ft.FontWeight.BOLD),
            border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            multiline=True,
            min_lines=5,
            max_lines=5,
            max_length=1000,
            text_size=18,
        )
        # 登録ボタン作成
        # ボタンクリックで入力した家計簿を登録する
        self.entry_button = ft.FilledButton(
            content=ft.Text("登録", size=18),
            width=100,
            height=40,
            on_click=lambda e: self.value_check(),
        )
        # 削除ボタン作成
        # ボタンクリックで家計簿省略を削除する
        self.delete_button = ft.FilledButton(
            content=ft.Text("削除", size=18),
            width=100,
            height=40,
            on_click=lambda e: self.HAB_delete(),
        )
        # フッター部エリア作成
        self.footer = ft.Row(
            controls=[self.entry_button, self.delete_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # 家計簿詳細画面にデータをセットする
        set_return = self.HAB_detail_data_set(self.seq)
        # 家計簿詳細画面に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [self.overlay]
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
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
                                            self.datetime_dropdown.control,
                                            self.HAB_kbn_dropdown,
                                            self.amount_textField,
                                            self.HABkinds_dropdown,
                                        ]
                                    ),
                                    self.HABdetail_textField,
                                    self.footer,
                                ],
                                spacing=15,
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
        self.page.window.width = self.config.window_size.HAB_detail.width
        self.page.window.height = self.config.window_size.HAB_detail.height
        CommonMethod.center_non_update(self.page)
        # "/HAB_list"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/HAB_detail", controls)

    def HAB_detail_data_set(self, arg_seq):
        """
        家計簿詳細のデータをセット
        """
        # 家計簿詳細取得
        fill_HAB_detail = self.HAB_detail_adapter.fill_HAB_detail(
            arg_seq,
            self.page.data[0].user_id,
        )
        # エラーがない場合
        if fill_HAB_detail.return_message_box.message_id is None:
            # 各コントロールに取得したデータをセットする
            self.datetime_dropdown.year.value = fill_HAB_detail.return_row[0][
                1
            ].strftime("%Y")
            self.datetime_dropdown.month.value = fill_HAB_detail.return_row[0][
                1
            ].strftime("%m")
            self.datetime_dropdown.day.value = fill_HAB_detail.return_row[0][
                1
            ].strftime("%d")
            self.datetime_dropdown.hour.value = fill_HAB_detail.return_row[0][
                1
            ].strftime("%H")
            self.datetime_dropdown.minute.value = fill_HAB_detail.return_row[0][
                1
            ].strftime("%M")
            self.datetime_dropdown.year.data = fill_HAB_detail.return_row[0][
                1
            ].strftime("%Y")
            self.datetime_dropdown.month.data = fill_HAB_detail.return_row[0][
                1
            ].strftime("%m")
            self.datetime_dropdown.day.data = fill_HAB_detail.return_row[0][1].strftime(
                "%d"
            )
            self.datetime_dropdown.hour.data = fill_HAB_detail.return_row[0][
                1
            ].strftime("%H")
            self.datetime_dropdown.minute.data = fill_HAB_detail.return_row[0][
                1
            ].strftime("%M")
            self.HAB_kbn_dropdown.data = fill_HAB_detail.return_row[0][2]
            self.HAB_kbn_dropdown.value = fill_HAB_detail.return_row[0][3]
            self.amount_textField.value = fill_HAB_detail.return_row[0][4]
            self.HABkinds_dropdown.data = fill_HAB_detail.return_row[0][5]
            self.HABkinds_dropdown.value = fill_HAB_detail.return_row[0][6]
            self.HABdetail_textField.value = fill_HAB_detail.return_row[0][7]
            self.update_version = fill_HAB_detail.return_row[0][8]
            return None
        else:
            # fill_HAB_list.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_HAB_detail.return_message_box.message_id,
                fill_HAB_detail.return_message_box.message_text,
            )
            # メッセージボックスのアクションを家計簿一覧に戻るよう設定
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.back()),
            ]
            # 家計簿一覧で最新情報が再取得されるように設定
            self.is_update = True
            return msg

    def back(self):
        """
        家計簿一覧に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        self.page.views.pop()
        self.page.window.width = self.config.window_size.HAB_list.width
        self.page.window.height = self.config.window_size.HAB_list.height
        CommonMethod.center_non_update(self.page)
        # 画面表示後、登録をした場合
        if self.is_update:
            # 家計簿一覧画面で最新情報を取得するよう設定する
            HAB_year_month = {
                "year": self.datetime_dropdown.year.data,
                "month": self.datetime_dropdown.month.data,
            }
            n = len(self.page.views) - 1
            self.page.views[n].data = HAB_year_month
            # 画面を活性にする
            self.overlay.visible = False
            self.page.go("/HAB_list")
        else:
            # 画面を活性にする
            self.overlay.visible = False
            self.page.go("/back")

    def value_check(self):
        """
        入力値チェック
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 入力値チェック
        if self.amount_textField.value == "":
            msg = My_Control.Msgbox(
                "HAB005C", Message.Message_Box.HAB005C.format("金額")
            )
        else:
            msg = My_Control.Msgbox("HAB004I", Message.Message_Box.HAB004I)
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.HAB_entry(msg)),
                ft.TextButton("いいえ", on_click=lambda e: self.page.close(msg)),
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def HAB_entry(self, arg_msg):
        """
        家計簿詳細を登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 家計簿詳細テーブルに登録するデータを作成する
        HAB_ditail_row = HAB_Detail()
        HAB_ditail_row.HAB_seq = self.seq
        HAB_ditail_row.HAB_at = datetime.datetime(
            int(self.datetime_dropdown.year.data),
            int(self.datetime_dropdown.month.data),
            int(self.datetime_dropdown.day.data),
            int(self.datetime_dropdown.hour.data),
            int(self.datetime_dropdown.minute.data),
        )
        HAB_ditail_row.HAB_kbn = self.HAB_kbn_dropdown.data
        HAB_ditail_row.amount = self.amount_textField.value
        HAB_ditail_row.HABkinds = self.HABkinds_dropdown.data
        HAB_ditail_row.HABdetail = self.HABdetail_textField.value
        HAB_ditail_row.update_user_id = self.page.data[0].user_id
        HAB_ditail_row.update_version = self.update_version
        # 家計簿詳細アダプターを使用し、更新を行う
        # return_HAB_ditailには登録成功かエラーのメッセージが代入されている
        return_HAB_ditail = self.HAB_detail_adapter.update_HAB_detail(HAB_ditail_row)
        # return_HAB_ditail.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_HAB_ditail.return_message_box.message_id,
            return_HAB_ditail.return_message_box.message_text,
        )
        # メッセージ情報が登録完了の場合
        if return_HAB_ditail.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            msg.actions = [
                ft.TextButton("はい", on_click=lambda e: self.entry_msg_yes(msg))
            ]
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def entry_msg_yes(self, arg_msg):
        """
        家計簿登録完了メッセージ用
        家計簿詳細更新
        """
        self.page.close(arg_msg)
        # 更新フラグを立てる
        self.is_update = True
        # 家計簿画面を更新する
        msg = self.HAB_detail_data_set(self.seq)
        # 家計簿画面に表示するデータが取得できなかった場合
        if msg is not None:
            # 自作コントロールのメッセージボックスを画面上に表示する
            self.page.open(msg)
        self.page.update()

    def HAB_delete(self):
        """
        家計簿詳細を削除する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        delete_info_msg = My_Control.Msgbox("HAB005I", Message.Message_Box.HAB005I)
        delete_info_msg.actions = [
            ft.TextButton("はい", on_click=lambda e: self.delete_info_msg_yes()),
            ft.TextButton(
                "いいえ",
                on_click=lambda e: self.delete_info_msg_no(delete_info_msg),
            ),
        ]
        self.page.open(delete_info_msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()

    def delete_info_msg_yes(self):
        """
        論理削除で登録する
        """
        # 家計簿詳細の論理削除するデータを作成する
        HAB_ditail_row = HAB_Detail()
        HAB_ditail_row.HAB_seq = self.seq
        HAB_ditail_row.update_user_id = self.page.data[0].user_id
        HAB_ditail_row.update_version = self.update_version
        # 家計簿詳細アダプターを使用し、論理削除を行う
        # return_HAB_ditailには論理削除成功かエラーのメッセージが代入されている
        return_HAB_ditail = self.HAB_detail_adapter.delete_HAB_detail(HAB_ditail_row)
        # return_HAB_ditail.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        delete_complete_msg = My_Control.Msgbox(
            return_HAB_ditail.return_message_box.message_id,
            return_HAB_ditail.return_message_box.message_text,
        )
        delete_complete_msg.actions = [
            ft.TextButton(
                "はい",
                on_click=lambda e: self.delete_complete_msg(
                    return_HAB_ditail.return_message_box.message_id,
                ),
            ),
        ]
        # メッセージ情報が論理削除成功の場合
        if return_HAB_ditail.return_message_box.message_id[-1] == Const.Log_Kinds.INFO:
            # 更新フラグを立てる
            self.is_update = True
        self.page.open(delete_complete_msg)
        self.page.update()

    def delete_complete_msg(self, arg_message_id):
        """
        削除完了後、家計簿一覧を表示する
        """
        if arg_message_id[-1] == Const.Log_Kinds.WARNING:
            self.page.window.close()
        else:
            self.back()

    def delete_info_msg_no(self, arg_msg):
        """
        削除を中断する
        """
        # メッセージボックスを閉じる
        self.page.close(arg_msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()
