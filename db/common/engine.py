from sqlalchemy import create_engine, inspect
from common.message_box import Message_Box
from sqlalchemy.orm import Session
from db.models import Log
from common.message import Message
from common.create_exception_log import Create_Exception_Log
from common.const import Const


# DB接続
class Engine:
    def __init__(self):
        self.engine = create_engine("sqlite:///db/example.db", echo=True)
        self.inspector = inspect(self.engine)
        # セッションクラス
        self.session = Session(self.engine)
        # ログクラス
        self.log_row = Log()
        # メッセージクラス
        self.message = Message()
        # 例外エラー出力クラス
        self.create_exception_log = Create_Exception_Log()
        # 定数クラス
        self.const = Const()

    # ログ追加
    # 【引数】
    #   arg_log_kinds：ログ種類,
    #   arg_function_id：処理ID,
    #   arg_log_detail：ログ詳細,
    #   arg_user_id：操作ユーザー
    def create_log(self, arg_log_kinds, arg_function_id, arg_log_detail, arg_user_id):
        # 引数を元にログクラスをインスタンス
        log = Log(
            log_kinds=arg_log_kinds,
            function_id=arg_function_id,
            log_detail=arg_log_detail,
            user_id=arg_user_id,
        )
        try:
            # インスタンスしたログをセッションに追加
            self.session.add(log)
            # データベースに反映
            self.session.commit()
        except Exception as e:
            isError = False
            # 例外エラーテキストファイルを出力
            isError = self.create_exception_log.create_exception_log(arg_function_id, e)
            return isError
        finally:
            # セッションを閉じる
            self.session.close()

    def exception_log(self, arg_log_function_id, arg_e, arg_entry_user_id):
        message_box = Message_Box()
        message_box.message_id = "HAB001W"
        message_box.message_text = self.message.Message_Box.HAB001W
        self.create_log(
            Const.Log_Kinds.WARNING,
            arg_log_function_id,
            repr(arg_e),
            arg_entry_user_id,
        )
        return message_box


# 返却用
class Return_Info:
    def __init__(self):
        self.return_row = None
        self.return_message_box = Message_Box()
