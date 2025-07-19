from INSERT import Insert
from db.create_table import Create_Table
from db.users_adapter import Users_Adapter
from db.models import User
from common.const import Const


try:
    create_table = Create_Table()
    isCreate = create_table.create_table()
    if isCreate:
        create_table.create_user()

    Insert.insert()

    user_adapter = Users_Adapter()
    return_user = user_adapter.fill_users(Const.Admin.USER_ID)
    if return_user.return_message_box.message_text is None:
        print(return_user.return_row[0].user_id)
        print("テーブル・データ作成完了")
    else:
        print(return_user.return_message_box.message_text)
except Exception as e:
    print(e)
    print("例外エラー")
