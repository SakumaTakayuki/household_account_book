from sqlalchemy import select
from db.models import User
from db.common.engine import Engine, Return_Info


# ログイン用ユーザー情報テーブル接続
class Login_Adapter(Engine):
    def __init__(self):
        super().__init__()
        self.user_row = User()
        self.display = self.const.display.LOGIN

    # ログイン認証
    def login(self, arg_fill_kbn, arg_where_user_id, arg_password, arg_fill_user_id):
        return_user = Return_Info()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.USERS,
        )
        if arg_fill_kbn == self.const.Fill_Kbn.FIRST:
            fill_kbn = arg_where_user_id
        else:
            fill_kbn = self.const.Const_Text.LIST
        if self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display,
                self.const.Table_Name.USERS,
                fill_kbn,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_fill_user_id,
        ):
            return_user.return_message_box = self.exception_log_exception()
            return return_user
        else:
            if arg_fill_kbn == self.const.Fill_Kbn.FIRST:
                stmt = select(User).where(
                    User.user_id == arg_where_user_id, User.password == arg_password
                )
            else:
                stmt = select(User)
            try:
                select_row = self.session.scalars(stmt).all()
                if len(select_row) == 0:
                    return_user.return_message_box.message_id = "HAB004C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB004C.format(
                            self.const.display.LOGIN
                        )
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.Fill_NO_ROW.format(
                            self.display,
                            self.const.Table_Name.USERS,
                            fill_kbn,
                        ),
                        arg_fill_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
                else:
                    return_user.return_row = select_row
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL.format(
                            self.display,
                            self.const.Table_Name.USERS,
                            fill_kbn,
                            len(select_row),
                        ),
                        arg_fill_user_id,
                    ):
                        return_user.return_row = None
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    return return_user
            except Exception as e:
                return_user.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_fill_user_id
                )
                return return_user
            finally:
                self.session.close()
