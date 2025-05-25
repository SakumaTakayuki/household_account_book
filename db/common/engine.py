from sqlalchemy import create_engine, inspect
from common.error_message import Error_Message
from sqlalchemy.orm import Session
from db.models import Log
from common.create_exception_log import Create_Exception_Log


# DB接続
class Engine:
    def __init__(self):
        self.engine = create_engine("sqlite:///db/example.db", echo=True)
        self.inspector = inspect(self.engine)
        self.error_message = Error_Message()
        self.log_row = Log()
        self.create_exception_log = Create_Exception_Log()

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
            # log出力
            isError = self.create_exception_log.create_exception_log(arg_function_id, e)
            return isError
        finally:
            session.close()
