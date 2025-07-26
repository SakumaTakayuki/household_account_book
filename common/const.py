# 定数
class Const:
    # 初期管理者
    class Admin:
        USER_ID = "admin"
        NAME = "管理者"
        PASSWORD = "admin"

    # ログイン認証用ユーザー
    class Login:
        USER_ID = "login"

    # 共通部品用ユーザー
    class Common_Parts:
        USER_ID = "common_parts"

    # エラー区分
    class Log_Error_Kbn:
        LOGFILE_CREATE_ERROR = 8
        LOG_EXCEPTION_ERROR = 9

    # ファイルパス
    class FilePath:
        EXCEPTION_FOLDER = "log"
        EXCEPTION_FILE = "exception_log.txt"

    # ログ用種類
    class Log_Kinds:
        START = "S"
        END = "E"
        INFO = "I"
        CAUTION = "C"
        WARNING = "W"

    # ログ用処理
    class Log_Process:
        SELECT = "SEL"
        INSERT = "INS"
        UPDATE = "UPD"
        DELETE = "DEL"

    # ログ用機能
    class Log_Function:
        HAB_DETAIL = "HAB_DETAIL"
        USERS = "USERS"
        MASTER = "MASTER"
        SHOP_MASTER = "SHOP_MASTER"
        CSV_MASTER = "CSV_MASTER"

    # 文字
    class Const_Text:
        TEXT_BLANK = ""
        LIST = "一覧"
        ALL = "全件"
        DOUBLE_QUOTATION = '"'
        COMMA = ","
        ADDITION = "追加"

    # テーブル名
    class Table_Name:
        USERS = "users"
        MASTER = "master"
        HAB_DETAIL = "HAB_detail"
        SHOP_MASTER = "shop_master"
        CSV_MASTER = "CSV_master"

    # 取得区分
    class Fill_Kbn:
        FIRST = "1行目"
        LIST = "一覧"

    # 削除フラグ
    class Del_flg:
        NON_DELETE = "0"
        DELETE = "1"

    # 画面名
    class Display:
        LOGIN = "ログイン"
        HAB_LIST = "家計簿一覧"
        HAB_DETAIL = "家計簿詳細"
        BULK_REGISTRATION = "一括登録"
        MASTER_MENU = "マスタメニュー"
        SHOP_MASTER = "店舗マスタ"
        MASTER = "マスタ"
        CSV_MASTER = "CSVマスタ"
        USERS = "ユーザーマスタ"
        COMMON_PARTS = "共通部品"

    # マスタID
    class Master_ID:
        HAB_kbn = "HAB_kbn"
        HABkinds = "HABkinds"
        CSV_COMPANY = "CSV_company"

    # 入出金区分
    class HAB_kbn:
        kbn_in = "入金"
        kbn_out = "出金"

    # 入出金区分コード
    class HAB_kbn_code:
        kbn_in = "in"
        kbn_out = "out"

    # 詳細種類
    class HABkinds:
        food_expenses = "食費"
        salary = "給与"

    # 詳細種類コード
    class HABkinds_code:
        food_expenses = "01"
        salary = "02"
