class Const:
    """
    定数
    """

    class Admin:
        """
        初期管理者
        """

        USER_ID = "admin"
        NAME = "管理者"
        PASSWORD = "admin"

    class Login:
        """
        ログイン認証用ユーザー
        """

        USER_ID = "login"

    class Common_Parts:
        """
        共通部品用ユーザー
        """

        USER_ID = "common_parts"

    class Log_Error_Kbn:
        """
        エラー区分
        """

        LOGFILE_CREATE_ERROR = 8
        LOG_EXCEPTION_ERROR = 9

    class FilePath:
        """
        ファイルパス
        """

        EXCEPTION_FOLDER = "log"
        EXCEPTION_FILE = "exception_log.txt"

    class Log_Kinds:
        """
        ログ用種類
        """

        START = "S"
        END = "E"
        INFO = "I"
        CAUTION = "C"
        WARNING = "W"

    class Log_Process:
        """
        ログ用処理
        """

        SELECT = "SEL"
        INSERT = "INS"
        UPDATE = "UPD"
        DELETE = "DEL"

    class Log_Function:
        """
        ログ用機能
        """

        HAB_DETAIL = "HAB_DETAIL"
        USERS = "USERS"
        MASTER = "MASTER"
        SHOP_MASTER = "SHOP_MASTER"
        CSV_MASTER = "CSV_MASTER"

    class Const_Text:
        """
        文字
        """

        TEXT_BLANK = ""
        LIST = "一覧"
        ALL = "全件"
        DOUBLE_QUOTATION = '"'
        COMMA = ","
        ADDITION = "追加"

    class Table_Name:
        """
        テーブル名
        """

        USERS = "users"
        MASTER = "master"
        HAB_DETAIL = "HAB_detail"
        SHOP_MASTER = "shop_master"
        CSV_MASTER = "CSV_master"

    class Fill_Kbn:
        """
        取得区分
        """

        FIRST = "1行目"
        LIST = "一覧"

    class Del_flg:
        """
        削除フラグ
        """

        NON_DELETE = "0"
        DELETE = "1"

    class Display:
        """
        画面名
        """

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

    class Master_ID:
        """
        マスタID
        """

        HAB_kbn = "HAB_kbn"
        HABkinds = "HABkinds"
        CSV_COMPANY = "CSV_company"

    class HAB_kbn:
        """
        入出金区分
        """

        kbn_in = "入金"
        kbn_out = "出金"

    class HAB_kbn_code:
        """
        入出金区分コード
        """

        kbn_in = "in"
        kbn_out = "out"

    class HABkinds:
        """
        詳細種類
        """

        food_expenses = "食費"
        salary = "給与"

    class HABkinds_code:
        """
        詳細種類コード
        """

        food_expenses = "01"
        salary = "02"
