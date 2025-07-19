from db.models import Bass
from db.common.engine import Engine
from db.users_adapter import Users_Adapter
from db.models import User
from werkzeug.security import generate_password_hash


# テーブルとadminユーザー作成
class Create_Table(Engine):
    def __init__(self):
        super().__init__()

    # DBにとadminユーザー作成
    def create_table(self):
        if len(self.inspector.get_table_names()) == 0:
            Bass.metadata.create_all(self.engine)
            return True
        else:
            return False

    def create_user(self):
        user_adapter = Users_Adapter()
        create_row = User()
        create_row.user_id = self.const.Admin.USER_ID
        create_row.name = self.const.Admin.NAME
        create_row.password = self.const.Admin.PASSWORD
        create_row.entry_user_id = self.const.Admin.USER_ID
        user_adapter.create_users(create_row, self.const.Admin.USER_ID)
