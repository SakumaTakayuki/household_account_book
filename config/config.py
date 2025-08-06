import flet as ft
import configparser
import json


class Config:
    def __init__(self):
        self.datetime_dropdown = datetime_dropdown()
        self.HAB_list_column_name = HAB_list_column_name()
        self.shop_master_column_name = shop_master_column_name()
        self.master_column_name = master_column_name()
        self.CSV_master_column_name = CSV_master_column_name()
        self.users_column_name = users_column_name()

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
            width = 1085
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


class Config_Read:
    def __init__(self):
        self.config_ini = configparser.ConfigParser()
        self.config_ini.read("config/config.ini", encoding="utf-8")


class datetime_dropdown(Config_Read):
    def __init__(self):
        super().__init__()
        self.start_year = self.config_ini.get("Datetime_Dropdown", "start_year")
        self.end_year = self.config_ini.get("Datetime_Dropdown", "end_year")


class HAB_list_column_name(Config_Read):
    def __init__(self):
        super().__init__()
        self.column_name = json.loads(
            self.config_ini.get("HAB_list_column_name", "column_name")
        )


class shop_master_column_name(Config_Read):
    def __init__(self):
        super().__init__()
        self.column_name = json.loads(
            self.config_ini.get("shop_master_column_name", "column_name")
        )


class master_column_name(Config_Read):
    def __init__(self):
        super().__init__()
        self.column_name = json.loads(
            self.config_ini.get("master_column_name", "column_name")
        )


class CSV_master_column_name(Config_Read):
    def __init__(self):
        super().__init__()
        self.column_name = json.loads(
            self.config_ini.get("CSV_master_column_name", "column_name")
        )


class users_column_name(Config_Read):
    def __init__(self):
        super().__init__()
        self.column_name = json.loads(
            self.config_ini.get("users_column_name", "column_name")
        )
