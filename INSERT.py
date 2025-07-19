from sqlalchemy import select
from db.models import Master, HAB_Detail, Shop_Master, CSV_Master
from db.common.engine import Engine
import datetime


class Insert:
    def insert():
        try:
            adapter = Engine()
            master_row = []
            master_row.append(
                Master(
                    m_id="HAB_kbn", m_code="in", m_text="入金", entry_user_id="admin"
                )
            )
            master_row.append(
                Master(
                    m_id="HAB_kbn", m_code="out", m_text="出金", entry_user_id="admin"
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds", m_code="01", m_text="食費", entry_user_id="admin"
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds",
                    m_code="02",
                    m_text="消耗品費",
                    entry_user_id="admin",
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds",
                    m_code="03",
                    m_text="光熱通信費",
                    entry_user_id="admin",
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds", m_code="04", m_text="給与", entry_user_id="admin"
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds",
                    m_code="05",
                    m_text="サブスク",
                    entry_user_id="admin",
                )
            )
            master_row.append(
                Master(
                    m_id="HABkinds", m_code="06", m_text="その他", entry_user_id="admin"
                )
            )
            master_row.append(
                Master(
                    m_id="CSV_company",
                    m_code="paypay_card",
                    m_text="PayPayカード",
                    entry_user_id="admin",
                )
            )
            master_row.append(
                Master(
                    m_id="CSV_company",
                    m_code="credit_saison",
                    m_text="セゾンカード",
                    entry_user_id="admin",
                )
            )

            adapter.session.add_all(master_row)
            adapter.session.commit()

            shop_master_row = []
            shop_master_row.append(
                Shop_Master(code="01", name="出前館", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="01", name="キッチンコート", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="01", name="やよい軒", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="01", name="つけ麺　しろぼし", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(
                    code="01", name="元祖からあげ本舗大吉", entry_user_id="admin"
                )
            )
            shop_master_row.append(
                Shop_Master(code="01", name="セブンーイレブン", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="01", name="コモディイイダ", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(
                    code="01", name="ステーキハウスおなかいっぱ", entry_user_id="admin"
                )
            )
            shop_master_row.append(
                Shop_Master(code="01", name="松屋フーズ", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(
                    code="01", name="１６８カラアゲ弁当タオ", entry_user_id="admin"
                )
            )
            shop_master_row.append(
                Shop_Master(code="01", name="ニューカリカ", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="02", name="ミネドラッグ", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="02", name="ＡＢＣーＭＡＲＴ", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(
                    code="03", name="ｙ．ｕ　ｍｏｂｉｌｅ", entry_user_id="admin"
                )
            )
            shop_master_row.append(
                Shop_Master(code="03", name="ソフトバンク", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="03", name="楽天モバイル", entry_user_id="admin")
            )
            shop_master_row.append(
                Shop_Master(code="05", name="Ｕ－ＮＥＸＴ", entry_user_id="admin")
            )

            adapter.session.add_all(shop_master_row)
            adapter.session.commit()

            CSV_master_row = []
            CSV_master_row.append(
                CSV_Master(
                    code="paypay_card",
                    HAB_at_text="利用日/キャンセル日",
                    amount_text="当月支払金額",
                    HABdetail_text="利用店名・商品名",
                    character_code="utf-8-sig",
                    entry_user_id="admin",
                )
            )
            CSV_master_row.append(
                CSV_Master(
                    code="credit_saison",
                    HAB_at_text="利用日",
                    amount_text="利用金額",
                    HABdetail_text="ご利用店名及び商品名",
                    character_code="shift_jis",
                    entry_user_id="admin",
                )
            )

            adapter.session.add_all(CSV_master_row)
            adapter.session.commit()

        except Exception as e:
            print(e)
        finally:
            adapter.session.close()
