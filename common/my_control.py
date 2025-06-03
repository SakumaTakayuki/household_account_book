import flet as ft


class My_Control:

    class HAB_LIST:
        def __init__(self, testpage):
            self.page = testpage
            self.control = None
            row_button_width = 50
            row_button_height = 50
            row_width = 100
            row_height = 50
            topfirst_row_border_config = ft.border.all(2.0, ft.Colors.BLACK)
            topinside_row_border_config = ft.border.only(
                top=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                right=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(2.0, ft.Colors.BLACK),
            )
            insidefirst_row_border_config = ft.border.only(
                left=ft.border.BorderSide(2.0, ft.Colors.BLACK),
                right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            )
            insideinside_row_border_config = ft.border.only(
                right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
                bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            )
            # 列名作成
            i = 999
            test1 = ft.Row(
                [
                    ft.Container(
                        width=50,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=topfirst_row_border_config,
                        data=i,
                    ),
                    ft.Container(
                        content=ft.Text(f"利用日時"),
                        width=200,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=topinside_row_border_config,
                        data=i,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self.page,
                            e,
                            testConlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(f"入出金区分"),
                        width=200,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=topinside_row_border_config,
                        data=i,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self.page,
                            e,
                            testConlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(f"金額"),
                        width=200,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=topinside_row_border_config,
                        data=i,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self.page,
                            e,
                            testConlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(f"詳細種類"),
                        width=200,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=topinside_row_border_config,
                        data=i,
                        on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                            self.page,
                            e,
                            testConlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
                    ),
                ],
                spacing=0,
            )
            # 行作成
            testlist = []
            row_count = 50
            for i in range(0, row_count):
                first_column_border_config = insidefirst_row_border_config
                inside_column_border_config = insideinside_row_border_config
                test = ft.Row(
                    [
                        ft.Container(
                            content=ft.Button(
                                text="詳",
                                bgcolor=ft.Colors.with_opacity(
                                    0.0, ft.Colors.PRIMARY_CONTAINER
                                ),
                                data=i,
                                on_click=lambda e: My_Control.HAB_LIST.page_go(
                                    self.page,
                                    e,
                                    testConlist,
                                    ft.Colors.RED_ACCENT_100,
                                ),
                            ),
                            width=50,
                            height=50,
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.0, ft.Colors.PRIMARY_CONTAINER
                            ),
                            border=first_column_border_config,
                            data=i,
                        ),
                        ft.Container(
                            content=ft.Text(f"testB{i}"),
                            width=200,
                            height=50,
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.0, ft.Colors.PRIMARY_CONTAINER
                            ),
                            border=inside_column_border_config,
                            data=i,
                            on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                                self.page,
                                e,
                                testConlist,
                                ft.Colors.RED_ACCENT_100,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(f"testC{i}"),
                            width=200,
                            height=50,
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.0, ft.Colors.PRIMARY_CONTAINER
                            ),
                            border=inside_column_border_config,
                            data=i,
                            on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                                self.page,
                                e,
                                testConlist,
                                ft.Colors.RED_ACCENT_100,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(f"testD{i}"),
                            width=200,
                            height=50,
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.0, ft.Colors.PRIMARY_CONTAINER
                            ),
                            border=inside_column_border_config,
                            data=i,
                            on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                                self.page,
                                e,
                                testConlist,
                                ft.Colors.RED_ACCENT_100,
                            ),
                        ),
                        ft.Container(
                            content=ft.Text(f"testE{i}"),
                            width=200,
                            height=50,
                            padding=10,
                            bgcolor=ft.Colors.with_opacity(
                                0.0, ft.Colors.PRIMARY_CONTAINER
                            ),
                            border=inside_column_border_config,
                            data=i,
                            on_click=lambda e: My_Control.HAB_LIST.on_child_click(
                                self.page,
                                e,
                                testConlist,
                                ft.Colors.RED_ACCENT_100,
                            ),
                        ),
                    ],
                    spacing=0,
                )
                testlist.append(test)
            testConlist = []
            testCon0 = ft.Container()
            testCon0.content = test1
            testCon0.width = (
                test1.controls[0].width
                + test1.controls[1].width
                + test1.controls[2].width
                + test1.controls[3].width
                + test1.controls[4].width
            )
            testConlist.append(testCon0)
            # 作成行をコンテナに入れる
            for i in range(0, row_count):
                testCon = ft.Container()
                testCon.content = testlist[i]
                testCon.width = (
                    testlist[i].controls[0].width
                    + testlist[i].controls[1].width
                    + testlist[i].controls[2].width
                    + testlist[i].controls[3].width
                    + testlist[i].controls[4].width
                )
                testCon.data = lambda: i
                testConlist.append(testCon)

            # Columnを作成し、その中にheader_text、Divider、row1、row2、row3を追加
            self.control = ft.Column(
                controls=testConlist,
                spacing=0,  # Column内の要素間のスペース
                # horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Column内の要素を水平方向中央揃え
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
            )

        def on_child_click(page, e, parent_container: ft.Container, color: str):
            """
            子コントロールがクリックされた時のイベントハンドラ
            parent_container: 背景色を変更したい親コンテナのインスタンス
            color: 変更したい色
            """
            int1 = e.control.data
            for item in parent_container:
                item.bgcolor = ft.Colors.WHITE
            parent_container[int1].bgcolor = color
            # for item in parent_container:
            #    page.update()
            # parent_container[int1].update()
            page.update()

            # クリックされた子コントロールの背景も変える（オプション）
            e.control.content = ft.Text("赤に変える")
            e.control.update()

        def page_go(page, e, parent_container: ft.Container, color: str):
            int1 = e.control.data
            for item in parent_container:
                item.bgcolor = ft.Colors.WHITE
            parent_container[int1].bgcolor = color
            page.update()
            n = len(page.views) - 1
            page.views[n].data = int1

            page.go("/detail")
