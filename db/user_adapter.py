from sqlalchemy import select
from sqlalchemy.orm import Session
from db.models import User
from db.common.engine import Engine
from common.message_box import Message_Box


# 返却用ユーザー情報
class Return_User:
    def __init__(self):
        self.return_user_row = None
        self.return_message_box = Message_Box()


# ユーザー情報テーブル接続
class User_Adapter(Engine):
    def __init__(self):
        super().__init__()
        self.user_row = User()

    # ユーザー情報追加
    def create_user(self, arg_user_row: User):
        user = User(
            user_id=arg_user_row.user_id,
            name=arg_user_row.name,
            password=arg_user_row.password,
            entry_user_id=arg_user_row.entry_user_id,
        )
        try:
            with Session(self.engine) as session:
                session.add(user)
                session.commit()
        except Exception as e:
            # log出力
            pass
        finally:
            session.close()

    # ユーザー情報取得
    def fill_user(self, arg_user_row: User):
        return_user = Return_User()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.USERS,
        )
        self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.const.Table_Name.USERS,
                arg_user_row.user_id,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_row.entry_user_id,
        )
        stmt = select(User).where(User.user_id == arg_user_row.user_id)
        try:
            with Session(self.engine) as session:
                return_user.return_user_row = session.scalars(stmt).all()
            if len(return_user.return_user_row) == 0:
                return_user.return_message_box.message_id = "HAB001I"
                return_user.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.Fill_NO_ROW.format(
                        self.const.Table_Name.USERS,
                        arg_user_row.user_id,
                    ),
                    arg_user_row.entry_user_id,
                )
                return return_user
            self.create_log(
                self.const.Log_Kinds.END,
                str_log_function_id,
                self.message.Log_Message.FILL.format(
                    self.const.Table_Name.USERS,
                    arg_user_row.user_id,
                    len(return_user.return_user_row),
                ),
                arg_user_row.entry_user_id,
            )
            return return_user
        except Exception as e:
            return_user.return_message_box = self.exception_log(
                str_log_function_id, e, arg_user_row.entry_user_id
            )
            return return_user
        finally:
            session.close()

    # ユーザー情報更新
    def update_user(self, arg_user_row: User):
        return_user = Return_User()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.USERS,
        )
        str_log_detail = self.message.Log_Message.UPDATE.format(
            self.const.Table_Name.USERS, arg_user_row.user_id
        )
        self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            str_log_detail,
            arg_user_row.entry_user_id,
        )
        stmt = select(User).where(
            User.user_id == arg_user_row.user_id,
            User.update_at == arg_user_row.update_at,
        )
        try:
            with Session(self.engine) as session:
                fill_user = session.scalars(stmt).first()
                if fill_user is not None:
                    fill_user.name = arg_user_row.name
                    fill_user.password = arg_user_row.password
                    fill_user.update_user_id = arg_user_row.update_user_id
                    session.commit()
                    return_user.return_message_box.message_id = "HAB003I"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        str_log_detail,
                        arg_user_row.entry_user_id,
                    )
                    return return_user
                else:
                    return_user.return_message_box.message_id = "HAB004I"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB004I
                    )
                    self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.const.Table_Name.USERS, arg_user_row.user_id
                        ),
                        arg_user_row.entry_user_id,
                    )
                    return return_user
        except Exception as e:
            return_user.return_message_box = self.exception_log()
            return return_user
        finally:
            session.close()
