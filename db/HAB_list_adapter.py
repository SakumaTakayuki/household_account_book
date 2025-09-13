from sqlalchemy import select, and_, func, case
from sqlalchemy.orm import aliased
from db.models import HAB_Detail, Master
from db.common.engine import Engine, Return_Info


# 家計簿詳細テーブル接続
class HAB_List_Adapter(Engine):
    def __init__(self):
        super().__init__()
        # 画面名を設定
        self.display_name = self.const.Display.HAB_LIST  # 家計簿一覧

    # 家計簿一覧取得
    def fill_HAB_list(self, arg_where_year_month, arg_user_id):
        """
        家計簿一覧を取得する
        引数
            arg_where_year_month：検索条件
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_HAB_list = Return_Info()
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
                arg_where_year_month,
                self.const.Const_Text.TEXT_BLANK,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_list.return_message_box = error_message
            return return_HAB_list
        else:
            try:
                # 家計簿一覧を取得するSELECT文を作成する
                # マスタテーブルを別名で定義する
                Master1 = aliased(Master)
                Master2 = aliased(Master)
                stmt = (
                    select(
                        HAB_Detail.HAB_seq,
                        HAB_Detail.HAB_at,
                        Master1.m_text.label("HAB_kbn"),
                        HAB_Detail.amount,
                        Master2.m_text.label("HABkinds"),
                        HAB_Detail.HABdetail,
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
                    .where(
                        HAB_Detail.HAB_at.like(f"{arg_where_year_month}%"),
                        HAB_Detail.del_flg == self.const.Del_flg.NON_DELETE,
                    )
                    # 並び順を設定する
                    .order_by(
                        HAB_Detail.HAB_at,
                        HAB_Detail.HAB_kbn,
                        HAB_Detail.amount,
                        HAB_Detail.HABkinds,
                    )
                )
                # SELECT文を全件取得で実行する
                select_row = self.session.execute(stmt).all()
                # 返却用の返却行に取得した家計簿一覧を代入する
                return_HAB_list.return_row = select_row
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.FILL.format(
                        self.display_name,
                        self.const.Table_Name.HAB_DETAIL,
                        arg_where_year_month,
                        len(select_row),
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_HAB_list.return_message_box = error_message
                    return return_HAB_list
                else:
                    return return_HAB_list
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_list.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_HAB_list
            finally:
                # セッションを閉じる
                self.session.close()

    # 入出金円グラフデータ取得
    def fill_HAB_kbn_PieChart_data(self, arg_where_year_month, arg_user_id):
        """
        入出金円グラフデータを取得する
        引数
            arg_where_year_month：検索条件
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_HAB_kbn_PieChart_data = Return_Info()
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
            self.message.Log_Message.FILL_HAB_kbn_PIECHART.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_where_year_month,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_kbn_PieChart_data.return_message_box = error_message
            return return_HAB_kbn_PieChart_data
        else:
            try:
                # 入出金区分を取得するSELECT文を作成
                HAB_kbn_stmt = select(Master).where(
                    Master.m_id == self.const.Master_ID.HAB_kbn,
                )
                # SELECT文を全件取得で実行する
                select_HAB_kbn_row = self.session.scalars(HAB_kbn_stmt).all()
                if len(select_HAB_kbn_row) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_HAB_kbn_PieChart_data.return_message_box.message_id = (
                        "HAB003W"
                    )
                    return_HAB_kbn_PieChart_data.return_message_box.message_text = (
                        self.message.Message_Box.HAB003W
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL_HAB_kbn_PIECHART_ERROR.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            self.const.Master_ID.HAB_kbn,
                        ),
                        arg_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_kbn_PieChart_data.return_message_box = error_message
                        return return_HAB_kbn_PieChart_data
                    else:
                        return return_HAB_kbn_PieChart_data
                else:
                    # 入出金円グラフデータを取得するSELECT文を作成する
                    # 副問い合わせ
                    sub_stmt = (
                        select(
                            Master.m_code.label("m_code"), Master.m_text.label("m_text")
                        )
                        .select_from(Master)
                        .where(
                            Master.m_id == self.const.Master_ID.HAB_kbn,
                        )
                        .subquery("master")
                    )
                    case_list = []
                    for HAB_kbn_row in select_HAB_kbn_row:
                        case_list.append(
                            (
                                sub_stmt.c.m_code == HAB_kbn_row.m_code
                                and HAB_Detail.HAB_kbn == HAB_kbn_row.m_code,
                                HAB_Detail.amount,
                            )
                        )
                    # 主問い合わせ
                    stmt = (
                        select(
                            sub_stmt.c.m_code,
                            sub_stmt.c.m_text,
                            func.coalesce(
                                func.sum(
                                    case(*case_list),
                                ),
                                0,
                            ).label("amount"),
                        )
                        .select_from(sub_stmt)
                        # マスタテーブルと結合する
                        .outerjoin(
                            HAB_Detail,
                            onclause=and_(
                                sub_stmt.c.m_code == HAB_Detail.HAB_kbn,
                                HAB_Detail.HAB_at.like(
                                    f"{arg_where_year_month}%",
                                ),
                                HAB_Detail.del_flg == self.const.Del_flg.NON_DELETE,
                            ),
                        )
                        .group_by(sub_stmt.c.m_text)
                    )
                    # SELECT文を全件取得で実行する
                    select_row = self.session.execute(stmt).all()
                    # 返却用の返却行に取得した家計簿一覧を代入する
                    return_HAB_kbn_PieChart_data.return_row = select_row
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL_HAB_kbn_PIECHART.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_where_year_month,
                        ),
                        arg_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HAB_kbn_PieChart_data.return_message_box = error_message
                        return return_HAB_kbn_PieChart_data
                    else:
                        return return_HAB_kbn_PieChart_data
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_kbn_PieChart_data.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_HAB_kbn_PieChart_data
            finally:
                # セッションを閉じる
                self.session.close()

    # 詳細種類円グラフデータ取得
    def fill_HABkinds_PieChart_data(self, arg_where_year_month, arg_user_id):
        """
        詳細種類グラフデータを取得する
        引数
            arg_where_year_month：検索条件
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_HABkinds_PieChart_data = Return_Info()
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
            self.message.Log_Message.FILL_HABkinds_PIECHART.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                arg_where_year_month,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HABkinds_PieChart_data.return_message_box = error_message
            return return_HABkinds_PieChart_data
        else:
            try:
                # 詳細種類を取得するSELECT文を作成
                HABkinds_stmt = select(Master).where(
                    Master.m_id == self.const.Master_ID.HABkinds
                )
                # SELECT文を全件取得で実行する
                select_HABkinds_row = self.session.scalars(HABkinds_stmt).all()
                if len(select_HABkinds_row) == 0:
                    # 返却用のメッセージボックスにIDとメッセージ内容を代入する
                    return_HABkinds_PieChart_data.return_message_box.message_id = (
                        "HAB003W"
                    )
                    return_HABkinds_PieChart_data.return_message_box.message_text = (
                        self.message.Message_Box.HAB003W
                    )
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL_HABkinds_PIECHART_ERROR.format(
                            self.display_name,
                            self.const.Table_Name.MASTER,
                            self.const.Master_ID.HABkinds,
                        ),
                        arg_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HABkinds_PieChart_data.return_message_box = error_message
                        return return_HABkinds_PieChart_data
                    else:
                        return return_HABkinds_PieChart_data
                else:
                    # 入出金円グラフデータを取得するSELECT文を作成する
                    # 副問い合わせ
                    sub_stmt = (
                        select(
                            Master.m_code.label("m_code"), Master.m_text.label("m_text")
                        )
                        .select_from(Master)
                        .where(
                            Master.m_id == self.const.Master_ID.HABkinds,
                        )
                        .subquery("master")
                    )
                    case_list = []
                    for HABkinds_row in select_HABkinds_row:
                        case_list.append(
                            (
                                sub_stmt.c.m_code == HABkinds_row.m_code
                                and HAB_Detail.HAB_kbn == HABkinds_row.m_code,
                                HAB_Detail.amount,
                            )
                        )
                    # 主問い合わせ
                    stmt = (
                        select(
                            sub_stmt.c.m_code,
                            sub_stmt.c.m_text,
                            func.coalesce(
                                func.sum(
                                    case(*case_list),
                                ),
                                0,
                            ).label("amount"),
                        )
                        .select_from(sub_stmt)
                        # マスタテーブルと結合する
                        .outerjoin(
                            HAB_Detail,
                            onclause=and_(
                                sub_stmt.c.m_code == HAB_Detail.HABkinds,
                                HAB_Detail.HAB_at.like(f"{arg_where_year_month}%"),
                                HAB_Detail.HAB_kbn == self.const.HAB_kbn_code.kbn_out,
                                HAB_Detail.del_flg == self.const.Del_flg.NON_DELETE,
                            ),
                        )
                        .group_by(sub_stmt.c.m_text)
                    )
                    # SELECT文を全件取得で実行する
                    select_row = self.session.execute(stmt).all()
                    # 返却用の返却行に取得した家計簿一覧を代入する
                    return_HABkinds_PieChart_data.return_row = select_row
                    # ENDログ出力
                    error_message = self.create_log(
                        self.const.Log_Kinds.END,
                        str_log_function_id,
                        self.message.Log_Message.FILL_HABkinds_PIECHART.format(
                            self.display_name,
                            self.const.Table_Name.HAB_DETAIL,
                            arg_where_year_month,
                        ),
                        arg_user_id,
                    )
                    # ENDログ出力失敗の場合
                    if error_message != None:
                        # 返却用のメッセージボックスに例外エラーメッセージを代入する
                        return_HABkinds_PieChart_data.return_message_box = error_message
                        return return_HABkinds_PieChart_data
                    else:
                        return return_HABkinds_PieChart_data
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HABkinds_PieChart_data.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_HABkinds_PieChart_data
            finally:
                # セッションを閉じる
                self.session.close()

    # 家計簿登録
    def create_HAB_list(self, arg_HAB_ditail_row: HAB_Detail, arg_user_id):
        """
        家計簿を登録する
        引数
            arg_HAB_ditail_row：家計簿
            arg_user_id：操作ユーザー
        """
        # 返却用クラスをインスタンス化
        return_HAB_list = Return_Info()
        # ログ出力のfunction_idを作成
        str_log_function_id = self.message.Log_Function_Id.id.format(
            self.const.Log_Kinds.INFO,
            self.const.Log_Process.INSERT,
            self.const.Log_Function.HAB_DETAIL,
        )
        # 新規登録する家計簿の年月日時刻を作成する
        log_ditail = arg_HAB_ditail_row.HAB_at.strftime("%Y-%m-%d %H:%M")
        # STARTログ出力
        error_message = self.create_log(
            self.const.Log_Kinds.START,
            str_log_function_id,
            self.message.Log_Message.INSERT.format(
                self.display_name,
                self.const.Table_Name.HAB_DETAIL,
                log_ditail,
            ),
            arg_user_id,
        )
        # STARTログ出力失敗の場合
        if error_message != None:
            # 返却用のメッセージボックスに例外エラーメッセージを代入する
            return_HAB_list.return_message_box = error_message
            return return_HAB_list
        else:
            try:
                # 家計簿を登録する
                self.session.add(arg_HAB_ditail_row)
                self.session.commit()
                # 返却する登録完了メッセージを作成する
                return_HAB_list.return_message_box.message_id = "HAB001I"
                return_HAB_list.return_message_box.message_text = (
                    self.message.Message_Box.HAB001I
                )
                # ENDログ出力
                error_message = self.create_log(
                    self.const.Log_Kinds.END,
                    str_log_function_id,
                    self.message.Log_Message.INSERT.format(
                        self.display_name,
                        self.const.Table_Name.HAB_DETAIL,
                        log_ditail,
                    ),
                    arg_user_id,
                )
                # ENDログ出力失敗の場合
                if error_message != None:
                    # 返却用のメッセージボックスに例外エラーメッセージを代入する
                    return_HAB_list.return_message_box = error_message
                    return return_HAB_list
                else:
                    return return_HAB_list
            except Exception as e:
                # 例外エラー用メッセージ作成
                return_HAB_list.return_message_box = self.exception_log(
                    str_log_function_id, e, arg_user_id
                )
                return return_HAB_list
            finally:
                # セッションを閉じる
                self.session.close()
