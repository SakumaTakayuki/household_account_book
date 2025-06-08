from db.models import Bass
from db.common.engine import Engine
from db.user_adapter import User_Adapter
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
        user_adapter = User_Adapter()
        create_row = user_adapter.user_row
        create_row.user_id = self.const.Admin.USER_ID
        create_row.name = self.const.Admin.NAME
        create_row.password = generate_password_hash(
            self.const.Admin.PASSWORD, method="pbkdf2:sha256"
        )
        create_row.entry_user_id = self.const.Admin.USER_ID
        user_adapter.create_user(create_row)
