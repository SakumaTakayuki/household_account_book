import flet as ft
from db.HAB_list_adapter import HAB_List_Adapter
from db.common.engine import Return_Info
from db.models import HAB_Detail
from common.my_control import My_Control
from common.message import Message
from common.const import Const
from common.method import CommonMethod
import datetime
from config.config import Config


# 家計簿一覧画面
class HAB_List(My_Control.MyView):
    def __init__(self, arg_page: ft.Page, arg_HAB_year_month):
        self.page = arg_page
        self.config = Config()
        # オーバーレイ作成
        self.overlay = My_Control.MyOverlay(self.page).overlay
        # 家計簿アダプターをインスタンス化
        self.HAB_list_adapter = HAB_List_Adapter()
        # 今日の日付を取得
        today = datetime.datetime.now()
        if arg_HAB_year_month is None:
            year = today.strftime("%Y")
            month = today.strftime("%m")
        else:
            year = arg_HAB_year_month["year"]
            month = arg_HAB_year_month["month"]
        # 家計簿一覧作成
        self.HAB_list = My_Control.HAB_LIST(self.page)
        self.HAB_list.page_go_setting = "HAB_detail"
        set_return = self.HAB_list_data_set(year, month)
        # 家計簿一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            controls = [set_return]
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            HAB_kbn_return = self.fill_HAB_kbn_PieChart_data(year, month)
            if HAB_kbn_return is not None:
                controls = [HAB_kbn_return]
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(HAB_kbn_return)
            else:
                HABkinds_return = self.fill_HABkinds_PieChart_data(year, month)
                if HABkinds_return is not None:
                    controls = [HABkinds_return]
                    # 自作コントロールのメッセージボックスをログイン画面上に表示する
                    self.page.open(HABkinds_return)
                else:
                    # 家計簿一覧の年月を代入
                    self.HAB_list_year = year
                    self.HAB_list_month = month
                    # 画面ラベル作成
                    self.display_label = ft.Container(
                        content=ft.Text(
                            Const.Display.HAB_LIST,
                            size=30,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.alignment.center,
                    )
                    # マスタメニューボタン作成
                    # ボタンクリックでマスタ管理画面に遷移する
                    self.master_menu_button = ft.FilledButton(
                        content=ft.Text("マスタメニュー", size=18),
                        width=125,
                        height=40,
                        on_click=lambda e: self.go_master_menu_page(),
                    )
                    # ヘッダ部エリア作成
                    self.header = ft.Row(
                        controls=[
                            ft.Container(width=100),
                            self.display_label,
                            self.master_menu_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
                    # 前月ボタン作成
                    # ボタンクリックで前月の家計簿一覧を表示する
                    self.last_month_button = ft.FilledButton(
                        content=ft.Text("前月", size=18),
                        width=100,
                        height=40,
                        on_click=lambda e: self.last_month_data_set(),
                    )
                    # 当月ボタン作成
                    # ボタンクリックで当月の家計簿一覧を表示する
                    self.this_month_button = ft.FilledButton(
                        content=ft.Text("当月", size=18),
                        width=100,
                        height=40,
                        on_click=lambda e: self.this_month_data_set(),
                    )
                    # 次月ボタン作成
                    # ボタンクリックで次月の家計簿一覧を表示する
                    self.next_month_button = ft.FilledButton(
                        content=ft.Text("次月", size=18),
                        width=100,
                        height=40,
                        on_click=lambda e: self.next_month_data_set(),
                    )
                    # 年月選択表示機能作成
                    # ボタンクリックで選択した年月の家計簿一覧を表示する
                    self.year_month_dropdown = My_Control.Datetime_Dropdown(self.page)
                    self.year_month_dropdown.year.value = year
                    self.year_month_dropdown.month.value = month
                    self.year_month_dropdown.day.visible = False
                    self.year_month_dropdown.hour.visible = False
                    self.year_month_dropdown.minute.visible = False
                    self.year_month_dropdown.search.on_click = (
                        lambda e: self.select_date_data_set(
                            self.year_month_dropdown.year.data,
                            self.year_month_dropdown.month.data,
                        )
                    )
                    # 一括登録ボタン作成
                    # ボタンクリックで一括登録画面に遷移する
                    self.bulk_registration_button = ft.FilledButton(
                        content=ft.Text("一括登録", size=18),
                        width=100,
                        height=40,
                        on_click=lambda e: self.go_bulk_registration_page(),
                    )
                    # ボタン表示エリア作成
                    buttonlist_row = ft.Row(
                        controls=[
                            ft.Row(
                                controls=[
                                    self.last_month_button,
                                    self.this_month_button,
                                    self.next_month_button,
                                    self.year_month_dropdown.control,
                                ],
                                spacing=50,
                            ),
                            self.bulk_registration_button,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    )
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
                    # 引数arg_HAB_year_monthが今日でない場合
                    if not (
                        year == today.strftime("%Y") and month == today.strftime("%m")
                    ):
                        # 入力エリア初期化
                        self.input_area_clear(year, month)
                    # 登録ボタン作成
                    # ボタンクリックで入力した家計簿を登録する
                    self.entry_button = ft.FilledButton(
                        content=ft.Text("登録", size=18),
                        width=100,
                        height=40,
                        on_click=lambda e: self.value_check(),
                    )
                    # controlsに作成したコントロールを追加する
                    controls = [
                        ft.Column(
                            controls=[
                                self.header,
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            buttonlist_row,
                                            ft.Row(
                                                controls=[
                                                    self.HAB_list.control,
                                                    self.HAB_kbn_PieChart,
                                                    self.HABkinds_PieChart,
                                                ]
                                            ),
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
                                                        self.entry_button,
                                                    ],
                                                    spacing=15,
                                                ),
                                                border=ft.border.all(
                                                    2.0, ft.Colors.BLACK
                                                ),
                                                padding=20,
                                            ),
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
        self.page.window.width = self.config.window_size.HAB_list.width
        self.page.window.height = self.config.window_size.HAB_list.height
        CommonMethod.center_non_update(self.page)
        # "/HAB_list"が呼び出された時にcontrolsが表示されるように設定
        super().__init__("/HAB_list", controls)

    def HAB_list_data_set(self, arg_year, arg_month):
        """
        家計簿一覧のデータをセット
        """
        # 条件年月作成
        where_year_month = f"{arg_year}-{arg_month}"
        # 家計簿一覧取得
        fill_HAB_list = self.HAB_list_adapter.fill_HAB_list(
            where_year_month,
            self.page.data[0].user_id,
        )
        column_name = []
        row_list = []
        if fill_HAB_list.return_message_box.message_id is None:
            # 一覧の列名取得
            column_name = self.config.HAB_list_column_name.column_name
            HAB_row: HAB_Detail
            # 取得した家計簿一覧をself.HAB_listにデータをセットできるように加工
            for HAB_row in fill_HAB_list.return_row:
                row = [
                    HAB_row.HAB_seq,
                    HAB_row.HAB_at.strftime("%Y-%m-%d %H:%M"),
                    HAB_row.HAB_kbn,
                    HAB_row.amount,
                    HAB_row.HABkinds,
                    HAB_row.HABdetail,
                ]
                row_list.append(row)
            # self.HAB_listにデータをセットする
            self.HAB_list.set_data_list(column_name, row_list, True)
            return None
        else:
            # fill_HAB_list.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_HAB_list.return_message_box.message_id,
                fill_HAB_list.return_message_box.message_text,
            )
            return msg

    def fill_HAB_kbn_PieChart_data(self, arg_year, arg_month):
        """
        入出金区分円グラフ作成
        """
        # 条件年月作成
        where_year_month = f"{arg_year}-{arg_month}"
        # 家計簿一覧(入出金区分)取得
        fill_HAB_kbn_PieChart_data = self.HAB_list_adapter.fill_HAB_kbn_PieChart_data(
            where_year_month,
            self.page.data[0].user_id,
        )
        if fill_HAB_kbn_PieChart_data.return_message_box.message_id is None:
            # 入出金区分円グラフのデータ作成
            HAB_kbn_PieChart_data_list = {}
            for HAB_kbn_row in fill_HAB_kbn_PieChart_data.return_row:
                HAB_kbn_PieChart_data_list[HAB_kbn_row.m_text] = HAB_kbn_row.amount
            colors = self.config.my_pieChart_colors.HAB_kbn_colors
            HAB_kbn_my_piechart_data = [HAB_kbn_PieChart_data_list, colors]
            # 入出金区分円グラフ作成
            self.HAB_kbn_PieChart = My_Control.MyPieChart(data=HAB_kbn_my_piechart_data)
            return None
        else:
            # fill_HAB_kbn_PieChart_data.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_HAB_kbn_PieChart_data.return_message_box.message_id,
                fill_HAB_kbn_PieChart_data.return_message_box.message_text,
            )
            return msg

    def fill_HABkinds_PieChart_data(self, arg_year, arg_month):
        """
        詳細種類円グラフ作成
        """
        # 条件年月作成
        where_year_month = f"{arg_year}-{arg_month}"
        # 家計簿一覧(詳細種類)取得
        fill_HABkinds_PieChart_data = self.HAB_list_adapter.fill_HABkinds_PieChart_data(
            where_year_month,
            self.page.data[0].user_id,
        )
        if fill_HABkinds_PieChart_data.return_message_box.message_id is None:
            # 詳細種類円グラフのデータ作成
            HABkinds_PieChart_data_list = {}
            for HABkinds_row in fill_HABkinds_PieChart_data.return_row:
                HABkinds_PieChart_data_list[HABkinds_row.m_text] = HABkinds_row.amount
            colors = self.config.my_pieChart_colors.HABkinds_colors
            HABkinds_my_piechart_data = [HABkinds_PieChart_data_list, colors]
            # 詳細種類円グラフ作成
            self.HABkinds_PieChart = My_Control.MyPieChart(
                data=HABkinds_my_piechart_data
            )
            return None
        else:
            # fill_HABkinds_PieChart_data.return_message_boxに代入されたメッセージ情報を
            # 自作コントロールのメッセージボックスに渡しインスタンス化
            msg = My_Control.Msgbox(
                fill_HABkinds_PieChart_data.return_message_box.message_id,
                fill_HABkinds_PieChart_data.return_message_box.message_text,
            )
            return msg

    def input_area_clear(self, arg_year, arg_month):
        """
        入力エリアを初期化
        """
        self.datetime_dropdown.year.value = f"{arg_year}"
        self.datetime_dropdown.month.value = f"{arg_month:02}"
        self.datetime_dropdown.day.value = "01"
        self.datetime_dropdown.hour.value = "00"
        self.datetime_dropdown.minute.value = "00"
        self.datetime_dropdown.year.data = f"{arg_year}"
        self.datetime_dropdown.month.data = f"{arg_month:02}"
        self.datetime_dropdown.day.data = "01"
        self.datetime_dropdown.hour.data = "00"
        self.datetime_dropdown.minute.data = "00"
        self.HAB_kbn_dropdown.value_clear()
        self.amount_textField.value = Const.Const_Text.TEXT_BLANK
        self.HABkinds_dropdown.value_clear()
        self.HABdetail_textField.value = Const.Const_Text.TEXT_BLANK

    def last_month_data_set(self):
        """
        前月の家計簿一覧のデータをセット
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 表示している一覧の年月を取得
        year = int(self.HAB_list_year)
        month = int(self.HAB_list_month)
        # 1月の場合
        if month == 1:
            month = 12
            year = year - 1
        else:
            month = month - 1
        # コンフィグの日付時刻選択ドロップダウンの開始年と同じ年かつ1月の場合
        if year == self.config.datetime_dropdown.start_year and month == 1:
            # 前月ボタンを非活性にする
            self.last_month_button.disabled = True
        else:
            # 前月ボタンと次月ボタンを活性にする
            self.last_month_button.disabled = False
            self.next_month_button.disabled = False
        # 表示している一覧の年月 - 1の年月を渡す
        set_return = self.HAB_list_data_set(f"{year}", f"{month:02}")
        # 家計簿一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            HAB_kbn_return = self.fill_HAB_kbn_PieChart_data(f"{year}", f"{month:02}")
            if HAB_kbn_return is not None:
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(HAB_kbn_return)
            else:
                HABkinds_return = self.fill_HABkinds_PieChart_data(
                    f"{year}", f"{month:02}"
                )
                if HABkinds_return is not None:
                    # 自作コントロールのメッセージボックスをログイン画面上に表示する
                    self.page.open(HABkinds_return)
                else:
                    # 表示しているself.HAB_list_data_setを入れ替える
                    self.controls[0].controls[1].content.controls[1].controls[
                        0
                    ] = self.HAB_list.control
                    self.controls[0].controls[1].content.controls[1].controls[
                        1
                    ] = self.HAB_kbn_PieChart
                    self.controls[0].controls[1].content.controls[1].controls[
                        2
                    ] = self.HABkinds_PieChart
                    # 日付時刻選択ドロップダウンの年月を変更する
                    self.year_month_dropdown.year.value = f"{year}"
                    self.year_month_dropdown.month.value = f"{month:02}"
                    self.year_month_dropdown.year.data = f"{year}"
                    self.year_month_dropdown.month.data = f"{month:02}"
                    # 入力エリア初期化
                    self.input_area_clear(year, month)
                    # 家計簿一覧の年月を代入
                    self.HAB_list_year = f"{year}"
                    self.HAB_list_month = f"{month:02}"
        # 画面を活性にする
        self.overlay.visible = False
        # コントロールを更新する
        self.page.update()

    def this_month_data_set(self):
        """
        当月の家計簿一覧のデータをセット
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 今日の日付を取得
        today = datetime.datetime.now()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        set_return = self.HAB_list_data_set(year, month)
        # 家計簿一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            HAB_kbn_return = self.fill_HAB_kbn_PieChart_data(f"{year}", f"{month:02}")
            if HAB_kbn_return is not None:
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(HAB_kbn_return)
            else:
                HABkinds_return = self.fill_HABkinds_PieChart_data(
                    f"{year}", f"{month:02}"
                )
                if HABkinds_return is not None:
                    # 自作コントロールのメッセージボックスをログイン画面上に表示する
                    self.page.open(HABkinds_return)
                else:
                    # 表示しているself.HAB_list_data_setを入れ替える
                    self.controls[0].controls[1].content.controls[1].controls[
                        0
                    ] = self.HAB_list.control
                    self.controls[0].controls[1].content.controls[1].controls[
                        1
                    ] = self.HAB_kbn_PieChart
                    self.controls[0].controls[1].content.controls[1].controls[
                        2
                    ] = self.HABkinds_PieChart
                    # 日付時刻選択ドロップダウンの年月を変更する
                    self.year_month_dropdown.year.value = year
                    self.year_month_dropdown.month.value = month
                    self.year_month_dropdown.year.data = year
                    self.year_month_dropdown.month.data = month
                    # 入力エリア初期化
                    self.input_area_clear(year, month)
                    # 家計簿一覧の年月を代入
                    self.HAB_list_year = year
                    self.HAB_list_month = month
                    # 前月ボタンと次月ボタンを活性にする
                    self.last_month_button.disabled = False
                    self.next_month_button.disabled = False
        # 画面を活性にする
        self.overlay.visible = False
        # コントロールを更新する
        self.page.update()

    def next_month_data_set(self):
        """
        次月の家計簿一覧のデータをセット
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 表示している一覧の年月を取得
        year = int(self.HAB_list_year)
        month = int(self.HAB_list_month)
        # 12月の場合
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        # コンフィグの日付時刻選択ドロップダウンの終了年と同じ年かつ12月の場合
        if year == self.config.datetime_dropdown.end_year and month == 12:
            # 次月ボタンを非活性にする
            self.next_month_button.disabled = True
        else:
            # 前月ボタンと次月ボタンを活性にする
            self.next_month_button.disabled = False
            self.last_month_button.disabled = False
        # 表示している一覧の年月 + 1の年月を渡す
        set_return = self.HAB_list_data_set(f"{year}", f"{month:02}")
        # 家計簿一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            HAB_kbn_return = self.fill_HAB_kbn_PieChart_data(f"{year}", f"{month:02}")
            if HAB_kbn_return is not None:
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(HAB_kbn_return)
            else:
                HABkinds_return = self.fill_HABkinds_PieChart_data(
                    f"{year}", f"{month:02}"
                )
                if HABkinds_return is not None:
                    # 自作コントロールのメッセージボックスをログイン画面上に表示する
                    self.page.open(HABkinds_return)
                else:
                    # 表示しているself.HAB_list_data_setを入れ替える
                    self.controls[0].controls[1].content.controls[1].controls[
                        0
                    ] = self.HAB_list.control
                    self.controls[0].controls[1].content.controls[1].controls[
                        1
                    ] = self.HAB_kbn_PieChart
                    self.controls[0].controls[1].content.controls[1].controls[
                        2
                    ] = self.HABkinds_PieChart
                    # 日付時刻選択ドロップダウンの年月を変更する
                    self.year_month_dropdown.year.value = f"{year}"
                    self.year_month_dropdown.month.value = f"{month:02}"
                    self.year_month_dropdown.year.data = f"{year}"
                    self.year_month_dropdown.month.data = f"{month:02}"
                    # 入力エリア初期化
                    self.input_area_clear(year, month)
                    # 家計簿一覧の年月を代入
                    self.HAB_list_year = f"{year}"
                    self.HAB_list_month = f"{month:02}"
        # 画面を活性にする
        self.overlay.visible = False
        # コントロールを更新する
        self.page.update()

    def select_date_data_set(self, arg_year, arg_month):
        """
        選択した年月の家計簿一覧のデータをセット
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        set_return = self.HAB_list_data_set(arg_year, arg_month)
        # 家計簿一覧に表示するデータが取得できなかった場合
        if set_return is not None:
            # 自作コントロールのメッセージボックスをログイン画面上に表示する
            self.page.open(set_return)
        else:
            HAB_kbn_return = self.fill_HAB_kbn_PieChart_data(arg_year, arg_month)
            if HAB_kbn_return is not None:
                # 自作コントロールのメッセージボックスをログイン画面上に表示する
                self.page.open(HAB_kbn_return)
            else:
                HABkinds_return = self.fill_HABkinds_PieChart_data(arg_year, arg_month)
                if HABkinds_return is not None:
                    # 自作コントロールのメッセージボックスをログイン画面上に表示する
                    self.page.open(HABkinds_return)
                else:
                    # 表示しているself.HAB_list_data_setを入れ替える
                    self.controls[0].controls[1].content.controls[1].controls[
                        0
                    ] = self.HAB_list.control
                    self.controls[0].controls[1].content.controls[1].controls[
                        1
                    ] = self.HAB_kbn_PieChart
                    self.controls[0].controls[1].content.controls[1].controls[
                        2
                    ] = self.HABkinds_PieChart
                    # 年月選択表示機能の年月に引数の年月を代入する
                    self.year_month_dropdown.year.value = arg_year
                    self.year_month_dropdown.month.value = arg_month
                    self.year_month_dropdown.year.data = arg_year
                    self.year_month_dropdown.month.data = arg_month
                    # 入力エリア初期化
                    self.input_area_clear(arg_year, arg_month)
                    # 家計簿一覧の年月を代入
                    self.HAB_list_year = arg_year
                    self.HAB_list_month = arg_month
                    # 前月ボタンと次月ボタンの非活性判定をする
                    if (
                        arg_year == str(self.config.datetime_dropdown.start_year)
                        and arg_month == "01"
                    ):
                        # 前月ボタンを非活性にする
                        self.last_month_button.disabled = True
                    elif (
                        arg_year == str(self.config.datetime_dropdown.end_year)
                        and arg_month == "12"
                    ):
                        # 次月ボタンを非活性にする
                        self.next_month_button.disabled = True
                    else:
                        # 前月ボタンと次月ボタンを活性にする
                        self.last_month_button.disabled = False
                        self.next_month_button.disabled = False
        # 画面を活性にする
        self.overlay.visible = False
        # コントロールを更新する
        self.page.update()

    def go_bulk_registration_page(self):
        """
        一括登録画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # 一括登録画面を表示する
        self.page.go("/bulk_registration")

    def go_master_menu_page(self):
        """
        マスタメニュー画面に遷移する
        """
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        n = len(self.page.views) - 1
        self.page.views[n].data = None
        # 画面を活性にする
        self.overlay.visible = False
        # マスタメニュー画面を表示する
        self.page.go("/master_menu")

    def value_check(self):
        """
        入力値チェック
        """
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
        家計簿を登録する
        """
        self.page.close(arg_msg)
        # 画面を非活性にする
        self.overlay.visible = True
        self.page.update()
        # 家計簿詳細テーブルに登録するデータを作成する
        HAB_ditail_row = HAB_Detail()
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
        HAB_ditail_row.entry_user_id = self.page.data[0].user_id
        # 家計簿アダプターを使用し、新規登録を行う
        # return_HAB_ditailには登録成功かエラーのメッセージが代入されている
        return_HAB_ditail = self.HAB_list_adapter.create_HAB_list(
            HAB_ditail_row, self.page.data[0].user_id
        )
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
        家計簿一覧更新
        """
        self.page.close(arg_msg)
        # 家計簿一覧を更新する
        self.select_date_data_set(
            self.datetime_dropdown.year.data, self.datetime_dropdown.month.data
        )
