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
            user_adapter = User_Adapter()
            return True
        else:
            return False

    def create_user(self):
        user_adapter = User_Adapter()
        create_row = user_adapter.user_row
        create_row.user_id = "admin"
        create_row.name = "admin"
        create_row.password = "admin"
        create_row.entry_user_id = "admin"
        user_adapter.create_row(create_row)
