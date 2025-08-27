from common.const import Const
from datetime import datetime
from zoneinfo import ZoneInfo


# ログ出力時例外エラーテキストファイル出力
class Create_Exception_Log:
    """
    ログ出力時例外エラーテキストファイル出力
    """

    # テキストファイル出力
    def create_exception_log(self, arg_function_id, arg_log_detail):
        """
        ログ出力例外エラー用テキストファイル出力
        引数
            arg_function_id：処理ID,
            arg_log_detail：例外エラー内容
        """
        f = None
        try:
            # 規定フォルダにファイルがない場合は作成して開く
            # ファイルがある場合はカーソルが最下行の状態で開く
            f = open(
                f"{Const.FilePath.EXCEPTION_FOLDER}/{Const.FilePath.EXCEPTION_FILE}",
                "a+",
                encoding="utf-8",
            )
            # 「現在時間   処理ID  例外エラー内容」を書き込む
            f.write(
                f"{datetime.now(ZoneInfo("Asia/Tokyo"))}  {arg_function_id}   {arg_log_detail}\n"
            )
            return Const.Log_Error_Kbn.LOG_EXCEPTION_ERROR
        except:
            return Const.Log_Error_Kbn.LOGFILE_CREATE_ERROR
        finally:
            # ファイルが開かれている場合
            if f is not None:
                # ファイルを閉じる
                f.close()
