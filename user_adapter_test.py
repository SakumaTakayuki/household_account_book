from db.common.engine import Return_Info
from db.user_adapter import User_Adapter

user_adapter = User_Adapter()

# 追加失敗
new_row = user_adapter.user_row
new_row.user_id = user_adapter.const.Admin.USER_ID
new_row.name = user_adapter.const.Admin.USER_ID
new_row.password = user_adapter.const.Admin.USER_ID
new_row.entry_user_id = user_adapter.const.Admin.USER_ID
result: Return_Info = user_adapter.create_user(new_row)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
# 追加成功
new_row = user_adapter.user_row
new_row.user_id = user_adapter.const.Admin.USER_ID + "001"
new_row.name = user_adapter.const.Admin.USER_ID + "001"
new_row.password = user_adapter.const.Admin.USER_ID + "001"
new_row.entry_user_id = user_adapter.const.Admin.USER_ID
result = user_adapter.create_user(new_row)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
# 追加データ取得
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID,
)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
print(
    f"{result.return_row.user_id}：{result.return_row.name}：{result.return_row.password}：{result.return_row.del_flg}"
)
print(
    f"{result.return_row.entry_user_id}：{result.return_row.entry_at}：{result.return_row.update_user_id}：{result.return_row.update_at}"
)
# 更新成功
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID + "001",
)
result_row = result.return_row[0]
result_row.name = user_adapter.const.Admin.USER_ID + "更新"
result_row.password = user_adapter.const.Admin.USER_ID + "更新"
result_row.update_user_id = user_adapter.const.Admin.USER_ID + "001"
result = user_adapter.update_user(result_row)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)

# 更新失敗（追加データ取得後にデータを更新する）
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID,
)
result_row1 = result.return_row[0]
result_row1.name = user_adapter.const.Admin.USER_ID + "排他更新"
result_row1.password = user_adapter.const.Admin.USER_ID + "排他更新"
result_row1.update_user_id = user_adapter.const.Admin.USER_ID
user_adapter.update_user(result_row1)  # 通常通り更新する
result_row2 = result.return_row[0]
result_row2.name = user_adapter.const.Admin.USER_ID + "失敗"
result_row2.password = user_adapter.const.Admin.USER_ID + "失敗"
result_row2.update_user_id = user_adapter.const.Admin.USER_ID
result = user_adapter.update_user(result_row2)  # fillした情報の時刻を渡す
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
# 更新データ取得成功
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID,
)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
print(
    f"{result.return_row.user_id}：{result.return_row.name}：{result.return_row.password}：{result.return_row.del_flg}"
)
print(
    f"{result.return_row.entry_user_id}：{result.return_row.entry_at}：{result.return_row.update_user_id}：{result.return_row.update_at}"
)
# データ削除成功
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID + "001",
)
result.update_user_id = user_adapter.const.Admin.USER_ID + "001"
result = user_adapter.delete_user(result)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
print(
    f"{result.return_row.user_id}：{result.return_row.name}：{result.return_row.password}：{result.return_row.del_flg}"
)
print(
    f"{result.return_row.entry_user_id}：{result.return_row.entry_at}：{result.return_row.update_user_id}：{result.return_row.update_at}"
)
# データ削除失敗（削除データ取得後にデータを更新する）
new_row = user_adapter.user_row
new_row.user_id = user_adapter.const.Admin.USER_ID + "002"
new_row.name = user_adapter.const.Admin.USER_ID + "002"
new_row.password = user_adapter.const.Admin.USER_ID + "002"
new_row.entry_user_id = user_adapter.const.Admin.USER_ID
user_adapter.create_user(new_row)
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "002",
    user_adapter.const.Admin.USER_ID,
)
result_row = result.return_row
result_row.result.update_user_id = user_adapter.const.Admin.USER_ID
user_adapter.update_user(result_row)  # 通常通り更新する
result_row.result.update_user_id = user_adapter.const.Admin.USER_ID + "002"
result = user_adapter.delete_user(result_row)  # fillした情報の時刻を渡す
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
print(
    f"{result.return_row.user_id}：{result.return_row.name}：{result.return_row.password}：{result.return_row.del_flg}"
)
print(
    f"{result.return_row.entry_user_id}：{result.return_row.entry_at}：{result.return_row.update_user_id}：{result.return_row.update_at}"
)
# 更新データ取得失敗
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.FIRST,
    user_adapter.const.Admin.USER_ID + "001",
    user_adapter.const.Admin.USER_ID,
)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
print(
    f"{result.return_row.user_id}：{result.return_row.name}：{result.return_row.password}：{result.return_row.del_flg}"
)
print(
    f"{result.return_row.entry_user_id}：{result.return_row.entry_at}：{result.return_row.update_user_id}：{result.return_row.update_at}"
)
# 一覧取得
result = user_adapter.fill_user(
    user_adapter.const.Fill_Kbn.LIST,
    None,
    user_adapter.const.Admin.USER_ID,
)
print(
    f"{result.return_message_box.message_id}：{result.return_message_box.message_text}"
)
for row in result.return_row:
    print(f"{row.user_id}：{row.name}：{row.password}：{row.del_flg}")
    print(f"{row.entry_user_id}：{row.entry_at}：{row.update_user_id}：{row.update_at}")
