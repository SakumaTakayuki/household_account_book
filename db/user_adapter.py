from sqlalchemy import select, update
from sqlalchemy.orm import Session, selectinload
from db.models import User
from db.common.engine import Engine


# ユーザー情報テーブル接続
class User_Adapter(Engine):
    def __init__(self):
        super().__init__()
        self.user_row = User()

    # ユーザー情報追加
    def create_row(self, arg_user_row: User):
        user = User(
            user_id=arg_user_row.user_id,
            name=arg_user_row.name,
            password=arg_user_row.password,
            entry_user_id=arg_user_row.entry_user_id,
        )
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    # ユーザー情報取得
    def fill_row(self, argUser):
        stmt = select(User).where(User.user_id == argUser)
        with Session(self.engine) as session:
            row = session.scalars(stmt).one()
        return row
