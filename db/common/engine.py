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
        self.log_row = Log()
        self.message = Message()
        self.create_exception_log = Create_Exception_Log()
        self.const = Const()

    # ログ追加
    def create_log(self, arg_log_kinds, arg_function_id, arg_log_detail, arg_user_id):
        isError = False
        log = Log(
            log_kinds=arg_log_kinds,
            function_id=arg_function_id,
            log_detail=arg_log_detail,
            user_id=arg_user_id,
        )
        try:
            with Session(self.engine) as session:
                session.add(log)
                session.commit()
        except Exception as e:
            isError = self.create_exception_log.create_exception_log(arg_function_id, e)
            return isError
        finally:
            session.close()

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
