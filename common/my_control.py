import flet as ft


class My_Control:

    class HAB_LIST:
        def __init__(self, arg_page):
            self.page = arg_page
            self.control = None

        def on_child_click(page, e, parent_container: ft.Container):
            """
            子コントロールがクリックされた時のイベントハンドラ
            page: ページ
            e: コントロールイベント
            parent_container: 親コンテナリスト
            """
            int1 = e.control.data
            for item in parent_container:
                item.bgcolor = ft.Colors.WHITE
            parent_container[int1 + 1].bgcolor = ft.Colors.GREY
            page.update()

        def page_go(page, e, parent_container: ft.Container):
            """
            [詳]ボタンがクリックされた時のイベントハンドラ
            page: ページ
            e: コントロールイベント
            parent_container: 親コンテナリスト
            """
            int1 = e.control.data
            for item in parent_container:
                item.bgcolor = ft.Colors.WHITE
            parent_container[int1 + 1].bgcolor = ft.Colors.GREY
            page.update()
            n = len(page.views) - 1
            page.views[n].data = int1

            page.go("/detail")

        def set_data_list(self, arg_column_name, arg_data_list):
            self.control = None
            column_name = arg_column_name
            data_list = arg_data_list
            row_button_width = 40
            row_button_height = 40
            column_width = 200
            row_width = 199.95
            row_height = 40
            topfirst_row_border_config = ft.border.all(2.0, ft.Colors.BLACK)
            topinside_row_border_config = ft.border.only(
                top=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(2.0, ft.Colors.BLACK),
            )
            insidefirst_row_border_config = ft.border.only(
                left=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            )
            insideinside_row_border_config = ft.border.only(
                right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            )
            insideend_row_border_config = ft.border.only(
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            )
            endfirst_row_border_config = ft.border.only(
                left=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(2.0, ft.Colors.BLACK),
            )
            endinside_row_border_config = ft.border.only(
                right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(2.0, ft.Colors.BLACK),
            )
            endend_row_border_config = ft.border.only(
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(2.0, ft.Colors.BLACK),
            )
            # 列名作成
            column_row = []
            column_data = 0
            column_row_0 = ft.Container(
                width=row_button_width,
                height=row_button_height,
                bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.PRIMARY_CONTAINER),
                border=topfirst_row_border_config,
                data=column_data,
            )
            column_row.append(column_row_0)
            for name in column_name:
                column_data = column_data + 1
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
                    border=topinside_row_border_config,
                    data=column_data,
                    on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                        self.page,
                        e,
                        cont_list,
                        ft.Colors.RED_ACCENT_100,
                    ),
                )
                column_row.append(column)
            columu_name = ft.Row(controls=column_row, spacing=0)
            # 行作成
            detail_row = []
            row_data = 0
            for data in data_list:
                if row_data == len(data_list) - 1:
                    first_row_border_config = endfirst_row_border_config
                    inside_row_border_config = endinside_row_border_config
                    end_row_border_config = endend_row_border_config
                else:
                    first_row_border_config = insidefirst_row_border_config
                    inside_row_border_config = insideinside_row_border_config
                    end_row_border_config = insideend_row_border_config
                row_cont_list = []
                row_cont_0 = ft.Container(
                    ft.Container(
                        content=ft.TextButton(
                            content=ft.Text(
                                "詳",
                                size=12,
                                color=ft.Colors.BLACK,
                                text_align=ft.TextAlign.CENTER,
                            ),
                            data=row_data,
                            on_click=lambda e: My_Control.HAB_LIST.page_go(
                                self.page,
                                e,
                                cont_list,
                            ),
                            expand=True,
                        ),
                        alignment=ft.alignment.center,
                        bgcolor=ft.Colors.GREY,
                        border=ft.border.all(1.0),
                        border_radius=10,
                    ),
                    width=row_button_width,
                    height=row_button_height,
                    bgcolor=ft.Colors.with_opacity(0.0, ft.Colors.PRIMARY_CONTAINER),
                    border=first_row_border_config,
                    data=row_data,
                )
                row_cont_list.append(row_cont_0)
                index = 0
                for row_detail in data:
                    row_cont = ft.Container(
                        content=ft.Text(row_detail),
                        width=row_width,
                        height=row_height,
                        padding=ft.padding.only(left=5),
                        alignment=ft.alignment.center_left,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        data=row_data,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self.page,
                            e,
                            cont_list,
                        ),
                    )
                    if index == len(column_name) - 1:
                        row_cont.border = end_row_border_config
                    else:
                        row_cont.border = inside_row_border_config
                    row_cont_list.append(row_cont)
                    index = index + 1
                detail_row.append(ft.Row(controls=row_cont_list, spacing=0))
                row_data = row_data + 1
            cont_list = []
            cont_column = ft.Container()
            cont_column.content = columu_name
            cont_column.width = row_button_width + column_width * len(column_name)
            cont_list.append(cont_column)
            # 作成行をコンテナに入れる
            for content in detail_row:
                cont_row = ft.Container()
                cont_row.content = content
                cont_row.width = row_button_width + row_width * len(column_name)
                cont_row.data = lambda: content.controls[0].data
                cont_list.append(cont_row)
            # Columnを作成し、その中にheader_text、Divider、row1、row2、row3を追加
            self.control = ft.Column(
                controls=cont_list,
                spacing=0,  # Column内の要素間のスペース
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Column内の要素を水平方向中央揃え
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
            )

    # メッセージボックス
    class Msgbox(ft.AlertDialog):
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
                actions=[
                    ft.TextButton("はい", on_click=lambda e: self.page.close(self)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

    # ビュー
    class MyView(ft.View):
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
