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
<<<<<<< HEAD
        self.error_message = Error_Message()
=======
        # セッションクラス
        self.session = Session(self.engine, expire_on_commit=False)
        # ログクラス
>>>>>>> 65862d6 (【Engine】SessionのOPにexpire_on_commit=False追加)
        self.log_row = Log()
        self.create_exception_log = Create_Exception_Log()

<<<<<<< HEAD
    # ログ追加
    def create_log(self, arg_log_kinds, arg_function_id, arg_log_detail, arg_user_id):
        isError = False
=======
    # ログ作成
    def create_log(
        self, arg_log_kinds, arg_log_function_id, arg_log_detail, arg_entry_user_id
    ):
        """
        ログを作成する
        引数
            arg_log_kinds：ログ種類,
            arg_log_function_id：処理ID,
            arg_log_detail：ログ詳細,
            arg_entry_user_id：操作ユーザー
        """
        error_message = None
        # 引数を元にログクラスをインスタンス
<<<<<<< HEAD
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
=======
        try:
            log = Log(
                log_kinds=arg_log_kinds,
                function_id=arg_log_function_id,
                log_detail=arg_log_detail,
                user_id=arg_entry_user_id,
            )
>>>>>>> 0d7bd94 (【Engine】ログ出力周りの修正)
            # インスタンスしたログをセッションに追加
            self.session.add(log)
            # データベースに反映
            self.session.commit()
            return error_message
        except Exception as e:
            # 例外エラーテキストファイルを出力
            isError = self.create_exception_log.create_exception_log(
                arg_log_function_id, e
            )
            if isError == self.const.Log_Error_Kbn.LOGFILE_CREATE_ERROR:
                # 例外エラーテキストファイルを出力失敗時、エラー
                error_message = self.exception_log_exception()
            elif isError == self.const.Log_Error_Kbn.LOG_EXCEPTION_ERROR:
                # 例外エラーテキストファイルを出力成功時、エラー
                error_message = Message_Box()
                # インスタンスしたメッセージボックスにidとメッセージを代入
                error_message.message_id = "HAB002W"
                error_message.message_text = self.message.Message_Box.HAB002W
            # 例外エラーメッセージを返す
            return error_message
        finally:
            # セッションを閉じる
            self.session.close()

    # ログ出力時例外エラー用メッセージ作成
    def exception_log_exception(self):
        """
        ログ出力時の例外エラー用メッセージを作成する
        """
        # メッセージボックスクラスをインスタンス
        message_box = Message_Box()
        # インスタンスしたメッセージボックスにidとメッセージを代入
        message_box.message_id = "HAB001W"
        message_box.message_text = self.message.Message_Box.HAB001W
        # インスタンスしたメッセージボックスを返す
        return message_box

    # 例外エラー用メッセージ作成、ログ作成
    def exception_log(self, arg_log_function_id, arg_e, arg_entry_user_id):
        """
        例外エラー用メッセージ作成、ログ作成
        引数
            arg_log_kinds：ログ種類,
            arg_log_function_id：処理ID,
            arg_log_detail：ログ詳細,
            arg_entry_user_id：操作ユーザー
        """
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
