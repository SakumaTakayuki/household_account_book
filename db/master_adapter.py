from sqlalchemy import select, case
from db.models import Master
from db.common.engine import Engine, Return_Info


# マスタテーブル接続
class Master_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.MASTER  # マスタ

    # マスタ取得
    def fill_master(self, arg_user_id):
        """
        マスタを取得する
        """
        # 返却用クラスをインスタンス化
        return_master = Return_Info()
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
                # マスタを取得するSELECT文を作成
                stmt = (
                    select(
                        Master.m_id,
                        Master.m_code,
                        Master.m_text,
                        case(
                            (Master.del_flg == 1, "削除"),
                            else_="",
                        ).label("del_flg"),
                        Master.update_version,
                    ).select_from(Master)
                    # 並び順を設定する
                    .order_by(
                        Master.m_id,
                        Master.m_code,
                    )
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得したマスタを代入する
                return_master.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.MASTER,
                        self.const.Const_Text.ALL,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(str_log_function_id, e, arg_user_id)
                return
            finally:
                # セッションを閉じる
                self.session.close()

    # マスタ登録
    def create_master(self, arg_master_row: Master, arg_user_id):
        """
        マスタを登録する
        引数
            arg_master_row：マスタ追加行
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_master = Return_Info()
        log_detail = f"{arg_master_row.m_id} {arg_master_row.m_code}"
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.MASTER,
                log_detail,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_master.return_message_box = error_message
            return return_master
        else:
            try:
                # マスタを登録する
                self.session.add(arg_master_row)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_master.return_message_box.message_id = "HAB001I"
                return_master.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.MASTER,
                        log_detail,
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_master.return_message_box = error_message
                    return return_master
                else:
                    return return_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_master
            finally:
                # セッションを閉じる
                self.session.close()

    # マスタ更新
    def update_master(self, arg_master_row: Master):
        """
        マスタを更新する
        引数
            arg_master_row：マスタ
        """
        # 返却用クラスをインスタンス化
        return_master = Return_Info()
        log_detail = f"{arg_master_row.m_id} {arg_master_row.m_code}"
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.UPDATE.format(
                self.display_name,
                self.const.Table_Name.MASTER,
                log_detail,
            ),
            arg_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_master.return_message_box = error_message
            return return_master
        else:
            try:
                # マスタを取得するSELECT文を作成する
                stmt = select(Master).where(
                    Master.m_id == arg_master_row.m_id,
                    Master.m_code == arg_master_row.m_code,
                    Master.update_version == arg_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_master = self.session.scalars(stmt).all()
                if len(fill_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_master.return_message_box.message_id = "HAB003C"
                    return_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            log_detail,
                        ),
                        arg_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_master.return_message_box = error_message
                        return return_master
                    else:
                        return return_master
                else:
                    # マスタを登録する
                    fill_master[0].m_id = arg_master_row.m_id
                    fill_master[0].m_code = arg_master_row.m_code
                    fill_master[0].m_text = arg_master_row.m_text
                    fill_master[0].del_flg = arg_master_row.del_flg
                    fill_master[0].update_user_id = arg_master_row.update_user_id
                    fill_master[0].update_version = (
                        int(arg_master_row.update_version) + 1
                    )
                    self.session.add(fill_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_master.return_message_box.message_id = "HAB002I"
                    return_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            log_detail,
                        ),
                        arg_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_master.return_message_box = error_message
                        return return_master
                    else:
                        return return_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_master_row.update_user_id
                )
                return return_master
            finally:
                # セッションを閉じる
                self.session.close()

    # マスタ削除
    def delete_master(self, arg_master_row: Master):
        """
        マスタを削除する
        引数
            arg_master_row：マスタ
        """
        # 返却用クラスをインスタンス化
        return_master = Return_Info()
        log_detail = f"{arg_master_row.m_id} {arg_master_row.m_code}"
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.DELETE.format(
                self.display_name,
                self.const.Table_Name.MASTER,
                log_detail,
            ),
            arg_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_master.return_message_box = error_message
            return return_master
        else:
            try:
                # ユーザーマスタを取得するSELECT文を作成する
                stmt = select(Master).where(
                    Master.m_id == arg_master_row.m_id,
                    Master.m_code == arg_master_row.m_code,
                    Master.update_version == arg_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_master = self.session.scalars(stmt).all()
                if len(fill_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_master.return_message_box.message_id = "HAB003C"
                    return_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_DELETE.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            log_detail,
                        ),
                        arg_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_master.return_message_box = error_message
                        return return_master
                    else:
                        return return_master
                else:
                    # ユーザーマスタを登録する
                    fill_master[0].del_flg = self.const.Del_flg.DELETE
                    fill_master[0].update_user_id = arg_master_row.update_user_id
                    fill_master[0].update_version = (
                        int(arg_master_row.update_version) + 1
                    )
                    self.session.add(fill_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_master.return_message_box.message_id = "HAB003I"
                    return_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.DELETE.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            log_detail,
                        ),
                        arg_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_master.return_message_box = error_message
                        return return_master
                    else:
                        return return_master
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_master.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_master_row.update_user_id
                )
                return return_master
            finally:
                # セッションを閉じる
                self.session.close()

    # 入出金区分取得
    def fill_HAB_kbn(self):
        """
        入出金区分を取得する
        """
        # 返却用クラスをインスタンス化
        return_HAB_kbn = Return_Info()
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
                self.const.Display.COMMON_PARTS,
                self.const.Table_Name.MASTER,
                self.const.Master_ID.HAB_kbn,
                self.const.Const_Text.TEXT_BLANK,
            ),
            self.const.Common_Parts.USER_ID,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            return
        else:
            try:
                # 入出金区分を取得するSELECT文を作成
                stmt = select(Master).where(Master.m_id == self.const.Master_ID.HAB_kbn)
                # SELECT文を全件取得で実行する
                select_row = self.session.scalars(stmt).all()
                # 返却用の返却行に取得した入出金区分を代入する
                return_HAB_kbn.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.const.Display.COMMON_PARTS,
                        self.const.Table_Name.MASTER,
                        self.const.Master_ID.HAB_kbn,
                        len(select_row),
                    ),
                    self.const.Common_Parts.USER_ID,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_HAB_kbn
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(
                    str_log_function_id, e, self.const.Common_Parts.USER_ID
                )
                return
            finally:
                # セッションを閉じる
                self.session.close()

    # 詳細種類取得
    def fill_HABkinds(self):
        """
        詳細種類を取得する
        """
        # 返却用クラスをインスタンス化
        return_HABkinds = Return_Info()
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
                self.const.Display.COMMON_PARTS,
                self.const.Table_Name.MASTER,
                self.const.Master_ID.HABkinds,
                self.const.Const_Text.TEXT_BLANK,
            ),
            self.const.Common_Parts.USER_ID,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            return
        else:
            try:
                # 詳細種類を取得するSELECT文を作成
                stmt = select(Master).where(
                    Master.m_id == self.const.Master_ID.HABkinds
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.scalars(stmt).all()
                # 返却用の返却行に取得した詳細種類を代入する
                return_HABkinds.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.const.Display.COMMON_PARTS,
                        self.const.Table_Name.MASTER,
                        self.const.Master_ID.HABkinds,
                        len(select_row),
                    ),
                    self.const.Common_Parts.USER_ID,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_HABkinds
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(
                    str_log_function_id, e, self.const.Common_Parts.USER_ID
                )
                return
            finally:
                # セッションを閉じる
                self.session.close()

    # CSV提供会社取得
    def fill_CSV_company(self):
        """
        CSV提供会社を取得する
        """
        # 返却用クラスをインスタンス化
        return_CSV_company = Return_Info()
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
                self.const.Display.COMMON_PARTS,
                self.const.Table_Name.MASTER,
                self.const.Master_ID.CSV_COMPANY,
                self.const.Const_Text.TEXT_BLANK,
            ),
            self.const.Common_Parts.USER_ID,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            return
        else:
            try:
                # CSV提供会社を取得するSELECT文を作成
                stmt = select(Master).where(
                    Master.m_id == self.const.Master_ID.CSV_COMPANY
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.scalars(stmt).all()
                # 返却用の返却行に取得したCSV提供会社を代入する
                return_CSV_company.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.const.Display.COMMON_PARTS,
                        self.const.Table_Name.MASTER,
                        self.const.Master_ID.CSV_COMPANY,
                        len(select_row),
                    ),
                    self.const.Common_Parts.USER_ID,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    return
                else:
                    return return_CSV_company
            except Exception as e:
                # 例外エラー用メッセージ作成
                self.exception_log(
                    str_log_function_id, e, self.const.Common_Parts.USER_ID
                )
                return
            finally:
                # セッションを閉じる
                self.session.close()
