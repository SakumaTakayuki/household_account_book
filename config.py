# config
import flet as ft


class Config:
    class Datetime_Dropdown:
        start_year = 2000
        end_year = 2050

    class HAB_list_column_name:
        column_name = [
            "利用日時",
            "入出金区分",
            "金額",
            "詳細種類",
            "家計簿詳細",
        ]

    class shop_master_column_name:
        column_name = [
            "No",
            "詳細種類",
            "店舗名",
            "削除",
        ]

    class master_column_name:
        column_name = [
            "ID",
            "コード",
            "名称",
            "削除",
        ]

    class CSV_master_column_name:
        column_name = [
            "コード",
            "利用日時",
            "金額",
            "家計簿詳細",
            "文字コード",
            "削除",
        ]

    class users_column_name:
        column_name = [
            "ユーザーID",
            "名前",
            "削除",
        ]

    class my_pieChart_colors:
        HAB_kbn_colors = [
            ft.Colors.GREEN_500,
            ft.Colors.RED_500,
        ]

        HABkinds_colors = [
            ft.Colors.GREEN_500,
            ft.Colors.RED_500,
            ft.Colors.YELLOW_500,
            ft.Colors.BLUE_500,
            ft.Colors.GREEN_500,
            ft.Colors.RED_500,
            ft.Colors.YELLOW_500,
            ft.Colors.BLUE_500,
        ]

    class window_size:
        class login:
            width = 505
            height = 320

        class HAB_list:
            width = 1875
            height = 1005

        class HAB_detail:
            width = 1125
            height = 435

        class bulk_registration:
            width = 1125
            height = 720

        class master_menu:
            width = 1085
            height = 400

        class CSV_master:
            width = 1290
            height = 950

        class master:
            width = 890
            height = 880

        class shop_master:
            width = 890
            height = 880

        class users:
            width = 690
            height = 885
