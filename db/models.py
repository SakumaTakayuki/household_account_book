from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, String, Integer, DateTime, BigInteger

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
    # 更新管理
    update_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


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
    HABdetail: Mapped[str] = mapped_column(Text, nullable=True)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
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
    # 更新管理
    update_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


# ログ
class Log(Bass):
    __tablename__ = "log"
    # ログ番号
    log_seq: Mapped[int] = mapped_column(Integer, primary_key=True)
    # ログ種類
    log_kinds: Mapped[str] = mapped_column(String(1), nullable=False)
    # 処理ID
    function_id: Mapped[str] = mapped_column(String(20), nullable=False)
    # ログ詳細
    log_detail: Mapped[str] = mapped_column(Text, nullable=False)
    # 操作ユーザー
    user_id: Mapped[str] = mapped_column(String(20), nullable=False)
    # 操作時間
    operate_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo"))
    )


# マスタ
class Master(Bass):
    __tablename__ = "master"
    # マスタID
    m_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    # マスタコード
    m_code: Mapped[str] = mapped_column(String(20), primary_key=True)
    # マスタテキスト
    m_text: Mapped[str] = mapped_column(Text, nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
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
    # 更新管理
    update_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


# 店舗マスタ
class Shop_Master(Bass):
    __tablename__ = "shop_master"
    # 番号
    seq: Mapped[int] = mapped_column(Integer, primary_key=True)
    # HABKindsコード
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    # 店名
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
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
    # 更新管理
    update_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)


# CSV取込列マスタ
class CSV_Master(Bass):
    __tablename__ = "CSV_master"
    # 会社コード
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    # 利用日時列名
    HAB_at_text: Mapped[str] = mapped_column(String(20), nullable=False)
    # 金額列名
    amount_text: Mapped[str] = mapped_column(String(20), nullable=False)
    # 家計簿詳細列名
    HABdetail_text: Mapped[str] = mapped_column(String(20), nullable=False)
    # 文字コード
    character_code: Mapped[str] = mapped_column(String(20), nullable=False)
    # 削除フラグ
    del_flg: Mapped[str] = mapped_column(String(1), default="0")
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
    # 更新管理
    update_version: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
