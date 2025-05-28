# メッセージ一覧
class Message:

    # 処理ID用
    class Log_Function_Id:
        id = "{0}-{1}-{2}"

    # ログ詳細用
    class Log_Message:
        FILL = "{0}：{1} 取得 {2}件"
        Fill_NO_ROW = "{0}：{1} 取得 0件"
        INSERT = "{0}：{1} 追加"
        UPDATE = "{0}：{1} 更新"
        NON_UPDATE = "{0}：{1} 更新 排他エラー"

    # メッセージボックス用
    class Message_Box:
        # INFO
        HAB001I = "新規登録が完了しました。"
        HAB002I = "更新が完了しました。"
        # CAUTION
        HAB001C = "削除されたため表示できません。"
        HAB002C = "同じユーザーIDのユーザーが存在します。\nユーザーIDを変更して登録してください。"
        HAB003C = "他のユーザーが更新したため、更新に失敗しました。\n画面を再度開きなおしてください。"
        # WARNING
        HAB001W = (
            "ログファイル出力時にエラーが発生しました。\n管理者に連絡してください。"
        )
        HAB002W = "ログ作成時にエラーが発生しました。\n管理者に連絡してください。"
