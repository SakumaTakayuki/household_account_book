from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload
from models import User


# ユーザー情報テーブル接続
class User_Adapter:
    db_engine = None
    user_row = User()

    def __init__(self, arg_db_engine):
        self.db_engine = arg_db_engine

    # ユーザー情報追加
    def create_row(self, arg_user_row: User):
        user = User(
            user_id=arg_user_row.user_id,
            name=arg_user_row.name,
            password=arg_user_row.password,
            entry_user_id="administrator",
        )
        with Session(self.db_engine.engine) as session:
            session.add(user)
            session.commit()

    # ユーザー情報取得
    def fill_row(self, argUser):
        stmt = select(User).where(User.user_id == argUser)
        with Session(self.db_engine.engine) as session:
            row = session.scalars(stmt).one()
        return row
