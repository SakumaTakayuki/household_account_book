from sqlalchemy import create_engine, inspect
from models import Bass


# DB接続
class Engine:
    def __init__(self):
        self.engine = create_engine("sqlite:///example.db", echo=True)
        self.inspector = inspect(self.engine)

    # DBにテーブル作成
    def create_table(self):
        if len(self.inspector.get_table_names()) == 0:
            Bass.metadata.create_all(self.engine)
