from sqlalchemy import select
from db.models import User
from db.common.engine import Engine, Return_Info

# インデント修正 if else
# ログ出力exeption時の処理記載


# ユーザー情報テーブル接続
class User_Adapter(Engine):
    def __init__(self):
        super().__init__()
        self.user_row = User()

    # ユーザー情報取得
    def fill_user(self, arg_user_row: User):
        return_user = Return_Info()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.USERS,
        )
        if self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.const.Table_Name.USERS,
                arg_user_row.user_id,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_row.entry_user_id,
        ):
            return_user.return_message_box.message_id = "HAB002W"
            return_user.return_message_box.message_text = (
                self.message.Message_Box.HAB002W
            )
            return return_user
        else:
            stmt = select(User).where(User.user_id == arg_user_row.user_id)
            try:
                return_user.return_row = self.session.scalars(stmt).all()
                if len(return_user.return_row) == 0:
                    return_user.return_message_box.message_id = "HAB001C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB001C
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.Fill_NO_ROW.format(
                            self.const.Table_Name.USERS,
                            arg_user_row.user_id,
                        ),
                        arg_user_row.entry_user_id,
                    ):
                        return_user.return_message_box.message_id = "HAB002W"
                        return_user.return_message_box.message_text = (
                            self.message.Message_Box.HAB002W
                        )
                        return return_user
                    else:
                        return return_user
                else:
                    self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL.format(
                            self.const.Table_Name.USERS,
                            arg_user_row.user_id,
                            len(return_user.return_row),
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
                self.session.close()

    # ユーザー情報追加
    def create_user(self, arg_user_row: User):
        return_user = Return_Info()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.USERS,
        )
        str_log_detail = self.message.Log_Message.INSERT.format(
            self.const.Table_Name.USERS, arg_user_row.user_id
        )
        self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            str_log_detail,
            arg_user_row.entry_user_id,
        )
        user = User(
            user_id=arg_user_row.user_id,
            name=arg_user_row.name,
            password=arg_user_row.password,
            entry_user_id=arg_user_row.entry_user_id,
        )
        stmt = select(User).where(User.user_id == arg_user_row.user_id)
        try:
            return_user.return_row = self.session.scalars(stmt).all()
            if len(return_user.return_row) == 0:
                self.session.add(user)
                self.session.commit()
                return_user.return_message_box.message_id = "HAB001I"
                return_user.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    str_log_detail,
                    arg_user_row.entry_user_id,
                )
                return return_user
            else:
                return_user.return_message_box.message_id = "HAB002C"
                return_user.return_message_box.message_text = (
                    self.message.Message_Box.HAB002C
                )
                self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    str_log_detail,
                    arg_user_row.entry_user_id,
                )
                return return_user
        except Exception as e:
            return_user.return_message_box = self.exception_log(
                str_log_function_id, e, arg_user_row.entry_user_id
            )
            return return_user
        finally:
            self.session.close()

    # ユーザー情報更新
    def update_user(self, arg_user_row: User):
        return_user = Return_Info()
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
            fill_user = self.session.scalars(stmt).first()
            if fill_user is not None:
                fill_user.name = arg_user_row.name
                fill_user.password = arg_user_row.password
                fill_user.update_user_id = arg_user_row.update_user_id
                self.session.commit()
                return_user.return_message_box.message_id = "HAB002I"
                return_user.return_message_box.message_text = (
                    self.message.Message_Box.HAB002I
                )
                self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    str_log_detail,
                    arg_user_row.entry_user_id,
                )
                return return_user
            else:
                return_user.return_message_box.message_id = "HAB003C"
                return_user.return_message_box.message_text = (
                    self.message.Message_Box.HAB003C
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
            self.session.close()
