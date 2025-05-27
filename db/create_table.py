from db.models import Bass
from db.common.engine import Engine
from db.user_adapter import User_Adapter


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
        create_row.password = self.const.Admin.PAAWORD
        create_row.entry_user_id = self.const.Admin.USER_ID
        user_adapter.create_user(create_row)
