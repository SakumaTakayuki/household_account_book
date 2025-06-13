from sqlalchemy import select
from db.models import User
from db.common.engine import Engine, Return_Info
from werkzeug.security import check_password_hash


# ログイン用ユーザー情報テーブル接続
class Login_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.display.LOGIN  # ログイン

    # ログイン認証
    def login(self, arg_where_user_id, arg_password):
        """
        ログイン認証を実行する
        引数
            arg_where_user_id：検索条件
            arg_password：パスワード
        """
        # 返却用クラスをインスタンス化
        return_user = Return_Info()
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
            self.message.Log_Message.LOGIN.format(
                arg_where_user_id,
                self.const.Const_Text.TEXT_BLANK,
            ),
            self.const.Login.USER_ID,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_user.return_message_box = error_message
            return return_user
        else:
            try:
                # ユーザー情報を取得するSELECT文を作成
                # Where句に引数の検索条件を設定する
                stmt = select(User).where(User.user_id == arg_where_user_id)
                # SELECT文を全件取得で実行する
                select_row = self.session.scalars(stmt).all()
                # 取得結果：select_rowが0件の場合
                if len(select_row) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_user.return_message_box.message_id = "HAB004C"
                    return_user.return_message_box.message_text = (
                        self.message.Message_Box.HAB004C.format(
                            self.const.display.LOGIN
                        )
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.LOGIN_ERROR.format(
                            arg_where_user_id,
                            len(select_row),
                        ),
                        self.const.Login.USER_ID,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_user.return_message_box = error_message
                        return return_user
                    else:
                        return return_user
                else:
                    # 取得したユーザー情報のハッシュ化されたパスワードと引数パスワードが一致する場合
                    if check_password_hash(select_row[0].password, arg_password):
                        # 返却用の返却行に取得したユーザー情報を代入する
                        return_user.return_row = select_row
                        # ENDログ出力
                        error_message = self.create_log(
                            self.const.Log_Kinds.END,
                            str_log_function_id,
                            self.message.Log_Message.LOGIN_SUCCESS.format(
                                arg_where_user_id,
                                len(select_row),
                            ),
                            self.const.Login.USER_ID,
                        )
                        # ENDログ出力失敗の場合
                        if error_message != None:
                            # 返却用のメッセージボックスに例外エラーメッセージを代入する
                            return_user.return_message_box = error_message
                            return return_user
                        else:
                            return return_user
                    else:
                        # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                        return_user.return_message_box.message_id = "HAB004C"
                        return_user.return_message_box.message_text = (
                            self.message.Message_Box.HAB004C.format(
                                self.const.display.LOGIN
                            )
                        )
                        # ENDログ出力
                        error_message = self.create_log(
                            self.const.Log_Kinds.END,
                            str_log_function_id,
                            self.message.Log_Message.LOGIN_ERROR.format(
                                arg_where_user_id,
                                len(select_row),
                            ),
                            self.const.Login.USER_ID,
                        )
                        # ENDログ出力失敗の場合
                        if error_message != None:
                            # 返却用のメッセージボックスに例外エラーメッセージを代入する
                            return_user.return_message_box = error_message
                            return return_user
                        else:
                            return return_user
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_user.return_message_box = self.exception_log(
                    str_log_function_id, e, self.const.Login.USER_ID
                )
                return return_user
            finally:
                # セッションを閉じる
                self.session.close()
