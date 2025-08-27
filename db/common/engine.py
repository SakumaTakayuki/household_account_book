from sqlalchemy import create_engine, inspect
from common.error_message import Error_Message
from sqlalchemy.orm import Session
from db.models import Log
from common.message import Message
from common.create_exception_log import Create_Exception_Log
from common.const import Const
from common.message_box import Message_Box
from sqlalchemy import create_engine
import logging

# DB接続
class Engine:
    def __init__(self):
        # logger = logging.getLogger("sqlalchemy.engine")
        # logger.setLevel(logging.INFO)
        # handler = logging.FileHandler(filename="sqlalchemy.log", encoding="utf-8")
        # formatter = logging.Formatter(
        #    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        # )
        # handler.setFormatter(formatter)
        # logger.addHandler(handler)
        self.engine = create_engine(
            "sqlite:///db/household_account_book.db", echo=False
        )
        self.inspector = inspect(self.engine)
        # セッションクラス
        self.session = Session(self.engine, expire_on_commit=False)
        # ログクラス
        self.log_row = Log()
        # メッセージクラス
        self.message = Message()
        # 例外エラー出力クラス
        self.create_exception_log = Create_Exception_Log()
        # 定数クラス
        self.const = Const()

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
        try:
            log = Log(
                log_kinds=arg_log_kinds,
                function_id=arg_log_function_id,
                log_detail=arg_log_detail,
                user_id=arg_entry_user_id,
            )
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
