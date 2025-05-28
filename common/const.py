# 定数
class Const:
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
