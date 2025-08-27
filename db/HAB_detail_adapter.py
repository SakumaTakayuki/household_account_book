from sqlalchemy import select, and_
from sqlalchemy.orm import aliased
from db.models import HAB_Detail, Master
from db.common.engine import Engine, Return_Info


# 家計簿詳細テーブル接続
class HAB_Detail_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.HAB_DETAIL  # 家計簿詳細

    # 家計簿詳細取得
    def fill_HAB_detail(self, arg_HAB_seq, arg_user_id):
        """
        家計簿詳細を取得する
        引数
            arg_HAB_seq：検索条件
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_HAB_detail = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.SELECT,
            self.const.Log_Function.HAB_DETAIL,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.FILL.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_HAB_seq,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_detail.return_message_box = error_message
            return return_HAB_detail
        else:
            try:
                # 家計簿詳細を取得するSELECT文を作成する
                # マスタテーブルを別名で定義する
                Master1 = aliased(Master)
                Master2 = aliased(Master)
                stmt = (
                    select(
                        HAB_Detail.HAB_seq,
                        HAB_Detail.HAB_at,
                        HAB_Detail.HAB_kbn,
                        Master1.m_text.label("HAB_kbn_text"),
                        HAB_Detail.amount,
                        HAB_Detail.HABkinds,
                        Master2.m_text.label("HABkinds_text"),
                        HAB_Detail.HABdetail,
                        HAB_Detail.update_version,
                    ).select_from(HAB_Detail)
                    # マスタテーブルと結合する
                    .join(
                        Master1,
                        onclause=and_(
                            HAB_Detail.HAB_kbn == Master1.m_code,
                            Master1.m_id == "HAB_kbn",
                            Master1.del_flg == "0",
                        ),
                    )
                    # マスタテーブルと結合する
                    .join(
                        Master2,
                        onclause=and_(
                            HAB_Detail.HABkinds == Master2.m_code,
                            Master2.m_id == "HABkinds",
                            Master2.del_flg == "0",
                        ),
                    )
                    # Where句に引数の検索条件を設定する
                    .where(HAB_Detail.HAB_seq == int(arg_HAB_seq))
                )
                # SELECT文を全件取得で実行する
                fill_HAB_detail = self.session.execute(stmt).all()
                if len(fill_HAB_detail) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_HAB_detail.return_message_box.message_id = "HAB001C"
                    return_HAB_detail.return_message_box.message_text = (
                        self.message.Message_Box.HAB001C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.Fill_NO_ROW.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_seq,
                        ),
                        self.const.Login.USER_ID,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
                else:
                    # 返却用の返却行に取得した家計簿詳細を代入する
                    return_HAB_detail.return_row = fill_HAB_detail
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_seq,
                            len(fill_HAB_detail),
                        ),
                        arg_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_detail.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_HAB_detail
            finally:
                # セッションを閉じる
                self.session.close()

    # 家計簿詳細更新
    def update_HAB_detail(self, arg_HAB_ditail_row: HAB_Detail):
        """
        家計簿詳細を更新する
        引数
            arg_HAB_ditail_row：家計簿詳細
        """
        # 返却用クラスをインスタンス化
        return_HAB_detail = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.UPDATE,
            self.const.Log_Function.HAB_DETAIL,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.UPDATE.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_HAB_ditail_row.HAB_seq,
            ),
            arg_HAB_ditail_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_detail.return_message_box = error_message
            return return_HAB_detail
        else:
            try:
                # 家計簿詳細を取得するSELECT文を作成する
                stmt = select(HAB_Detail).where(
                    HAB_Detail.HAB_seq == arg_HAB_ditail_row.HAB_seq,
                    HAB_Detail.update_version == arg_HAB_ditail_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_HAB_detail = self.session.scalars(stmt).all()
                if len(fill_HAB_detail) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_HAB_detail.return_message_box.message_id = "HAB003C"
                    return_HAB_detail.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_ditail_row.HAB_seq,
                        ),
                        arg_HAB_ditail_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
                else:
                    # 家計簿詳細を登録する
                    fill_HAB_detail[0].HAB_at = arg_HAB_ditail_row.HAB_at
                    fill_HAB_detail[0].HAB_kbn = arg_HAB_ditail_row.HAB_kbn
                    fill_HAB_detail[0].amount = arg_HAB_ditail_row.amount
                    fill_HAB_detail[0].HABkinds = arg_HAB_ditail_row.HABkinds
                    fill_HAB_detail[0].HABdetail = arg_HAB_ditail_row.HABdetail
                    fill_HAB_detail[0].update_user_id = (
                        arg_HAB_ditail_row.update_user_id
                    )
                    fill_HAB_detail[0].update_version = (
                        int(arg_HAB_ditail_row.update_version) + 1
                    )
                    self.session.add(fill_HAB_detail[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_HAB_detail.return_message_box.message_id = "HAB002I"
                    return_HAB_detail.return_message_box.message_text = (
                        self.message.Message_Box.HAB002I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.UPDATE.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_ditail_row.HAB_seq,
                        ),
                        arg_HAB_ditail_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_detail.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_HAB_ditail_row.update_user_id
                )
                return return_HAB_detail
            finally:
                # セッションを閉じる
                self.session.close()

    # 家計簿詳細削除
    def delete_HAB_detail(self, arg_HAB_ditail_row: HAB_Detail):
        """
        家計簿詳細を更論理削除新する
        引数
            arg_HAB_ditail_row：家計簿詳細
        """
        # 返却用クラスをインスタンス化
        return_HAB_detail = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.DELETE,
            self.const.Log_Function.HAB_DETAIL,
        )
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.DELETE.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_HAB_ditail_row.HAB_seq,
            ),
            arg_HAB_ditail_row.update_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_detail.return_message_box = error_message
            return return_HAB_detail
        else:
            try:
                # 家計簿詳細を取得するSELECT文を作成する
                stmt = select(HAB_Detail).where(
                    HAB_Detail.HAB_seq == arg_HAB_ditail_row.HAB_seq,
                    HAB_Detail.update_version == arg_HAB_ditail_row.update_version,
                )
                # SELECT文を全件取得で実行する
                fill_HAB_detail = self.session.scalars(stmt).all()
                if len(fill_HAB_detail) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_HAB_detail.return_message_box.message_id = "HAB003C"
                    return_HAB_detail.return_message_box.message_text = (
                        self.message.Message_Box.HAB003C
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.NON_DELETE.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_ditail_row.HAB_seq,
                        ),
                        self.const.Login.USER_ID,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
                else:
                    # 家計簿詳細を登録する
                    fill_HAB_detail[0].del_flg = self.const.Del_flg.DELETE
                    fill_HAB_detail[0].update_user_id = (
                        arg_HAB_ditail_row.update_user_id
                    )
                    fill_HAB_detail[0].update_version = (
                        int(arg_HAB_ditail_row.update_version) + 1
                    )
                    self.session.add(fill_HAB_detail[0])
                    self.session.commit()
                    # 返却する登録完了メッセージを作成する
                    return_HAB_detail.return_message_box.message_id = "HAB003I"
                    return_HAB_detail.return_message_box.message_text = (
                        self.message.Message_Box.HAB003I
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.DELETE.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_HAB_ditail_row.HAB_seq,
                        ),
                        arg_HAB_ditail_row.update_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_detail.return_message_box = error_message
                        return return_HAB_detail
                    else:
                        return return_HAB_detail
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_detail.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_HAB_ditail_row.update_user_id
                )
                return return_HAB_detail
            finally:
                # セッションを閉じる
                self.session.close()
