import flet as ft
from db.bulk_registration_adapter import Bulk_Registration_Adapter
from db.models import HAB_Detail, CSV_Master
from common.my_control import My_Control
from common.message import Message
from common.const import Const
from common.method import CommonMethod
from config.config import Config
import datetime
import mojimoji
import copy


# 一括登録画面
class Bulk_Registration(My_Control.MyView):
    def __init__(self, arg_page: ft.Page):
        self.page = arg_page
        self.config = Config()
        self.is_update = False
        self.keep_HAB_detail_list = None
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # 一括登録アダプターをインスタンス化
        self.bulk_registration_adapter = Bulk_Registration_Adapter()
        # ヘッダ部エリア作成
        self.header = My_Control.Header_Area(Const.Display.BULK_REGISTRATION)
        self.header.back_button.on_click = lambda e: self.back()
        # CSV提供会社コンボ作成
        self.CSV_company_dropdown = My_Control.CSV_Company_Dropdown()
        # ファイル名テキストボックス作成
        self.file_name = ft.TextField(
            label=ft.Text("ファイル名", size=18, weight=ft.FontWeight.BOLD),
            border=ft.border.all(width=1.0, color=ft.Colors.BLACK),
            bgcolor=ft.Colors.WHITE,
            width=400,
            max_length=20,
            text_size=18,
            read_only=True,
        )
        # ファイル選択機能作成
        self.pick_files_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.select_file_button = ft.FilledButton(
            content=ft.Text("ファイル選択", size=18),
            width=125,
            height=40,
            on_click=lambda e: self.pick_files_dialog.pick_files(
                allowed_extensions=["csv"]
            ),
        )
        self.page.overlay.append(self.pick_files_dialog)
        # CSV選択エリア作成
        self.CSV_select_area = ft.Row(
            controls=[
                self.CSV_company_dropdown,
                self.file_name,
                self.select_file_button,
            ]
        )
        # 取込結果一覧作成
        self.import_results_list = My_Control.HAB_LIST(self.page)
        self.import_results_list.details_button_setting = False
        self.import_results_list.page_go_setting = "HAB_detail"
        set_return = self.import_results_list_data_set(None)
        # 取込結果一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            # 登録ボタン作成
            # ボタンクリックで入力した家計簿を登録する
            self.entry_button = ft.FilledButton(
                content=ft.Text("登録", size=18),
                width=100,
                height=40,
                on_click=lambda e: self.HAB_detail_list_check(),
            )
            # controlsに作成したコントロールを追加する
            controls = [
                ft.Column(
                    controls=[
                        self.header.control,
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    self.CSV_select_area,
                                    self.import_results_list.control,
                                    self.entry_button,
                                ],
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
        self.page.window.width = self.config.window_size.bulk_registration.width
        self.page.window.height = self.config.window_size.bulk_registration.height
        CommonMethod.center_non_update(self.page)
        # "/bulk_registration"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/bulk_registration", controls)

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        """
        ファイル選択結果の処理
        """
        if e.files is None:
            return
        else:
            # 画面を非活性にする
            self.overlay.visible = True
            self.page.update()
            set_return = self.import_results_list_data_set(e.files[0].path)
            # 取込結果一覧に表示するデータが取得できなかった場合
            if set_return is not None:
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(set_return)
            else:
                # ファイル名テキストボックスに選択したファイル名をセットする
                self.file_name.value = e.files[0].name
                # 表示しているself.import_results_list_data_setを入れ替える
                self.controls[0].controls[1].content.controls[
                    1
                ] = self.import_results_list.control
            # 画面を活性にする
            self.overlay.visible = False
            # コントロールを更新する
            self.page.update()

    def import_results_list_data_set(self, arg_file_path):
        """
        取込結果一覧のデータをセット
        """
        # 一覧の列名取得
        column_name_list = self.config.HAB_list_column_name.column_name
        if arg_file_path is not None:
            HAB_detail_list = []
            row_list = []
            HAB_at_column = 0
            amount_column = 0
            HABdetail_column = 0
            f = None
            fill_shop_master_list = self.bulk_registration_adapter.fill_shop_master(
                self.page.data[0].user_id
            )
            if fill_shop_master_list.return_message_box.message_id is not None:
                # fill_shop_master_list.return_message_boxに代入されたメッセージ情報を
                # 自作コントロールのメッセージボックスに渡しインスタンス化
                msg = My_Control.Msgbox(
                    fill_shop_master_list.return_message_box.message_id,
                    fill_shop_master_list.return_message_box.message_text,
                )
                return msg
            else:
                fill_HABkinds_list = self.bulk_registration_adapter.fill_HABkinds(
                    self.page.data[0].user_id
                )
                if fill_HABkinds_list.return_message_box.message_id is not None:
                    # fill_HABkinds_list.return_message_boxに代入されたメッセージ情報を
                    # 自作コントロールのメッセージボックスに渡しインスタンス化
                    msg = My_Control.Msgbox(
                        fill_HABkinds_list.return_message_box.message_id,
                        fill_HABkinds_list.return_message_box.message_text,
                    )
                    return msg
                else:
                    fill_CSV_master = self.bulk_registration_adapter.fill_CSV_master(
                        self.CSV_company_dropdown.data, self.page.data[0].user_id
                    )
                    if fill_CSV_master.return_message_box.message_id is not None:
                        # fill_HABkinds_list.return_message_boxに代入されたメッセージ情報を
                        # 自作コントロールのメッセージボックスに渡しインスタンス化
                        msg = My_Control.Msgbox(
                            fill_HABkinds_list.return_message_box.message_id,
                            fill_HABkinds_list.return_message_box.message_text,
                        )
                        return msg
                    else:
                        fill_CSV_master_row: CSV_Master
                        fill_CSV_master_row = fill_CSV_master.return_row[0]
                        try:
                            f = open(
                                arg_file_path,
                                "r",
                                encoding=fill_CSV_master_row.character_code,
                            )
                            column_line = f.readline()
                            column_line = column_line.replace(
                                Const.Const_Text.DOUBLE_QUOTATION,
                                Const.Const_Text.TEXT_BLANK,
                            )
                            column_name = column_line.split(Const.Const_Text.COMMA)
                            # 列名フォーマットチェック
                            try:
                                HAB_at_column = column_name.index(
                                    fill_CSV_master_row.HAB_at_text
                                )
                                amount_column = column_name.index(
                                    fill_CSV_master_row.amount_text
                                )
                                HABdetail_column = column_name.index(
                                    fill_CSV_master_row.HABdetail_text
                                )
                            except Exception as e:
                                msg = My_Control.Msgbox(
                                    "HAB006C",
                                    Message.Message_Box.HAB006C.format("列名"),
                                )
                                return msg
                            lines = f.readlines()
                            for line in lines:
                                line = line.replace(
                                    Const.Const_Text.DOUBLE_QUOTATION,
                                    Const.Const_Text.TEXT_BLANK,
                                )
                                line_data = line.split(Const.Const_Text.COMMA)
                                HAB_detail_row = HAB_Detail()
                                HAB_at_splited = None
                                # データフォーマットチェック
                                try:
                                    datetime.datetime.strptime(
                                        mojimoji.zen_to_han(line_data[HAB_at_column]),
                                        "%Y/%m/%d",
                                    )
                                    HAB_at_splited = line_data[HAB_at_column].split("/")
                                except ValueError as e:
                                    msg = My_Control.Msgbox(
                                        "HAB006C",
                                        Message.Message_Box.HAB006C.format("日付"),
                                    )
                                    return msg
                                if not line_data[amount_column].isdigit():
                                    msg = My_Control.Msgbox(
                                        "HAB006C",
                                        Message.Message_Box.HAB006C.format("金額"),
                                    )
                                    return msg
                                else:
                                    # 値セット
                                    HAB_detail_row.HAB_at = datetime.datetime(
                                        int(HAB_at_splited[0]),
                                        int(HAB_at_splited[1]),
                                        int(HAB_at_splited[2]),
                                    )
                                    HAB_detail_row.HAB_kbn = Const.HAB_kbn_code.kbn_out
                                    HAB_detail_row.amount = mojimoji.zen_to_han(
                                        line_data[amount_column]
                                    )
                                    filtered_shop_master_row = [
                                        shop_master_row
                                        for shop_master_row in fill_shop_master_list.return_row
                                        if shop_master_row.name
                                        in mojimoji.han_to_zen(
                                            line_data[HABdetail_column]
                                        )
                                    ]
                                    if len(filtered_shop_master_row) > 0:
                                        HAB_detail_row.HABkinds = (
                                            filtered_shop_master_row[0].code
                                        )
                                    else:
                                        HAB_detail_row.HABkinds = "06"
                                    HAB_detail_row.HABdetail = line_data[
                                        HABdetail_column
                                    ]
                                    HAB_detail_row.entry_user_id = Const.Admin.USER_ID
                                    HAB_detail_list.append(HAB_detail_row)
                            HAB_row: HAB_Detail
                            # CSVデータをself.HAB_listにデータをセットできるように加工
                            HAB_detail_list_copy = copy.deepcopy(HAB_detail_list)
                            for HAB_row in HAB_detail_list_copy:
                                filtered_HABkinds_row = [
                                    HABkinds_row
                                    for HABkinds_row in fill_HABkinds_list.return_row
                                    if HABkinds_row.m_code == HAB_row.HABkinds
                                ]
                                HAB_row.HABkinds = filtered_HABkinds_row[0].m_text
                                row = [
                                    HAB_row.HAB_seq,
                                    HAB_row.HAB_at.strftime("%Y-%m-%d %H:%M"),
                                    Const.HAB_kbn.kbn_out,
                                    HAB_row.amount,
                                    HAB_row.HABkinds,
                                    HAB_row.HABdetail,
                                ]
                                row_list.append(row)
                        except Exception as e:
                            msg = My_Control.Msgbox(
                                "HAB006C",
                                Message.Message_Box.HAB006C.format(
                                    "取り込んだファイル"
                                ),
                            )
                            return msg
                        finally:
                            # ファイルが開かれている場合
                            if f is not None:
                                # ファイルを閉じる
                                f.close()
                        # 取得した取込結果一覧をself.import_results_listにデータをセットできるように加工
                        self.import_results_list.set_data_list(
                            column_name_list, row_list, False
                        )
                        self.keep_HAB_detail_list = HAB_detail_list
                        return None
        else:
            self.import_results_list.set_data_list(column_name_list, None, False)
            return None

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
        if self.is_update:
            HAB_year_month = {
                "year": self.keep_HAB_detail_list[
                    len(self.keep_HAB_detail_list) - 1
                ].HAB_at.year,
                "month": f"{self.keep_HAB_detail_list[
                    len(self.keep_HAB_detail_list) - 1
                ].HAB_at.month:02}",
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

    def HAB_detail_list_check(self):
        """
        取込データ確認
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        if self.file_name.value == "":
            msg = My_Control.Msgbox("HAB007C", Message.Message_Box.HAB007C)
        elif len(self.keep_HAB_detail_list) == 0:
            msg = My_Control.Msgbox("HAB009C", Message.Message_Box.HAB009C)
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
        家計簿を登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 一括登録アダプターを使用し、新規登録を行う
        # return_bulk_registrationには登録成功かエラーのメッセージが代入されている
        return_bulk_registration = (
            self.bulk_registration_adapter.bulk_registration_HAB_list(
                self.keep_HAB_detail_list,
                self.file_name.value,
                self.page.data[0].user_id,
            )
        )
        # return_bulk_registration.return_message_boxに代入されたメッセージ情報を
        # 自作コントロールのメッセージボックスに渡しインスタンス化
        msg = My_Control.Msgbox(
            return_bulk_registration.return_message_box.message_id,
            return_bulk_registration.return_message_box.message_text,
        )
        # メッセージ情報が論理削除成功の場合
        if (
            return_bulk_registration.return_message_box.message_id[-1]
            == Const.Log_Kinds.INFO
        ):
            # 更新フラグを立てる
            self.is_update = True
        self.page.open(msg)
        # 画面を活性にする
        self.overlay.visible = False
        self.page.update()
