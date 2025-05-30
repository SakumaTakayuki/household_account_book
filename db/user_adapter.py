from sqlalchemy import select
from db.models import User
from db.common.engine import Engine, Return_Info


# ユーザー情報テーブル接続
class User_Adapter(Engine):
    def __init__(self):
        super().__init__()
        self.user_row = User()

    # ユーザー情報取得
    def fill_user(self, arg_fill_kbn, arg_where_user_id, arg_fill_user_id):
        return_user = Return_Info()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
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
                stmt = select(User).where(User.user_id == arg_where_user_id)
            else:
                stmt = select(User)
            try:
                select_row = self.session.scalars(stmt).all()
                if len(select_row) == 0:
                    return_user.return_message_box.message_id = "HAB001C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB001C
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.Fill_NO_ROW.format(
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
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL.format(
                            self.const.Table_Name.USERS,
                            fill_kbn,
                            len(select_row),
                        ),
                        arg_fill_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    return_user.return_row = select_row
                    return return_user
            except Exception as e:
                return_user.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_fill_user_id
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
        if self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            str_log_detail,
            arg_user_row.entry_user_id,
        ):
            return_user.return_message_box = self.exception_log_exception()
            return return_user
        else:
            user = User(
                user_id=arg_user_row.user_id,
                name=arg_user_row.name,
                password=arg_user_row.password,
                entry_user_id=arg_user_row.entry_user_id,
            )
            stmt = select(User).where(User.user_id == arg_user_row.user_id)
            try:
                select_row = self.session.scalars(stmt).all()
                if len(select_row) == 0:
                    self.session.add(user)
                    self.session.commit()
                    return_user.return_message_box.message_id = "HAB001I"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB001I
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        str_log_detail,
                        arg_user_row.entry_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
                else:
                    return_user.return_message_box.message_id = "HAB002C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB002C
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_INSERT.format(
                            self.const.Table_Name.USERS, arg_user_row.user_id
                        ),
                        arg_user_row.entry_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
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
        if self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            str_log_detail,
            arg_user_row.update_user_id,
        ):
            return_user.return_message_box = self.exception_log_exception()
            return return_user
        else:
            stmt = select(User).where(
                User.user_id == arg_user_row.user_id,
                User.update_seq == arg_user_row.update_seq,
            )
            try:
                fill_user = self.session.scalars(stmt).first()
                if fill_user is not None:
                    fill_user.name = arg_user_row.name
                    fill_user.password = arg_user_row.password
                    fill_user.update_user_id = arg_user_row.update_user_id
                    fill_user.update_seq = fill_user.update_seq + 1
                    self.session.commit()
                    return_user.return_message_box.message_id = "HAB002I"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        str_log_detail,
                        arg_user_row.update_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
                else:
                    return_user.return_message_box.message_id = "HAB003C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.const.Table_Name.USERS, arg_user_row.user_id
                        ),
                        arg_user_row.update_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
            except Exception as e:
                return_user.return_message_box = self.exception_log()
                return return_user
            finally:
                self.session.close()

    # ユーザー情報削除
    def delete_user(self, arg_user_row: User):
        return_user = Return_Info()
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.USERS,
        )
        str_log_detail = self.message.Log_Message.DELETE.format(
            self.const.Table_Name.USERS, arg_user_row.user_id
        )
        if self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            str_log_detail,
            arg_user_row.update_user_id,
        ):
            return_user.return_message_box = self.exception_log_exception()
            return return_user
        else:
            stmt = select(User).where(
                User.user_id == arg_user_row.user_id,
                User.update_seq == arg_user_row.update_seq,
            )
            try:
                fill_user = self.session.scalars(stmt).first()
                if fill_user is not None:
                    fill_user.del_flg = self.const.Del_flg.DELETE
                    fill_user.update_user_id = arg_user_row.update_user_id
                    fill_user.update_seq = fill_user.update_seq + 1
                    self.session.commit()
                    return_user.return_message_box.message_id = "HAB003I"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        str_log_detail,
                        arg_user_row.update_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
                else:
                    return_user.return_message_box.message_id = "HAB003C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    if self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.const.Table_Name.USERS, arg_user_row.user_id
                        ),
                        arg_user_row.update_user_id,
                    ):
                        return_user.return_message_box = self.exception_log_exception()
                        return return_user
                    else:
                        return return_user
            except Exception as e:
                return_user.return_message_box = self.exception_log()
                return return_user
            finally:
                self.session.close()
