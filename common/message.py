# メッセージ一覧
class Message:

    # 処理ID用
    class Log_Function_Id:
        id = "{0}-{1}-{2}"

    # ログ詳細用
    class Log_Message:
<<<<<<< HEAD
        FILL = "{0}：{1} 取得 {2}件"
        Fill_NO_ROW = "{0}：{1} 取得 0件"
        INSERT = "{0}：{1} 追加"
        UPDATE = "{0}：{1} 更新"
        NON_UPDATE = "{0}：{1} 更新 排他エラー"
=======
        LOGIN = "ログイン画面 users：{0} 取得 {1}件"
        LOGIN_SUCCESS = "ログイン画面 users：{0} 取得 {1}件 認証成功"
        LOGIN_ERROR = "ログイン画面 users：{0} 取得 {1}件 認証失敗"
        FILL = "{0}画面 {1}：{2} 取得 {3}件"
        Fill_NO_ROW = "{0}画面 {1}：{2} 取得 0件"
        INSERT = "{0}画面 {1}：{2} 追加"
        NON_INSERT = "{0}画面 {1}：{2} 追加 ID重複"
        UPDATE = "{0}画面 {1}：{2} 更新"
        NON_UPDATE = "{0}画面 {1}：{2} 更新 排他エラー"
        DELETE = "{0}画面 {1}：{2} 削除"
        NON_DELETE = "{0}画面 {1}：{2} 削除 排他エラー"
>>>>>>> 5ef5402 (【message】ログイン画面のメッセージ内容追加)

    # メッセージボックス用
    class Message_Box:
        # INFO
        HAB001I = "新規登録が完了しました。"
        HAB002I = "更新が完了しました。"
        # CAUTION
        HAB001C = "削除されたため表示できません。"
        HAB002C = "同じユーザーIDのユーザーが存在します。\nユーザーIDを変更して登録してください。"
        HAB003C = "他のユーザーが更新したため、更新に失敗しました。\n画面を再度開きなおしてください。"
        HAB004C = "{0}に失敗しました。"
        HAB005C = "{0}を入力してください。"
        # WARNING
        HAB001W = (
            "ログファイル作成時にエラーが発生しました。\n管理者に連絡してください。"
        )
        HAB002W = (
            "データベース操作時にエラーが発生しました。\n管理者に連絡してください。"
        )
