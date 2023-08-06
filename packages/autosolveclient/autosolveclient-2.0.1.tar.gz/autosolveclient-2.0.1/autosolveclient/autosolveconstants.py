class AutoSolveConstants:
    #NAMES
    HOSTNAME = "rabbit.autosolve.io"
    VHOST = "oneclick"
    DIRECT_EXCHANGE = "exchanges.direct"
    FANOUT_EXCHANGE = "exchanges.fanout"
    RECEIVER_QUEUE_NAME = "queues.response.direct"

    #ROUTES
    TOKEN_SEND_ROUTE = "routes.request.token"
    CANCEL_SEND_ROUTE = "routes.request.token.cancel"
    TOKEN_RECEIVE_ROUTE = "routes.response.token"
    CANCEL_RECEIVE_ROUTE = "routes.response.token.cancel"

    #CONFIG
    AUTO_DELETE = False
    DURABLE = True
    AUTO_ACK = True
    EXCLUSIVE = False

    #ERRORS
    INVALID_CLIENT_KEY = "Invalid Client Key"
    INVALID_API_KEY_OR_ACCESS_TOKEN = "Invalid API or Access Key"
    INPUT_VALUE_ERROR = "Input value for access_token is invalid or client_key/api_key are not set"
    CONNECTION_LOST_ERROR = "Connection lost, manual recovery expected"
    CONNECTION_REESTABLISH_FAILED = "Connection could not be re-established"
    CONNECTION_ERROR_INIT = "Connection error when initializing. Please retry"

    #STATUS
    SUCCESS = "info"
    WARNING = "warning"
    ERROR = "error"
    STATUS = "status"