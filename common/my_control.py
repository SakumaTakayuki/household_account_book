import flet as ft
from datetime import datetime
from db.master_adapter import Master_Adapter
from db.models import Master
from common.const import Const
from config.config import Config


class My_Control:
    """
    自作コントロール
    """

    class HAB_LIST:
        """
        一覧表
        """

        def __init__(self, arg_page):
            self.page = arg_page
            self.control = None
            """
            保存用作成コントロール
            """
            self.column_name = []
            """
            保存用列名
            """
            self.data_list = []
            """
            保存用データ
            """
            self.page_go_setting = None
            """
            詳細ボタン遷移先
            """
            self.selected_row_value = None
            """
            保存用行番号
            """

        def change_bgcolor(self, arg_parent_container: ft.Container, arg_row_no):
            """
            背景色変更
            引数
                arg_parent_container: 親コンテナリスト
                arg_row_no: 選択行番号
            """
            # 全行の背景を白にする
            for item in arg_parent_container:
                item.bgcolor = ft.Colors.WHITE
            # 選択行の背景を灰色にする
            arg_parent_container[arg_row_no + 1].bgcolor = ft.Colors.GREY

        def on_child_click(self, e, arg_parent_container: ft.Container):
            """
            子コントロールがクリックされた時のイベント
            引数
                e: コントロールイベント
                arg_parent_container: 親コンテナリスト
            """
            # 選択行番号取得
            row_no = e.control.data
            # 背景色変更
            self.change_bgcolor(arg_parent_container, row_no)
            # 選択行番号を保持する
            self.selected_row_value = row_no
            self.page.update()

        def page_go(self, e, arg_parent_container: ft.Container):
            """
            [詳]ボタンがクリックされた時のイベント
            引数
                e: コントロールイベント
                parent_container: 親コンテナリスト
            """
            # 画面を非活性にする
            self.page.views[len(self.page.views) - 1].controls[1].visible = True
            self.page.update()
            # 選択行番号取得
            row_no = e.control.data
            # 背景色変更
            self.change_bgcolor(arg_parent_container, row_no)
            n = len(self.page.views) - 1
            # 行番号のdataをビューのdataに代入する
            self.page.views[n].data = arg_parent_container[row_no + 1].data
            # 画面を活性にする
            self.page.views[len(self.page.views) - 1].controls[1].visible = False
            # 遷移先を表示する
            self.page.go(f"/{self.page_go_setting}")

        def set_data_list(
            self, arg_column_name, arg_data_list, details_button_setting=True
        ):
            """
            一覧表作成
            引数
                arg_column_name: 列名リスト
                arg_data_list: データリスト
            """
            self.control = None
            # 列名がある場合、保存用列名に代入
            if arg_column_name is not None:
                self.column_name = arg_column_name
            # データがある場合、保存用データに代入
            if arg_data_list is not None:
                self.data_list = arg_data_list
            # サイズを設定
            row_button_width = 40
            row_button_height = 40
            column_width = 200
            row_width = 199.95
            row_height = 40
            # 列名行リスト
            column_name_list = []
            # 列番号
            column_no = 0
            # 詳細ボタン表示の場合
            if details_button_setting:
                # 詳細ボタン列作成
                column_details_button = ft.Container(
                    width=row_button_width,
                    height=row_button_height,
                    bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.PRIMARY_CONTAINER),
                    border=ft.border.all(1.0, ft.Colors.BLACK),
                    data=column_no,
                )
                # 列名行リストに詳細ボタン列を追加する
                column_name_list.append(column_details_button)
                # 列番号更新
                column_no = column_no + 1
            # 保存用列名の分繰り返す
            for name in self.column_name:
                # 列名作成
                column = ft.Container(
                    content=ft.Text(
                        value=name,
                        weight=ft.FontWeight.BOLD,
                    ),
                    width=column_width,
                    height=row_height,
                    padding=ft.padding.only(left=5),
                    alignment=ft.alignment.center_left,
                    bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.PRIMARY_CONTAINER),
                    border=ft.border.all(1.0, ft.Colors.BLACK),
                    data=column_no,
                )
                # 列名行リストに作成した列名を追加する
                column_name_list.append(column)
                # 列番号更新
                column_no = column_no + 1
            # 列名行作成
            columu_name_row = ft.Row(controls=column_name_list, spacing=0)
            # コンテナリスト
            cont_list = []
            # 列名行をコンテナに追加する
            cont_column = ft.Container(
                content=columu_name_row,
                bgcolor=ft.Colors.WHITE,
            )
            # コンテナの横幅を設定する
            if details_button_setting:
                cont_column.width = row_button_width + column_width * len(
                    self.column_name
                )
            else:
                cont_column.width = column_width * len(self.column_name)
            cont_list.append(cont_column)
            # 行番号
            row_no = 0
            # 保存用データの分繰り返す
            for data in self.data_list:
                # 行データ用コンテナ作成
                cont_row = ft.Container(bgcolor=ft.Colors.WHITE, data=data[0])
                # SEQ番号削除
                del data[0]
                # コンテナの横幅を設定する
                if details_button_setting:
                    cont_row.width = row_button_width + row_width * len(
                        self.column_name
                    )
                else:
                    cont_row.width = row_width * len(self.column_name)
                # 各データ用コンテナリスト
                detail_cont_list = []
                # 詳細ボタン表示の場合
                if details_button_setting:
                    # 詳細ボタン作成
                    row_cont_details_button = ft.Container(
                        ft.Container(
                            content=ft.TextButton(
                                content=ft.Text(
                                    "詳",
                                    size=12,
                                    color=ft.Colors.BLACK,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                data=row_no,
                                on_click=lambda e: My_Control.HAB_LIST.page_go(
                                    self,
                                    e,
                                    cont_list,
                                ),
                            ),
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.GREY,
                            border=ft.border.all(1.0),
                            border_radius=10,
                        ),
                        width=row_button_width,
                        height=row_button_height,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=ft.border.all(0.5, ft.Colors.BLACK),
                        data=row_no,
                    )
                    # 各データ用コンテナリストに詳細ボタンを追加する
                    detail_cont_list.append(row_cont_details_button)
                # データの分繰り返す
                for data_detail in data:
                    # 表示するデータ作成
                    row_cont = ft.Container(
                        content=ft.Text(data_detail),
                        width=row_width,
                        height=row_height,
                        padding=ft.padding.only(left=5),
                        alignment=ft.alignment.center_left,
                        border=ft.border.all(0.5, ft.Colors.BLACK),
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        data=row_no,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self,
                            e,
                            cont_list,
                        ),
                    )
                    # 各データ用コンテナリストに表示するデータを追加する
                    detail_cont_list.append(row_cont)
                # 表示するデータを1行に成形する
                detail_row = ft.Row(controls=detail_cont_list, spacing=0)
                # 成形した行が行データ用コンテナに表示されるよう設定する
                cont_row.content = detail_row
                # 行データ用コンテナをコンテナリストに追加する
                cont_list.append(cont_row)
                # 行番号更新
                row_no = row_no + 1
            # スクロールを表示するために、列コントロールにコンテナリストが表示されるよう設定
            # コンテナに列コントロールが表示されるよう設定し、保存用作成コントロールに代入する
            self.control = ft.Container(
                content=ft.Column(
                    controls=cont_list,
                    spacing=0,
                    scroll=ft.ScrollMode.ALWAYS,
                ),
                height=450,
                border=ft.border.all(2.0, ft.Colors.BLACK),
            )

    class MyView(ft.View):
        """
        背景色を設定したビュー
        """

        def __init__(
            self,
            route=None,
            controls=None,
            appbar=None,
            bottom_appbar=None,
            floating_action_button=None,
            floating_action_button_location=None,
            navigation_bar=None,
            drawer=None,
            end_drawer=None,
            vertical_alignment=None,
            horizontal_alignment=None,
            spacing=None,
            padding=None,
            bgcolor=ft.Colors.LIGHT_BLUE_50,
            decoration=None,
            foreground_decoration=None,
            can_pop=None,
            on_confirm_pop=None,
            scroll=None,
            auto_scroll=None,
            fullscreen_dialog=None,
            on_scroll_interval=None,
            on_scroll=None,
            adaptive=None,
        ):
            super().__init__(
                route,
                controls,
                appbar,
                bottom_appbar,
                floating_action_button,
                floating_action_button_location,
                navigation_bar,
                drawer,
                end_drawer,
                vertical_alignment,
                horizontal_alignment,
                spacing,
                padding,
                bgcolor,
                decoration,
                foreground_decoration,
                can_pop,
                on_confirm_pop,
                scroll,
                auto_scroll,
                fullscreen_dialog,
                on_scroll_interval,
                on_scroll,
                adaptive,
            )

    class MyOverlay:
        """
        自作オーバーレイ
        """

        def __init__(self, arg_page: ft.Page):
            self.overlay = ft.Stack(
                controls=[
                    ft.Container(
                        width=arg_page.window.width,
                        height=arg_page.window.height,
                        alignment=ft.alignment.center,
                    )
                ],
                visible=False,
            )

    class Header_Area:
        """
        ヘッダ部エリア
        """

        def __init__(
            self,
            arg_display_name,
        ):
            """
            引数
                arg_display_name: 画面名
            """
            self.control = None
            # 画面ラベル作成
            self.display_label = ft.Container(
                content=ft.Text(
                    arg_display_name,
                    size=30,
                    weight=ft.FontWeight.BOLD,
                ),
                alignment=ft.alignment.center,
            )
            # 戻るボタン作成
            # ボタンクリックで1つ前の画面に戻る
            self.back_button = ft.FilledButton(
                content=ft.Text("戻る", size=18),
                width=100,
                height=40,
            )
            # ヘッダ部エリア作成
            self.control = ft.Row(
                controls=[
                    ft.Container(width=100),
                    self.display_label,
                    self.back_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

    class Msgbox(ft.AlertDialog):
        """
        アクションを設定した自作メッセージボックス
        """

        def __init__(self, arg_title, arg_content):
            """
            メッセージボックス作成
            引数
                arg_title：メッセージID
                arg_content：メッセージ内容
            """
            super().__init__(
                modal=True,
                title=ft.Text(
                    f"【{arg_title}】",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
                content=ft.Text(f"{arg_content}", size=18),
                actions_alignment=ft.MainAxisAlignment.END,
            )
            # メッセージIDの末尾が'W'の場合
            if arg_title[-1] == Const.Log_Kinds.WARNING:
                # ウィンドウが閉じるように設定
                self.actions = [
                    ft.TextButton("はい", on_click=lambda e: self.page.window.close())
                ]
            else:
                # メッセージが閉じるように設定
                self.actions = [
                    ft.TextButton("はい", on_click=lambda e: self.page.close(self))
                ]

    class MyDropdown(ft.Dropdown):
        """
        背景色、リストの背景色を白に設定した自作ドロップダウン
        """

        def __init__(
            self,
            value=None,
            autofocus=None,
            text_align=None,
            elevation=None,
            options=None,
            label_content=None,
            enable_filter=None,
            enable_search=None,
            editable=False,
            max_menu_height=None,
            menu_height=None,
            menu_width=None,
            expanded_insets=None,
            selected_suffix=None,
            input_filter=None,
            capitalization=None,
            options_fill_horizontally=None,
            padding=None,
            trailing_icon=None,
            leading_icon=None,
            select_icon=None,
            selected_trailing_icon=None,
            on_change=None,
            on_focus=None,
            on_blur=None,
            enable_feedback=None,
            item_height=None,
            alignment=None,
            hint_content=None,
            icon_content=None,
            select_icon_size=None,
            icon_size=None,
            select_icon_enabled_color=None,
            icon_enabled_color=None,
            select_icon_disabled_color=None,
            icon_disabled_color=None,
            bgcolor=ft.Colors.WHITE,
            error_style=None,
            error_text=None,
            text_size=18,
            text_style=None,
            label=None,
            label_style=None,
            icon=None,
            border=None,
            color=None,
            focused_color=None,
            focused_bgcolor=None,
            border_width=None,
            border_color=None,
            border_radius=None,
            focused_border_width=None,
            focused_border_color=None,
            content_padding=None,
            dense=None,
            filled=True,
            fill_color=ft.Colors.WHITE,
            hover_color=None,
            hint_text=None,
            hint_style=None,
            helper_text=None,
            helper_style=None,
            prefix=None,
            prefix_text=None,
            prefix_style=None,
            prefix_icon=None,
            disabled_hint_content=None,
            suffix=None,
            suffix_icon=None,
            suffix_text=None,
            suffix_style=None,
            counter=None,
            counter_text=None,
            counter_style=None,
            ref=None,
            key=None,
            width=None,
            expand=None,
            expand_loose=None,
            col=None,
            opacity=None,
            rotate=None,
            scale=None,
            offset=None,
            aspect_ratio=None,
            animate_opacity=None,
            animate_size=None,
            animate_position=None,
            animate_rotation=None,
            animate_scale=None,
            animate_offset=None,
            on_animation_end=None,
            tooltip=None,
            visible=None,
            disabled=None,
            data=None,
        ):
            super().__init__(
                value,
                autofocus,
                text_align,
                elevation,
                options,
                label_content,
                enable_filter,
                enable_search,
                editable,
                max_menu_height,
                menu_height,
                menu_width,
                expanded_insets,
                selected_suffix,
                input_filter,
                capitalization,
                options_fill_horizontally,
                padding,
                trailing_icon,
                leading_icon,
                select_icon,
                selected_trailing_icon,
                on_change,
                on_focus,
                on_blur,
                enable_feedback,
                item_height,
                alignment,
                hint_content,
                icon_content,
                select_icon_size,
                icon_size,
                select_icon_enabled_color,
                icon_enabled_color,
                select_icon_disabled_color,
                icon_disabled_color,
                bgcolor,
                error_style,
                error_text,
                text_size,
                text_style,
                label,
                label_style,
                icon,
                border,
                color,
                focused_color,
                focused_bgcolor,
                border_width,
                border_color,
                border_radius,
                focused_border_width,
                focused_border_color,
                content_padding,
                dense,
                filled,
                fill_color,
                hover_color,
                hint_text,
                hint_style,
                helper_text,
                helper_style,
                prefix,
                prefix_text,
                prefix_style,
                prefix_icon,
                disabled_hint_content,
                suffix,
                suffix_icon,
                suffix_text,
                suffix_style,
                counter,
                counter_text,
                counter_style,
                ref,
                key,
                width,
                expand,
                expand_loose,
                col,
                opacity,
                rotate,
                scale,
                offset,
                aspect_ratio,
                animate_opacity,
                animate_size,
                animate_position,
                animate_rotation,
                animate_scale,
                animate_offset,
                on_animation_end,
                tooltip,
                visible,
                disabled,
                data,
            )

        def change_dropdown(self, e):
            """
            選択した項目のdataをドロップダウンのdataに代入する
            """
            for option in self.options:
                if option.key == e.data:
                    self.data = option.data
                    return

        def value_clear(self):
            """
            値を初期化する
            """
            self.value = self.options[0].key
            self.data = self.options[0].data

    class Datetime_Dropdown:
        """
        自作日付時刻選択ドロップダウン
        """

        def __init__(self, arg_page):
            self.page = arg_page
            self.control = None
            # 今日の日付取得
            self.today = datetime.now()
            # 年リスト
            year_options = []
            # コンフィグで設定した開始年から終了年までのリストを作成する
            config = Config()
            for year in range(
                int(config.datetime_dropdown.start_year),
                int(config.datetime_dropdown.end_year) + 1,
            ):
                year_options.append(
                    ft.DropdownOption(
                        key=year, content=ft.Text(year, size=18), data=year
                    )
                )
            # 年ドロップダウン作成
            self.year = My_Control.MyDropdown(
                label=ft.Text(value="年", size=18, weight=ft.FontWeight.BOLD),
                options=year_options,
                width=110,
                menu_height=200,
                on_change=lambda e: self.day_create(
                    self.year.value, self.month.value, self.day.value
                ),
            )
            # 月リスト
            month_options = []
            # 月リスト作成
            for month in range(1, 13):
                month = f"{month:02}"
                month_options.append(
                    ft.DropdownOption(
                        key=month, content=ft.Text(month, size=18), data=month
                    )
                )
            # 月ドロップダウン作成
            self.month = My_Control.MyDropdown(
                label=ft.Text(value="月", size=18, weight=ft.FontWeight.BOLD),
                options=month_options,
                width=100,
                menu_height=200,
                on_change=lambda e: self.day_create(
                    self.year.value, self.month.value, self.day.value
                ),
            )
            # 日リスト
            day_options = []
            # 日ドロップダウン作成
            self.day = My_Control.MyDropdown(
                label=ft.Text(value="日", size=18, weight=ft.FontWeight.BOLD),
                options=day_options,
                width=100,
                menu_height=200,
                on_change=lambda e: self.set_data(
                    self.year.value, self.month.value, self.day.value
                ),
            )
            # 日リスト作成
            self.day_create(
                self.today.strftime("%Y"),
                self.today.strftime("%m"),
                self.today.strftime("%d"),
            )
            # 時リスト
            hour_options = []
            # 時リスト作成
            for hour in range(0, 24):
                hour = f"{hour:02}"
                hour_options.append(
                    ft.DropdownOption(
                        key=hour, content=ft.Text(hour, size=18), data=hour
                    )
                )
            # 時ドロップダウン作成
            self.hour = My_Control.MyDropdown(
                label=ft.Text(value="時", size=18, weight=ft.FontWeight.BOLD),
                options=hour_options,
                width=100,
                menu_height=200,
                on_change=lambda e: self.hour.change_dropdown(e),
            )
            # 分リスト
            minute_options = []
            # 分リスト作成
            for minute in range(0, 60):
                minute = f"{minute:02}"
                minute_options.append(
                    ft.DropdownOption(
                        key=minute, content=ft.Text(minute, size=18), data=minute
                    )
                )
            # 分ドロップダウン作成
            self.minute = My_Control.MyDropdown(
                label=ft.Text(value="分", size=18, weight=ft.FontWeight.BOLD),
                options=minute_options,
                width=100,
                menu_height=200,
                on_change=lambda e: self.minute.change_dropdown(e),
            )
            # 表示ボタン作成
            self.search = ft.FilledButton(
                content=ft.Text("表示", size=18),
                width=100,
                height=40,
            )
            # 初期値設定
            self.set_initial_value()
            self.control = ft.Row(
                controls=[
                    self.year,
                    self.month,
                    self.day,
                    self.hour,
                    self.minute,
                    self.search,
                ],
                spacing=0,
            )

        def day_create(self, arg_year, arg_month, arg_day):
            """
            日付を作成する
            """
            year = int(arg_year)
            month = int(arg_month)
            day = int(arg_day)
            days = None
            # 各月の日付設定
            if month == 2:
                if year % 4 == 0:
                    if year % 100 == 0 and year % 400 != 0:
                        days = 28
                    else:
                        days = 29
                else:
                    days = 28
            elif month == 4 or month == 6 or month == 9 or month == 11:
                days = 30
            else:
                days = 31
            # 日作成
            day_options = []
            for i in range(1, days + 1):
                i = f"{i:02}"
                day_options.append(
                    ft.DropdownOption(key=i, content=ft.Text(i, size=18), data=i)
                )
            # 日表示設定
            if day > days:
                day = days
            self.day.options = day_options
            self.set_data(year, month, day)

        def set_data(self, arg_year, arg_month, arg_day):
            """
            dataに値を代入する
            """
            self.year.data = f"{arg_year}"
            self.month.data = f"{arg_month:02}"
            self.day.data = f"{arg_day:02}"
            self.page.update()

        def set_initial_value(self):
            """
            初期値を設定する
            """
            self.year.value = self.today.strftime("%Y")
            self.year.data = self.today.strftime("%Y")
            self.month.value = self.today.strftime("%m")
            self.month.data = self.today.strftime("%m")
            self.day.value = self.today.strftime("%d")
            self.day.data = self.today.strftime("%d")
            self.hour.value = "00"
            self.hour.data = "00"
            self.minute.value = "00"
            self.minute.data = "00"

    # 入出金区分ドロップダウン
    class HAB_Kbn_Dropdown(MyDropdown):
        """
        入出金区分ドロップダウン
        """

        def __init__(
            self,
            value=None,
            autofocus=None,
            text_align=None,
            elevation=None,
            options=None,
            label_content=None,
            enable_filter=None,
            enable_search=None,
            editable=False,
            max_menu_height=None,
            menu_height=None,
            menu_width=None,
            expanded_insets=None,
            selected_suffix=None,
            input_filter=None,
            capitalization=None,
            options_fill_horizontally=None,
            padding=None,
            trailing_icon=None,
            leading_icon=None,
            select_icon=None,
            selected_trailing_icon=None,
            on_change=None,
            on_focus=None,
            on_blur=None,
            enable_feedback=None,
            item_height=None,
            alignment=None,
            hint_content=None,
            icon_content=None,
            select_icon_size=None,
            icon_size=None,
            select_icon_enabled_color=None,
            icon_enabled_color=None,
            select_icon_disabled_color=None,
            icon_disabled_color=None,
            bgcolor=ft.Colors.WHITE,
            error_style=None,
            error_text=None,
            text_size=18,
            text_style=None,
            label=ft.Text(value="入出金区分", size=18, weight=ft.FontWeight.BOLD),
            label_style=None,
            icon=None,
            border=None,
            color=None,
            focused_color=None,
            focused_bgcolor=None,
            border_width=None,
            border_color=None,
            border_radius=None,
            focused_border_width=None,
            focused_border_color=None,
            content_padding=None,
            dense=None,
            filled=True,
            fill_color=ft.Colors.WHITE,
            hover_color=None,
            hint_text=None,
            hint_style=None,
            helper_text=None,
            helper_style=None,
            prefix=None,
            prefix_text=None,
            prefix_style=None,
            prefix_icon=None,
            disabled_hint_content=None,
            suffix=None,
            suffix_icon=None,
            suffix_text=None,
            suffix_style=None,
            counter=None,
            counter_text=None,
            counter_style=None,
            ref=None,
            key=None,
            width=100,
            expand=None,
            expand_loose=None,
            col=None,
            opacity=None,
            rotate=None,
            scale=None,
            offset=None,
            aspect_ratio=None,
            animate_opacity=None,
            animate_size=None,
            animate_position=None,
            animate_rotation=None,
            animate_scale=None,
            animate_offset=None,
            on_animation_end=None,
            tooltip=None,
            visible=None,
            disabled=None,
            data=None,
        ):
            # マスターアダプターインスタンス化
            master_adapter = Master_Adapter()
            # 入出金区分取得
            HAB_kbn_list = master_adapter.fill_HAB_kbn()
            HAB_kbn_options = []
            HAB_kbn_row: Master
            # オプションに入出金区分をセットする
            for HAB_kbn_row in HAB_kbn_list.return_row:
                HAB_kbn_options.append(
                    ft.DropdownOption(
                        key=HAB_kbn_row.m_text,
                        content=ft.Text(HAB_kbn_row.m_text, size=18),
                        data=HAB_kbn_row.m_code,
                    )
                )
            options = HAB_kbn_options
            # 初期値の設定
            value = HAB_kbn_list.return_row[0].m_text
            data = HAB_kbn_list.return_row[0].m_code
            # ドロップダウン変更時のメソッドを設定
            on_change = lambda e: self.change_dropdown(e)
            super().__init__(
                value,
                autofocus,
                text_align,
                elevation,
                options,
                label_content,
                enable_filter,
                enable_search,
                editable,
                max_menu_height,
                menu_height,
                menu_width,
                expanded_insets,
                selected_suffix,
                input_filter,
                capitalization,
                options_fill_horizontally,
                padding,
                trailing_icon,
                leading_icon,
                select_icon,
                selected_trailing_icon,
                on_change,
                on_focus,
                on_blur,
                enable_feedback,
                item_height,
                alignment,
                hint_content,
                icon_content,
                select_icon_size,
                icon_size,
                select_icon_enabled_color,
                icon_enabled_color,
                select_icon_disabled_color,
                icon_disabled_color,
                bgcolor,
                error_style,
                error_text,
                text_size,
                text_style,
                label,
                label_style,
                icon,
                border,
                color,
                focused_color,
                focused_bgcolor,
                border_width,
                border_color,
                border_radius,
                focused_border_width,
                focused_border_color,
                content_padding,
                dense,
                filled,
                fill_color,
                hover_color,
                hint_text,
                hint_style,
                helper_text,
                helper_style,
                prefix,
                prefix_text,
                prefix_style,
                prefix_icon,
                disabled_hint_content,
                suffix,
                suffix_icon,
                suffix_text,
                suffix_style,
                counter,
                counter_text,
                counter_style,
                ref,
                key,
                width,
                expand,
                expand_loose,
                col,
                opacity,
                rotate,
                scale,
                offset,
                aspect_ratio,
                animate_opacity,
                animate_size,
                animate_position,
                animate_rotation,
                animate_scale,
                animate_offset,
                on_animation_end,
                tooltip,
                visible,
                disabled,
                data,
            )

    # 詳細種類ドロップダウン
    class HABkinds_Dropdown(MyDropdown):
        """
        詳細種類ドロップダウン
        """

        def __init__(
            self,
            value=None,
            autofocus=None,
            text_align=None,
            elevation=None,
            options=None,
            label_content=None,
            enable_filter=None,
            enable_search=None,
            editable=False,
            max_menu_height=None,
            menu_height=None,
            menu_width=None,
            expanded_insets=None,
            selected_suffix=None,
            input_filter=None,
            capitalization=None,
            options_fill_horizontally=None,
            padding=None,
            trailing_icon=None,
            leading_icon=None,
            select_icon=None,
            selected_trailing_icon=None,
            on_change=None,
            on_focus=None,
            on_blur=None,
            enable_feedback=None,
            item_height=None,
            alignment=None,
            hint_content=None,
            icon_content=None,
            select_icon_size=None,
            icon_size=None,
            select_icon_enabled_color=None,
            icon_enabled_color=None,
            select_icon_disabled_color=None,
            icon_disabled_color=None,
            bgcolor=ft.Colors.WHITE,
            error_style=None,
            error_text=None,
            text_size=18,
            text_style=None,
            label=ft.Text(value="詳細種類", size=18, weight=ft.FontWeight.BOLD),
            label_style=None,
            icon=None,
            border=None,
            color=None,
            focused_color=None,
            focused_bgcolor=None,
            border_width=None,
            border_color=None,
            border_radius=None,
            focused_border_width=None,
            focused_border_color=None,
            content_padding=None,
            dense=None,
            filled=True,
            fill_color=ft.Colors.WHITE,
            hover_color=None,
            hint_text=None,
            hint_style=None,
            helper_text=None,
            helper_style=None,
            prefix=None,
            prefix_text=None,
            prefix_style=None,
            prefix_icon=None,
            disabled_hint_content=None,
            suffix=None,
            suffix_icon=None,
            suffix_text=None,
            suffix_style=None,
            counter=None,
            counter_text=None,
            counter_style=None,
            ref=None,
            key=None,
            width=None,
            expand=None,
            expand_loose=None,
            col=None,
            opacity=None,
            rotate=None,
            scale=None,
            offset=None,
            aspect_ratio=None,
            animate_opacity=None,
            animate_size=None,
            animate_position=None,
            animate_rotation=None,
            animate_scale=None,
            animate_offset=None,
            on_animation_end=None,
            tooltip=None,
            visible=None,
            disabled=None,
            data=None,
        ):
            # マスターアダプターインスタンス化
            master_adapter = Master_Adapter()
            # 詳細種類を取得
            HABkinds_list = master_adapter.fill_HABkinds()
            HABkinds_options = []
            HABkinds_row: Master
            # オプションに詳細種類をセット
            for HABkinds_row in HABkinds_list.return_row:
                HABkinds_options.append(
                    ft.DropdownOption(
                        key=HABkinds_row.m_text,
                        content=ft.Text(HABkinds_row.m_text, size=18),
                        data=HABkinds_row.m_code,
                    )
                )
            options = HABkinds_options
            # 初期値を設定
            value = HABkinds_list.return_row[0].m_text
            data = HABkinds_list.return_row[0].m_code
            # ドロップダウン変更時のメソッドを設定
            on_change = lambda e: self.change_dropdown(e)
            super().__init__(
                value,
                autofocus,
                text_align,
                elevation,
                options,
                label_content,
                enable_filter,
                enable_search,
                editable,
                max_menu_height,
                menu_height,
                menu_width,
                expanded_insets,
                selected_suffix,
                input_filter,
                capitalization,
                options_fill_horizontally,
                padding,
                trailing_icon,
                leading_icon,
                select_icon,
                selected_trailing_icon,
                on_change,
                on_focus,
                on_blur,
                enable_feedback,
                item_height,
                alignment,
                hint_content,
                icon_content,
                select_icon_size,
                icon_size,
                select_icon_enabled_color,
                icon_enabled_color,
                select_icon_disabled_color,
                icon_disabled_color,
                bgcolor,
                error_style,
                error_text,
                text_size,
                text_style,
                label,
                label_style,
                icon,
                border,
                color,
                focused_color,
                focused_bgcolor,
                border_width,
                border_color,
                border_radius,
                focused_border_width,
                focused_border_color,
                content_padding,
                dense,
                filled,
                fill_color,
                hover_color,
                hint_text,
                hint_style,
                helper_text,
                helper_style,
                prefix,
                prefix_text,
                prefix_style,
                prefix_icon,
                disabled_hint_content,
                suffix,
                suffix_icon,
                suffix_text,
                suffix_style,
                counter,
                counter_text,
                counter_style,
                ref,
                key,
                width,
                expand,
                expand_loose,
                col,
                opacity,
                rotate,
                scale,
                offset,
                aspect_ratio,
                animate_opacity,
                animate_size,
                animate_position,
                animate_rotation,
                animate_scale,
                animate_offset,
                on_animation_end,
                tooltip,
                visible,
                disabled,
                data,
            )

    # 会社選択ドロップダウン
    class CSV_Company_Dropdown(MyDropdown):
        """
        会社選択ドロップダウン
        """

        def __init__(
            self,
            value=None,
            autofocus=None,
            text_align=None,
            elevation=None,
            options=None,
            label_content=None,
            enable_filter=None,
            enable_search=None,
            editable=False,
            max_menu_height=None,
            menu_height=None,
            menu_width=None,
            expanded_insets=None,
            selected_suffix=None,
            input_filter=None,
            capitalization=None,
            options_fill_horizontally=None,
            padding=None,
            trailing_icon=None,
            leading_icon=None,
            select_icon=None,
            selected_trailing_icon=None,
            on_change=None,
            on_focus=None,
            on_blur=None,
            enable_feedback=None,
            item_height=None,
            alignment=None,
            hint_content=None,
            icon_content=None,
            select_icon_size=None,
            icon_size=None,
            select_icon_enabled_color=None,
            icon_enabled_color=None,
            select_icon_disabled_color=None,
            icon_disabled_color=None,
            bgcolor=ft.Colors.WHITE,
            error_style=None,
            error_text=None,
            text_size=18,
            text_style=None,
            label=ft.Text(value="CSV提供会社", size=18, weight=ft.FontWeight.BOLD),
            label_style=None,
            icon=None,
            border=None,
            color=None,
            focused_color=None,
            focused_bgcolor=None,
            border_width=None,
            border_color=None,
            border_radius=None,
            focused_border_width=None,
            focused_border_color=None,
            content_padding=None,
            dense=None,
            filled=True,
            fill_color=ft.Colors.WHITE,
            hover_color=None,
            hint_text=None,
            hint_style=None,
            helper_text=None,
            helper_style=None,
            prefix=None,
            prefix_text=None,
            prefix_style=None,
            prefix_icon=None,
            disabled_hint_content=None,
            suffix=None,
            suffix_icon=None,
            suffix_text=None,
            suffix_style=None,
            counter=None,
            counter_text=None,
            counter_style=None,
            ref=None,
            key=None,
            width=None,
            expand=None,
            expand_loose=None,
            col=None,
            opacity=None,
            rotate=None,
            scale=None,
            offset=None,
            aspect_ratio=None,
            animate_opacity=None,
            animate_size=None,
            animate_position=None,
            animate_rotation=None,
            animate_scale=None,
            animate_offset=None,
            on_animation_end=None,
            tooltip=None,
            visible=None,
            disabled=None,
            data=None,
        ):
            # マスターアダプターインスタンス化
            master_adapter = Master_Adapter()
            # 会社名を取得
            CSV_company_list = master_adapter.fill_CSV_company()
            CSV_company_list_options = []
            CSV_company_list_row: Master
            # オプションに会社名をセット
            for CSV_company_list_row in CSV_company_list.return_row:
                CSV_company_list_options.append(
                    ft.DropdownOption(
                        key=CSV_company_list_row.m_text,
                        content=ft.Text(CSV_company_list_row.m_text, size=18),
                        data=CSV_company_list_row.m_code,
                    )
                )
            options = CSV_company_list_options
            # 初期値を設定
            value = CSV_company_list.return_row[0].m_text
            data = CSV_company_list.return_row[0].m_code
            # ドロップダウン変更時のメソッドを設定
            on_change = lambda e: self.change_dropdown(e)
            super().__init__(
                value,
                autofocus,
                text_align,
                elevation,
                options,
                label_content,
                enable_filter,
                enable_search,
                editable,
                max_menu_height,
                menu_height,
                menu_width,
                expanded_insets,
                selected_suffix,
                input_filter,
                capitalization,
                options_fill_horizontally,
                padding,
                trailing_icon,
                leading_icon,
                select_icon,
                selected_trailing_icon,
                on_change,
                on_focus,
                on_blur,
                enable_feedback,
                item_height,
                alignment,
                hint_content,
                icon_content,
                select_icon_size,
                icon_size,
                select_icon_enabled_color,
                icon_enabled_color,
                select_icon_disabled_color,
                icon_disabled_color,
                bgcolor,
                error_style,
                error_text,
                text_size,
                text_style,
                label,
                label_style,
                icon,
                border,
                color,
                focused_color,
                focused_bgcolor,
                border_width,
                border_color,
                border_radius,
                focused_border_width,
                focused_border_color,
                content_padding,
                dense,
                filled,
                fill_color,
                hover_color,
                hint_text,
                hint_style,
                helper_text,
                helper_style,
                prefix,
                prefix_text,
                prefix_style,
                prefix_icon,
                disabled_hint_content,
                suffix,
                suffix_icon,
                suffix_text,
                suffix_style,
                counter,
                counter_text,
                counter_style,
                ref,
                key,
                width,
                expand,
                expand_loose,
                col,
                opacity,
                rotate,
                scale,
                offset,
                aspect_ratio,
                animate_opacity,
                animate_size,
                animate_position,
                animate_rotation,
                animate_scale,
                animate_offset,
                on_animation_end,
                tooltip,
                visible,
                disabled,
                data,
            )

    # 円グラフ
    class MyPieChart(ft.PieChart):
        """
        円グラフ
        """

        def __init__(
            self,
            sections=None,
            center_space_color=None,
            center_space_radius=None,
            sections_space=None,
            start_degree_offset=None,
            animate=None,
            on_chart_event=None,
            ref=None,
            width=None,
            height=None,
            left=None,
            top=None,
            right=None,
            bottom=None,
            expand=None,
            expand_loose=None,
            col=None,
            opacity=None,
            rotate=None,
            scale=None,
            offset=None,
            aspect_ratio=None,
            animate_opacity=None,
            animate_size=None,
            animate_position=None,
            animate_rotation=None,
            animate_scale=None,
            animate_offset=None,
            on_animation_end=None,
            tooltip=None,
            badge=None,
            visible=None,
            disabled=None,
            data=None,
        ):
            data_list: dict = data[0]
            color_list = data[1]
            # PieChartSection のリストを作成
            sections = []
            total_value = sum(data_list.values())  # 全体の合計値を計算
            for i, (label, value) in enumerate(data_list.items()):
                # 各セクションのパーセンテージを計算
                percentage = (value / total_value) * 100 if total_value > 0 else 0
                sections.append(
                    ft.PieChartSection(
                        value=value,
                        color=color_list[i],  # 色のリストから割り当てる
                        radius=150,  # 扇の半径
                        title=f"{label}\n{percentage:.1f}% {value}円",  # ラベルとパーセンテージをタイトルに
                        title_style=ft.TextStyle(
                            size=14, color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD
                        ),
                    )
                )
            sections = sections
            sections_space = 2  # 各セクション間のスペース
            center_space_radius = 32  # 中心に空ける円の半径 (ドーナツグラフにする場合)
            expand = True  # 親コンポーネントに合わせて拡大する場合
            super().__init__(
                sections,
                center_space_color,
                center_space_radius,
                sections_space,
                start_degree_offset,
                animate,
                on_chart_event,
                ref,
                width,
                height,
                left,
                top,
                right,
                bottom,
                expand,
                expand_loose,
                col,
                opacity,
                rotate,
                scale,
                offset,
                aspect_ratio,
                animate_opacity,
                animate_size,
                animate_position,
                animate_rotation,
                animate_scale,
                animate_offset,
                on_animation_end,
                tooltip,
                badge,
                visible,
                disabled,
                data,
            )
