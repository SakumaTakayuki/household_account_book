from sqlalchemy import create_engine, inspect
<<<<<<< HEAD
from common.error_message import Error_Message
=======
>>>>>>> 1e9b8d9 (【engine】作成)
from sqlalchemy.orm import Session
from db.models import Log
from common.create_exception_log import Create_Exception_Log
<<<<<<< HEAD
=======
from common.const import Const
from common.message_box import Message_Box
>>>>>>> 1e9b8d9 (【engine】作成)


# DB接続
class Engine:
    def __init__(self):
        self.engine = create_engine("sqlite:///db/example.db", echo=True)
        self.inspector = inspect(self.engine)
        self.error_message = Error_Message()
        self.log_row = Log()
        self.create_exception_log = Create_Exception_Log()

<<<<<<< HEAD
    # ログ追加
    def create_log(self, arg_log_kinds, arg_function_id, arg_log_detail, arg_user_id):
        isError = False
=======
    # ログ作成
    # 【引数】
    #   arg_log_kinds：ログ種類,
    #   arg_log_function_id：処理ID,
    #   arg_log_detail：ログ詳細,
    #   arg_entry_user_id：操作ユーザー
    def create_log(
        self, arg_log_kinds, arg_log_function_id, arg_log_detail, arg_entry_user_id
    ):
        isError = False
        # 引数を元にログクラスをインスタンス
>>>>>>> 1e9b8d9 (【engine】作成)
        log = Log(
            log_kinds=arg_log_kinds,
            function_id=arg_log_function_id,
            log_detail=arg_log_detail,
            user_id=arg_entry_user_id,
        )
        try:
<<<<<<< HEAD
            with Session(self.engine) as session:
                session.add(log)
                session.commit()
        except Exception as e:
            # log出力
            isError = self.create_exception_log.create_exception_log(arg_function_id, e)
            return isError
        finally:
            session.close()
=======
            # インスタンスしたログをセッションに追加
            self.session.add(log)
            # データベースに反映
            self.session.commit()
            return isError
        except Exception as e:
            # 例外エラーテキストファイルを出力
            isError = self.create_exception_log.create_exception_log(
                arg_log_function_id, e
            )
            # 例外エラーテキストファイルを出力時に、例外エラーが発生したかを返す
            # 発生:True 未発生:False
            return isError
        finally:
            # セッションを閉じる
            self.session.close()

    # ログ出力時例外エラー用メッセージ作成
    def exception_log_exception(self):
        # メッセージボックスクラスをインスタンス
        message_box = Message_Box()
        # インスタンスしたメッセージボックスにidとメッセージを代入
        message_box.message_id = "HAB001W"
        message_box.message_text = self.message.Message_Box.HAB001W
        # インスタンスしたメッセージボックスを返す
        return message_box

    # Engineクラス継承クラス例外エラー用メッセージ作成、ログ作成
    #   arg_log_kinds：ログ種類,
    #   arg_log_function_id：処理ID,
    #   arg_log_detail：ログ詳細,
    #   arg_entry_user_id：操作ユーザー
    def exception_log(self, arg_log_function_id, arg_e, arg_entry_user_id):
        # メッセージボックスクラスをインスタンス
        message_box = Message_Box()
        # インスタンスしたメッセージボックスにidとメッセージを代入
        message_box.message_id = "HAB002W"
        message_box.message_text = self.message.Message_Box.HAB002W
        # ログ作成
        self.create_log(
            Const.Log_Kinds.WARNING,
            arg_log_function_id,
            repr(arg_e),
            arg_entry_user_id,
        )
        # インスタンスしたメッセージボックスを返す
        return message_box


# 返却用
class Return_Info:
    def __init__(self):
        # 取得した情報を代入する
        self.return_row = None
        # 画面のメッセージボックスに表示する情報を代入する
        self.return_message_box = Message_Box()
>>>>>>> 1e9b8d9 (【engine】作成)
