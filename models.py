from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, String, Integer, DateTime, ForeignKey

from datetime import datetime
from zoneinfo import ZoneInfo


class Bass(DeclarativeBase):
    pass


# ユーザー情報
class User(Bass):
    __tablename__ = "users"
    # ユーザーID
    user_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    # 名前
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    # パスワード
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), nullable=False, default="0")
    # 登録ユーザー
    entry_user_id: Mapped[str] = mapped_column(String(20), nullable=False)
    # 登録時間
    entry_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
    # 更新ユーザー
    update_user_id: Mapped[str] = mapped_column(String(20), nullable=True)
    # 更新時間
    update_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )


# 家計簿詳細
class HAB_Detail(Bass):
    __tablename__ = "HAB_detail"
    # 詳細番号
    HAB_seq: Mapped[int] = mapped_column(Integer, primary_key=True)
    # 入出金区分
    HAB_kbn: Mapped[str] = mapped_column(String(1), nullable=False)
    # 利用日時
    HAB_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # 金額
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    # 詳細種類
    HABkinds: Mapped[str] = mapped_column(String(20), nullable=False)
    # 家計簿詳細
    HABdetail: Mapped[str] = mapped_column(Text, nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
    # 登録ユーザー
    entry_user_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("users.user_id"), nullable=False
    )
    # 登録時間
    entry_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
    # 更新ユーザー
    update_user_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("users.user_id"), nullable=True
    )
    # 更新時間
    update_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )


# ログ
class Log(Bass):
    __tablename__ = "log"
    # ログ番号
    log_seq: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ログ種類
    log_kinds: Mapped[str] = mapped_column(String(20), nullable=False)
    # 処理ID
    function_id: Mapped[str] = mapped_column(String(10), nullable=False)
    # ログ詳細
    log_detail: Mapped[str] = mapped_column(Text, nullable=False)
    # 操作ユーザー
    user_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("users.user_id"), nullable=False
    )
    # 操作時間
    operate_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )


# マスタ
class Master(Bass):
    __tablename__ = "master"
    # マスタID
    M_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    # マスタコード
    m_code: Mapped[str] = mapped_column(String(10), nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
    # 登録ユーザー
    entry_user_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("users.user_id"), nullable=False
    )
    # 登録時間
    entry_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
    # 更新ユーザー
    update_user_id: Mapped[str] = mapped_column(
        String(20), ForeignKey("users.user_id"), nullable=True
    )
    # 更新時間
    update_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )
