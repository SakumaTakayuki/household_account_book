class Message:

    class Log_Function_Id:
        id = "{0}-{1}-{2}"

    class Log_Message:
        FILL = "{0}：{1} 取得 {2}件"
        Fill_NO_ROW = "{0}：{1} 取得 0件"
        UPDATE = "{0}：{1} 更新"
        NON_UPDATE = "{0}：{1} 更新 排他エラー"

    class Message_Box:
        HAB001I = "削除されたため表示できません。"
        HAB002I = "新規登録が完了しました。"
        HAB003I = "更新が完了しました。"
        HAB004I = "他のユーザーが更新したため、更新に失敗しました。\n画面を再度開きなおしてください。"
        HAB001W = "エラーが発生しました。\n管理者に連絡してください。"
