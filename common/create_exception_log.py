from datetime import datetime
from zoneinfo import ZoneInfo


class Create_Exception_Log:
    def create_exception_log(self, arg_function_id, arg_log_detail):
        try:
            f = open("log/exception_log.txt", "a+", encoding="utf-8")
            f.write(
                f"{datetime.now(ZoneInfo("Asia/Tokyo"))}  {arg_function_id}   {arg_log_detail}\n"
            )
        except:
            return True
        finally:
            f.close()
