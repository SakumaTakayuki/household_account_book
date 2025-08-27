from sqlalchemy import select, case
from db.models import CSV_Master
from db.common.engine import Engine, Return_Info


# CSVマスタテーブル接続
class CSV_Master_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.CSV_MASTER  # CSVマスタ

    # CSVマスタ取得
    def fill_CSV_master(self, arg_user_id):
        """
        CSVマスタを取得する
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
                # CSVマスタを取得するSELECT文を作成
                stmt = (
                    select(
                        CSV_Master.code,
                        CSV_Master.HAB_at_text,
                        CSV_Master.amount_text,
                        CSV_Master.HABdetail_text,
                        CSV_Master.character_code,
                        case(
                            (CSV_Master.del_flg == 1, "削除"),
                            else_="",
                        ).label("del_flg"),
                        CSV_Master.update_version,
                    ).select_from(CSV_Master)
                    # 並び順を設定する
                    .order_by(
                        CSV_Master.code,
                    )
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得したCSVマスタを代入する
                return_CSV_master.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.CSV_MASTER,
                        self.const.Const_Text.ALL,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_CSV_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(str_log_function_id, e, arg_user_id)
                return
            finally:
                # セッションを閉じる
                self.session.close()

    # CSVマスタ登録
    def create_CSV_master(self, arg_CSV_master_row: CSV_Master, arg_user_id):
        """
        CSVマスタを登録する
        引数
            arg_CSV_master_row：CSVマスタ追加行
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_CSV_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.CSV_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.CSV_MASTER,
                arg_CSV_master_row.code,
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
                # CSVマスタを登録する
                self.session.add(arg_CSV_master_row)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_CSV_master.return_message_box.message_id = "HAB001I"
                return_CSV_master.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.CSV_MASTER,
                        arg_CSV_master_row.code,
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

    # CSVマスタ更新
    def update_CSV_master(self, arg_CSV_master_row: CSV_Master):
        """
        CSVマスタを更新する
        引数
            arg_CSV_master_row：CSVマスタ
        """
        # 返却用クラスをインスタンス化
        return_CSV_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.CSV_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.UPDATE.format(
                self.display_name,
                self.const.Table_Name.CSV_MASTER,
                arg_CSV_master_row.code,
            ),
            arg_CSV_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_CSV_master.return_message_box = error_message
            return return_CSV_master
        else:
            try:
                # CSVマスタを取得するSELECT文を作成する
                stmt = select(CSV_Master).where(
                    CSV_Master.code == arg_CSV_master_row.code,
                    CSV_Master.update_version == arg_CSV_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_CSV_master = self.session.scalars(stmt).all()
                if len(fill_CSV_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_CSV_master.return_message_box.message_id = "HAB003C"
                    return_CSV_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.CSV_MASTER,
                            arg_CSV_master_row.code,
                        ),
                        arg_CSV_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_CSV_master.return_message_box = error_message
                        return return_CSV_master
                    else:
                        return return_CSV_master
                else:
                    # CSVマスタを登録する
                    fill_CSV_master[0].code = arg_CSV_master_row.code
                    fill_CSV_master[0].HAB_at_text = arg_CSV_master_row.HAB_at_text
                    fill_CSV_master[0].amount_text = arg_CSV_master_row.amount_text
                    fill_CSV_master[0].HABdetail_text = (
                        arg_CSV_master_row.HABdetail_text
                    )
                    fill_CSV_master[0].character_code = (
                        arg_CSV_master_row.character_code
                    )
                    fill_CSV_master[0].del_flg = arg_CSV_master_row.del_flg
                    fill_CSV_master[0].update_user_id = (
                        arg_CSV_master_row.update_user_id
                    )
                    fill_CSV_master[0].update_version = (
                        int(arg_CSV_master_row.update_version) + 1
                    )
                    self.session.add(fill_CSV_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_CSV_master.return_message_box.message_id = "HAB002I"
                    return_CSV_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.CSV_MASTER,
                            arg_CSV_master_row.code,
                        ),
                        arg_CSV_master_row.update_user_id,
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
                    str_log_function_id, e, arg_CSV_master_row.update_user_id
                )
                return return_CSV_master
            finally:
                # セッションを閉じる
                self.session.close()

    # CSVマスタ削除
    def delete_CSV_master(self, arg_CSV_master_row: CSV_Master):
        """
        CSVマスタを削除する
        引数
            arg_CSV_master_row：CSVマスタ
        """
        # 返却用クラスをインスタンス化
        return_CSV_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.CSV_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.DELETE.format(
                self.display_name,
                self.const.Table_Name.CSV_MASTER,
                arg_CSV_master_row.code,
            ),
            arg_CSV_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_CSV_master.return_message_box = error_message
            return return_CSV_master
        else:
            try:
                # CSVマスタを取得するSELECT文を作成する
                stmt = select(CSV_Master).where(
                    CSV_Master.code == arg_CSV_master_row.code,
                    CSV_Master.update_version == arg_CSV_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_CSV_master = self.session.scalars(stmt).all()
                if len(fill_CSV_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_CSV_master.return_message_box.message_id = "HAB003C"
                    return_CSV_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_DELETE.format(
                            self.display_name,
                            self.const.Table_Name.CSV_MASTER,
                            arg_CSV_master_row.code,
                        ),
                        arg_CSV_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_CSV_master.return_message_box = error_message
                        return return_CSV_master
                    else:
                        return return_CSV_master
                else:
                    # CSVマスタを登録する
                    fill_CSV_master[0].del_flg = self.const.Del_flg.DELETE
                    fill_CSV_master[0].update_user_id = (
                        arg_CSV_master_row.update_user_id
                    )
                    fill_CSV_master[0].update_version = (
                        int(arg_CSV_master_row.update_version) + 1
                    )
                    self.session.add(fill_CSV_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_CSV_master.return_message_box.message_id = "HAB003I"
                    return_CSV_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.DELETE.format(
                            self.display_name,
                            self.const.Table_Name.CSV_MASTER,
                            arg_CSV_master_row.code,
                        ),
                        arg_CSV_master_row.update_user_id,
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
                    str_log_function_id, e, arg_CSV_master_row.update_user_id
                )
                return return_CSV_master
            finally:
                # セッションを閉じる
                self.session.close()
