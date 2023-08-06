from autosolveclient.autosolve import AutoSolve

try:
    auto_solve_factory = AutoSolve({
        "access_token": "30144-f3fd90d2-eba6-4c9a-964d-57f3c3f118e8",
        "api_key": "c52c4db5-233a-4e00-96bc-f35945073228",
        "client_key": "Testing-32f4dd15-11a9-4b4b-97f3-5f3b94063609",
        "debug": True,
        "should_alert_on_cancel": True
    })

    auto_solve = auto_solve_factory.get_instance()
    auto_solve.init()
    finished = auto_solve.initialized()

    message = {
        "taskId": 6,
        "url": "https://recaptcha.autosolve.io/version/1",
        "siteKey": "6Ld_LMAUAAAAAOIqLSy5XY9-DUKLkAgiDpqtTJ9b",
        "version": 0,
        "minScore": 0,
    }

    auto_solve.send_token_request(message)
except Exception as s:
    print(s)

