from sqlalchemy import select, case
from db.models import User
from db.common.engine import Engine, Return_Info
from werkzeug.security import generate_password_hash


# ユーザーマスタテーブル接続
class Users_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.USERS  # ユーザーマスタ

    # ユーザーマスタ取得
    def fill_users(self, arg_user_id):
        """
        ユーザーマスタを取得する
        """
        # 返却用クラスをインスタンス化
        return_users = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.USERS,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display_name,
                self.const.Table_Name.USERS,
                self.const.Const_Text.ALL,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            return
        else:
            try:
                # ユーザーマスタを取得するSELECT文を作成
                stmt = (
                    select(
                        User.user_id,
                        User.name,
                        case(
                            (User.del_flg == 1, "削除"),
                            else_="",
                        ).label("del_flg"),
                        User.update_version,
                    ).select_from(User)
                    # 並び順を設定する
                    .order_by(
                        User.user_id,
                    )
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得したユーザーマスタを代入する
                return_users.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.USERS,
                        self.const.Const_Text.ALL,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_users
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(str_log_function_id, e, arg_user_id)
                return
            finally:
                # セッションを閉じる
                self.session.close()

    # ユーザーマスタ登録
    def create_users(self, arg_users_row: User, arg_user_id):
        """
        ユーザーマスタを登録する
        引数
            arg_users_row：ユーザーマスタ追加行
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_users = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.USERS,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.USERS,
                arg_users_row.user_id,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_users.return_message_box = error_message
            return return_users
        else:
            try:
                # パスワードを暗号化する
                arg_users_row.password = generate_password_hash(
                    password=arg_users_row.password, method="pbkdf2:sha256"
                )
                # ユーザーマスタを登録する
                self.session.add(arg_users_row)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_users.return_message_box.message_id = "HAB001I"
                return_users.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.USERS,
                        arg_users_row.user_id,
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_users.return_message_box = error_message
                    return return_users
                else:
                    return return_users
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_users.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_users
            finally:
                # セッションを閉じる
                self.session.close()

    # ユーザーマスタ更新
    def update_users(self, arg_users_row: User):
        """
        ユーザーマスタを更新する
        引数
            arg_users_row：ユーザーマスタ
        """
        # 返却用クラスをインスタンス化
        return_users = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.USERS,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.UPDATE.format(
                self.display_name,
                self.const.Table_Name.USERS,
                arg_users_row.user_id,
            ),
            arg_users_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_users.return_message_box = error_message
            return return_users
        else:
            try:
                # ユーザーマスタを取得するSELECT文を作成する
                stmt = select(User).where(
                    User.user_id == arg_users_row.user_id,
                    User.update_version == arg_users_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_users = self.session.scalars(stmt).all()
                if len(fill_users) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_users.return_message_box.message_id = "HAB003C"
                    return_users.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.USERS,
                            arg_users_row.user_id,
                        ),
                        arg_users_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_users.return_message_box = error_message
                        return return_users
                    else:
                        return return_users
                else:
                    # ユーザーマスタを登録する
                    fill_users[0].user_id = arg_users_row.user_id
                    fill_users[0].name = arg_users_row.name
                    # パスワードを暗号化する
                    fill_users[0].password = generate_password_hash(
                        password=arg_users_row.password, method="pbkdf2:sha256"
                    )
                    fill_users[0].del_flg = arg_users_row.del_flg
                    fill_users[0].update_user_id = arg_users_row.update_user_id
                    fill_users[0].update_version = int(arg_users_row.update_version) + 1
                    self.session.add(fill_users[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_users.return_message_box.message_id = "HAB002I"
                    return_users.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.USERS,
                            arg_users_row.user_id,
                        ),
                        arg_users_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_users.return_message_box = error_message
                        return return_users
                    else:
                        return return_users
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_users.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_users_row.update_user_id
                )
                return return_users
            finally:
                # セッションを閉じる
                self.session.close()

    # ユーザーマスタ削除
    def delete_users(self, arg_users_row: User):
        """
        ユーザーマスタを削除する
        引数
            arg_users_row：ユーザーマスタ
        """
        # 返却用クラスをインスタンス化
        return_users = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.USERS,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.DELETE.format(
                self.display_name,
                self.const.Table_Name.USERS,
                arg_users_row.user_id,
            ),
            arg_users_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_users.return_message_box = error_message
            return return_users
        else:
            try:
                # ユーザーマスタを取得するSELECT文を作成する
                stmt = select(User).where(
                    User.user_id == arg_users_row.user_id,
                    User.update_version == arg_users_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_users = self.session.scalars(stmt).all()
                if len(fill_users) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_users.return_message_box.message_id = "HAB003C"
                    return_users.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_DELETE.format(
                            self.display_name,
                            self.const.Table_Name.USERS,
                            arg_users_row.user_id,
                        ),
                        arg_users_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_users.return_message_box = error_message
                        return return_users
                    else:
                        return return_users
                else:
                    # ユーザーマスタを登録する
                    fill_users[0].del_flg = self.const.Del_flg.DELETE
                    fill_users[0].update_user_id = arg_users_row.update_user_id
                    fill_users[0].update_version = int(arg_users_row.update_version) + 1
                    self.session.add(fill_users[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_users.return_message_box.message_id = "HAB003I"
                    return_users.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.DELETE.format(
                            self.display_name,
                            self.const.Table_Name.USERS,
                            arg_users_row.user_id,
                        ),
                        arg_users_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_users.return_message_box = error_message
                        return return_users
                    else:
                        return return_users
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_users.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_users_row.update_user_id
                )
                return return_users
            finally:
                # セッションを閉じる
                self.session.close()
