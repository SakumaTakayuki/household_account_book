from sqlalchemy import select
from db.models import HAB_Detail, Master, Shop_Master, CSV_Master
from db.common.engine import Engine, Return_Info


# 一括登録関連テーブル接続
class Bulk_Registration_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.BULK_REGISTRATION  # 一括登録

    # 店舗マスタ取得
    def fill_shop_master(self, arg_user_id):
        """
        店舗マスタを取得する
        """
        # 返却用クラスをインスタンス化
        return_shop_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.SHOP_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display_name,
                self.const.Table_Name.SHOP_MASTER,
                self.const.Const_Text.ALL,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_shop_master.return_message_box = error_message
            return return_shop_master
        else:
            try:
                # 店舗マスタを取得するSELECT文を作成する
                stmt = select(Shop_Master.name, Shop_Master.code)
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得した家計簿一覧を代入する
                return_shop_master.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.SHOP_MASTER,
                        self.const.Const_Text.ALL,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_shop_master.return_message_box = error_message
                    return return_shop_master
                else:
                    return return_shop_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_shop_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_shop_master
            finally:
                # セッションを閉じる
                self.session.close()

    # 詳細種類取得
    def fill_HABkinds(self, arg_user_id):
        """
        詳細種類を取得する
        """
        # 返却用クラスをインスタンス化
        return_shop_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display_name,
                self.const.Table_Name.MASTER,
                self.const.Master_ID.HABkinds,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_shop_master.return_message_box = error_message
            return return_shop_master
        else:
            try:
                # 詳細種類を取得するSELECT文を作成する
                stmt = select(Master.m_code, Master.m_text).where(
                    Master.m_id == self.const.Master_ID.HABkinds
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得した家計簿一覧を代入する
                return_shop_master.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.MASTER,
                        self.const.Master_ID.HABkinds,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_shop_master.return_message_box = error_message
                    return return_shop_master
                else:
                    return return_shop_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_shop_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_shop_master
            finally:
                # セッションを閉じる
                self.session.close()

    # CSV取込列マスタ取得
    def fill_CSV_master(self, arg_where_code, arg_user_id):
        """
        CSV取込列マスタを取得する
        """
        # 返却用クラスをインスタンス化
        return_CSV_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.CSV_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display_name,
                self.const.Table_Name.CSV_MASTER,
                arg_where_code,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_CSV_master.return_message_box = error_message
            return return_CSV_master
        else:
            try:
                # 店舗マスタを取得するSELECT文を作成する
                stmt = select(CSV_Master).where(CSV_Master.code == arg_where_code)
                # SELECT文を全件取得で実行する
                select_row = self.session.scalars(stmt).all()
                # 返却用の返却行に取得した家計簿一覧を代入する
                return_CSV_master.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.CSV_MASTER,
                        arg_where_code,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_CSV_master.return_message_box = error_message
                    return return_CSV_master
                else:
                    return return_CSV_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_CSV_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_CSV_master
            finally:
                # セッションを閉じる
                self.session.close()

    # 家計簿一括登録
    def bulk_registration_HAB_list(
        self, arg_HAB_ditail_list: HAB_Detail, arg_file_name, arg_user_id
    ):
        """
        家計簿を一括登録する
        引数
            arg_HAB_ditail_list：家計簿一覧
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_bulk_registration_HAB_list = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.HAB_DETAIL,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_file_name,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_bulk_registration_HAB_list.return_message_box = error_message
            return return_bulk_registration_HAB_list
        else:
            try:
                # 家計簿を登録する
                self.session.add_all(arg_HAB_ditail_list)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_bulk_registration_HAB_list.return_message_box.message_id = (
                    "HAB001I"
                )
                return_bulk_registration_HAB_list.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.HAB_DETAIL,
                        arg_file_name,
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_bulk_registration_HAB_list.return_message_box = error_message
                    return return_bulk_registration_HAB_list
                else:
                    return return_bulk_registration_HAB_list
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_bulk_registration_HAB_list.return_message_box = (
                    self.exception_log(str_log_function_id, e, arg_user_id)
                )
                return return_bulk_registration_HAB_list
            finally:
                # セッションを閉じる
                self.session.close()
