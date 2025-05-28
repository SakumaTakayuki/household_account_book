from db.common.engine import Engine, Return_Info

engine = Engine()
info = Return_Info()
test = engine.create_log("T", "id", "detail", "admin")
print(test)
test = engine.exception_log_exception()
print(test.message_id, test.message_text)
test = engine.exception_log("id", "detail", "admin")
print(test.message_id, test.message_text)
