from sqlalchemy import select, and_, case
from db.models import Master, Shop_Master
from db.common.engine import Engine, Return_Info


# 店舗マスタテーブル接続
class Shop_Master_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.SHOP_MASTER  # 店舗マスタ

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
                stmt = (
                    select(
                        Shop_Master.seq,
                        Master.m_text.label("code_text"),
                        Shop_Master.name,
                        case(
                            (Shop_Master.del_flg == 1, "削除"),
                            else_="",
                        ).label("del_flg"),
                        Shop_Master.update_version,
                    ).select_from(Shop_Master)
                    # マスタテーブルと結合する
                    .join(
                        Master,
                        onclause=and_(
                            Shop_Master.code == Master.m_code,
                            Master.m_id == "HABkinds",
                            Master.del_flg == "0",
                        ),
                    )
                    # 並び順を設定する
                    .order_by(
                        Shop_Master.seq,
                    )
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

    # 店舗マスタ登録
    def create_shop_master(self, arg_shop_master_row: Shop_Master, arg_user_id):
        """
        店舗マスタを登録する
        引数
            arg_shop_master_row：店舗マスタ追加行
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_shop_master = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.SHOP_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.SHOP_MASTER,
                arg_shop_master_row.name,
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
                # 店舗マスタを登録する
                self.session.add(arg_shop_master_row)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_shop_master.return_message_box.message_id = "HAB001I"
                return_shop_master.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.SHOP_MASTER,
                        arg_shop_master_row.name,
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

    # 店舗マスタ更新
    def update_shop_master(self, arg_shop_master_row: Shop_Master):
        """
        店舗マスタを更新する
        引数
            arg_shop_master_row：店舗マスタ
        """
        # 返却用クラスをインスタンス化
        return_shop_master = Return_Info()
        log_detail = f"{arg_shop_master_row.seq} {arg_shop_master_row.name}"
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.SHOP_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.UPDATE.format(
                self.display_name,
                self.const.Table_Name.SHOP_MASTER,
                log_detail,
            ),
            arg_shop_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_shop_master.return_message_box = error_message
            return return_shop_master
        else:
            try:
                # 店舗マスタを取得するSELECT文を作成する
                stmt = select(Shop_Master).where(
                    Shop_Master.seq == arg_shop_master_row.seq,
                    Shop_Master.update_version == arg_shop_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_shop_master = self.session.scalars(stmt).all()
                if len(fill_shop_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_shop_master.return_message_box.message_id = "HAB003C"
                    return_shop_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.SHOP_MASTER,
                            log_detail,
                        ),
                        arg_shop_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_shop_master.return_message_box = error_message
                        return return_shop_master
                    else:
                        return return_shop_master
                else:
                    # 店舗マスタを登録する
                    fill_shop_master[0].seq = arg_shop_master_row.seq
                    fill_shop_master[0].code = arg_shop_master_row.code
                    fill_shop_master[0].name = arg_shop_master_row.name
                    fill_shop_master[0].del_flg = arg_shop_master_row.del_flg
                    fill_shop_master[0].update_user_id = (
                        arg_shop_master_row.update_user_id
                    )
                    fill_shop_master[0].update_version = (
                        int(arg_shop_master_row.update_version) + 1
                    )
                    self.session.add(fill_shop_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_shop_master.return_message_box.message_id = "HAB002I"
                    return_shop_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.SHOP_MASTER,
                            log_detail,
                        ),
                        arg_shop_master_row.update_user_id,
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
                    str_log_function_id, e, arg_shop_master_row.update_user_id
                )
                return return_shop_master
            finally:
                # セッションを閉じる
                self.session.close()

    # 店舗マスタ削除
    def delete_shop_master(self, arg_shop_master_row: Shop_Master):
        """
        店舗マスタを削除する
        引数
            arg_shop_master_row：店舗マスタ
        """
        # 返却用クラスをインスタンス化
        return_shop_master = Return_Info()
        log_detail = f"{arg_shop_master_row.seq} {arg_shop_master_row.name}"
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.SHOP_MASTER,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.DELETE.format(
                self.display_name,
                self.const.Table_Name.SHOP_MASTER,
                log_detail,
            ),
            arg_shop_master_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_shop_master.return_message_box = error_message
            return return_shop_master
        else:
            try:
                # 店舗マスタを取得するSELECT文を作成する
                stmt = select(Shop_Master).where(
                    Shop_Master.seq == arg_shop_master_row.seq,
                    Shop_Master.update_version == arg_shop_master_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_shop_master = self.session.scalars(stmt).all()
                if len(fill_shop_master) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_shop_master.return_message_box.message_id = "HAB003C"
                    return_shop_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_DELETE.format(
                            self.display_name,
                            self.const.Table_Name.SHOP_MASTER,
                            log_detail,
                        ),
                        arg_shop_master_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_shop_master.return_message_box = error_message
                        return return_shop_master
                    else:
                        return return_shop_master
                else:
                    # 店舗マスタを登録する
                    fill_shop_master[0].del_flg = self.const.Del_flg.DELETE
                    fill_shop_master[0].update_user_id = (
                        arg_shop_master_row.update_user_id
                    )
                    fill_shop_master[0].update_version = (
                        int(arg_shop_master_row.update_version) + 1
                    )
                    self.session.add(fill_shop_master[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_shop_master.return_message_box.message_id = "HAB003I"
                    return_shop_master.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.DELETE.format(
                            self.display_name,
                            self.const.Table_Name.SHOP_MASTER,
                            log_detail,
                        ),
                        arg_shop_master_row.update_user_id,
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
                    str_log_function_id, e, arg_shop_master_row.update_user_id
                )
                return return_shop_master
            finally:
                # セッションを閉じる
                self.session.close()
