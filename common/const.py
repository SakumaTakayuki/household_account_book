# 定数
class Const:
<<<<<<< HEAD
=======
    # 初期管理者
    class Admin:
        USER_ID = "admin"
        NAME = "管理者"
        PASSWORD = "admin"

    # ログイン認証用ユーザー
    class Login:
        USER_ID = "login"
        NAME = "ログイン"
        PASSWORD = "login"

<<<<<<< HEAD
>>>>>>> a777732 (【const】画面名、ログイン時システムユーザー追加)
=======
    # エラー区分
    class Log_Error_Kbn:
        LOGFILE_CREATE_ERROR = 8
        LOG_EXCEPTION_ERROR = 9

>>>>>>> 0d7bd94 (【Engine】ログ出力周りの修正)
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
        HAB = "HAB"
        USERS = "USERS"

    # 文字
    class Const_Text:
        TEXT_BLANK = ""
<<<<<<< HEAD
=======
        LIST = "一覧"

    # テーブル名
    class Table_Name:
        USERS = "users"

    # 取得区分
    class Fill_Kbn:
        FIRST = "1行目"
        LIST = "一覧"

    # 削除フラグ
    class Del_flg:
        NON_DELETE = "0"
        DELETE = "1"

    # 画面名
    class display:
        LOGIN = "ログイン"
        USER_MASTER = "ユーザーマスタ"
>>>>>>> a777732 (【const】画面名、ログイン時システムユーザー追加)
