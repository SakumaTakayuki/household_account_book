import flet as ft


class My_testtable(ft.Control):
    def __init__(
        self,
        testpage,
        ref=None,
        expand=None,
        expand_loose=None,
        col=None,
        opacity=None,
        tooltip=None,
        badge=None,
        visible=None,
        disabled=None,
        data=None,
        rtl=None,
    ):
        super().__init__(
            ref,
            expand,
            expand_loose,
            col,
            opacity,
            tooltip,
            badge,
            visible,
            disabled,
            data,
            rtl,
        )
        self.page = testpage
        self.control = None
        # Columnに直接追加されるテキスト
        header_text = ft.Text(
            "以下は複数の行で構成されるセクションです。",
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        row_button_width = 50
        row_button_height = 50
        row_width = 100
        row_height = 50
        # 行作成
        testlist = []
        topfirst_row_border_config = ft.border.all(1.0, ft.Colors.BLACK)
        topinside_row_border_config = ft.border.only(
            top=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
        )
        insidefirst_row_border_config = ft.border.only(
            left=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
        )
        insideinside_row_border_config = ft.border.only(
            right=ft.border.BorderSide(1.0, ft.Colors.BLACK),
            bottom=ft.border.BorderSide(1.0, ft.Colors.BLACK),
        )
        row_count = 10
        for i in range(0, row_count):
            if i == 0:
                first_column_border_config = topfirst_row_border_config
                inside_column_border_config = topinside_row_border_config
            else:
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
                            on_click=lambda e: My_testtable.page_go(
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
                        on_click=lambda e: My_testtable.on_child_click(
                            self.page,
                            e,
                            testlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
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
                        on_click=lambda e: My_testtable.on_child_click(
                            self.page,
                            e,
                            testConlist,
                            ft.Colors.RED_ACCENT_100,
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(f"testC{i}"),
                        width=100,
                        height=50,
                        padding=10,
                        bgcolor=ft.Colors.with_opacity(
                            0.0, ft.Colors.PRIMARY_CONTAINER
                        ),
                        border=inside_column_border_config,
                        data=i,
                        on_click=lambda e: My_testtable.on_child_click(
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
        # 作成行をコンテナに入れる
        for i in range(0, row_count):
            testCon = ft.Container()
            testCon.content = testlist[i]
            testCon.width = (
                testlist[i].controls[0].width
                + testlist[i].controls[1].width
                + testlist[i].controls[2].width
            )
            testCon.data = lambda: i
            testConlist.append(testCon)

        # Columnを作成し、その中にheader_text、Divider、row1、row2、row3を追加
        self.control = ft.Column(
            controls=testConlist,
            spacing=0,  # Column内の要素間のスペース
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Column内の要素を水平方向中央揃え
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
        # for item in parent_container:
        #    page.update()
        # parent_container[int1].update()
        page.update()

        page.go("/view2")


def main(page: ft.Page):
    my_column = My_testtable(page)

    def create_view1():
        return ft.View(
            "/view1",
            [
                ft.AppBar(title=ft.Text("View 1")),
                my_column.control,
            ],
        )

    def create_view2(i):
        return ft.View(
            "/view2",
            [
                ft.AppBar(title=ft.Text(f"View 2：{i}")),
                ft.ElevatedButton("Go to View 1", on_click=lambda _: page.go("/view1")),
            ],
        )

    def route_change(handler):
        if handler.route == "/view1":
            page.views.append(create_view1())
        elif handler.route == "/view2":
            page.views.append(create_view2())
        page.update()

    page.title = "複数RowをColumnに追加"
    page.vertical_alignment = ft.CrossAxisAlignment.START  # 上寄せ

    page.on_route_change = route_change
    page.go("/view1")  # 初期表示としてView1を設定

    # page.add(my_column.control)  # ページにColumnを追加


if __name__ == "__main__":
    ft.app(target=main)
