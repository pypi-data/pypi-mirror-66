import pika, requests, threading, json, time
from logzero import logger
from pymitter import EventEmitter
from autosolveclient.autosolveconstants import AutoSolveConstants


class AutoSolve:

    def __init__(self, params):
        self.autosolve_constants = AutoSolveConstants()
        self.emitter = EventEmitter()

        self.access_token = params["access_token"]
        self.api_key = params["api_key"]
        self.client_key = params["client_key"]
        self.debug = params["debug"]
        self.should_alert_on_cancel = params["should_alert_on_cancel"]
        self.manual_reconnect = params["manual_reconnect"]

        self.routing_key = self.api_key.replace("-", "")
        self.send_routing_key = self.access_token.replace("-", "")

        self.account_id = self.access_token.split("-")[0]
        self.vhost = self.autosolve_constants.VHOST

        self.directExchangeName = self.build_with_account_id(self.autosolve_constants.DIRECT_EXCHANGE)
        self.fanoutExchangeName = self.build_with_account_id(self.autosolve_constants.FANOUT_EXCHANGE)

        self.receiver_queue_name = self.build_prefix_with_credentials(self.autosolve_constants.RECEIVER_QUEUE_NAME)

        self.routing_key_receiver = self.build_prefix_with_credentials(self.autosolve_constants.TOKEN_RECEIVE_ROUTE)
        self.routing_key_cancel = self.build_prefix_with_credentials(self.autosolve_constants.CANCEL_RECEIVE_ROUTE)

        self.token_send_routing_key = self.build_with_access_token(self.autosolve_constants.TOKEN_SEND_ROUTE)
        self.cancel_send_routing_key = self.build_with_access_token(self.autosolve_constants.CANCEL_SEND_ROUTE)

        self.connection = None
        self.channel = None
        self.cancel_channel = None
        self.consumer_thread = None
        self.ready = False
        self.connected = False

        self.message_backlog = []

    def initialized(self):
        while True:
            time.sleep(.5)
            if self.ready:
                break
        return True

    def init(self):
        if self.manual_reconnect is None:
            self.manual_reconnect = False
        if self.check_input_values():
            self.begin_connection()

    def begin_connection(self):
        self.consumer_thread = threading.Thread(target=self.connect)
        valid = self.validate_connection()
        if valid == 400:
            self.log(self.autosolve_constants.INVALID_CLIENT_KEY, self.autosolve_constants.ERROR)
            raise AuthException(self.autosolve_constants.INVALID_CLIENT_KEY)
        if valid == 401:
            self.log(self.autosolve_constants.INVALID_API_KEY_OR_ACCESS_TOKEN, self.autosolve_constants.ERROR)
            raise AuthException(self.autosolve_constants.INVALID_API_KEY_OR_ACCESS_TOKEN)
        else:
            self.log("Validation complete", self.autosolve_constants.SUCCESS)
            self.consumer_thread.start()

    def connect(self):
        self.log("Beginning connection establishment", self.autosolve_constants.STATUS)

        credentials = pika.PlainCredentials(self.account_id, self.access_token)
        parameters = pika.ConnectionParameters(host=self.autosolve_constants.HOSTNAME,
                                               port=5672,
                                               virtual_host=self.vhost,
                                               credentials=credentials,
                                               connection_attempts=50,
                                               blocked_connection_timeout=60)
        try:
            self.connected = self.establish_connection(parameters) \
                             and self.create_channels() \
                             and self.register_response_queue()

            if self.connected:
                self.log("Beginning message consumption", self.autosolve_constants.SUCCESS)
                self.ready = True
                self.channel.start_consuming()
            else:
                self.log("Error with RabbitMQ connection, attempting to re-establish", self.autosolve_constants.WARNING)

        except pika.exceptions.AMQPConnectionError or pika.exceptions.ConnectionClosedByBroker:
            self.log("Error with RabbitMQ connection, attempting to re-establish", self.autosolve_constants.WARNING)
            self.emitter.emit("AutoSolveError", self.autosolve_constants.CONNECTION_ERROR_INIT)
            self.handle_connection_error()
        except Exception:
            self.log("Unknown error occured during connection. Aborting", self.autosolve_constants.ERROR)
            self.emitter.emit("AutoSolveError", self.autosolve_constants.CONNECTION_ERROR_INIT)

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()

    def establish_connection(self, parameters):
        self.log("Attempting connection establishment", self.autosolve_constants.STATUS)

        try:
            self.connection = pika.BlockingConnection(parameters)
        except Exception:
            self.log("Connection Exception", self.autosolve_constants.ERROR)

        self.log("Connection established", self.autosolve_constants.SUCCESS)
        return True

    def create_channels(self):
        self.log("Creating channel", self.autosolve_constants.STATUS)
        self.channel = self.connection.channel()
        self.cancel_channel = self.connection.channel()

        self.log("Channels created", self.autosolve_constants.SUCCESS)
        return True

    def register_response_queue(self):
        try:
            self.log("Binding queue to exchange", self.autosolve_constants.STATUS)
            self.channel.queue_bind(queue=self.receiver_queue_name,
                                    exchange=self.directExchangeName,
                                    routing_key=self.routing_key_receiver)
            self.channel.queue_bind(queue=self.receiver_queue_name,
                                    exchange=self.directExchangeName,
                                    routing_key=self.routing_key_cancel)
            self.log("Queue binded to exchange " + self.directExchangeName,
                     self.autosolve_constants.SUCCESS)
            self.channel.basic_consume(queue=self.receiver_queue_name, auto_ack=self.autosolve_constants.AUTO_ACK,
                                       on_message_callback=self.receive_message)
            return True
        except pika.exceptions.ChannelClosedByBroker:
            self.emitter.emit("AutoSolveError", self.autosolve_constants.CONNECTION_ERROR_INIT)

    def receive_message(self, channel, method_frame, header_frame, body):
        if method_frame.routing_key == self.routing_key_receiver:
            self.on_receiver_message(channel, method_frame, header_frame, body)
        else:
            self.on_cancel_message(channel, method_frame, header_frame, body)

    def on_receiver_message(self, channel, method_frame, header_frame, body):
        json_string = "".join(chr(x) for x in body)
        self.log("Message Received: " + json_string, self.autosolve_constants.SUCCESS)
        self.emitter.emit("AutoSolveResponse", json_string)

    def on_cancel_message(self, channel, method_frame, header_frame, body):
        json_string = "".join(chr(x) for x in body)
        self.log("Message Received: " + json_string, self.autosolve_constants.SUCCESS)
        self.emitter.emit("AutoSolveResponse_Cancel", json_string)

    def handle_connection_error(self):
        self.connected = False
        if (self.manual_reconnect):
            self.emitter.emit("AutoSolveError", self.autosolve_constants.CONNECTION_LOST_ERROR)
        else:
            while True:
                try:
                    self.connect()
                except pika.exceptions.ConnectionClosedByBroker:
                    break
                except pika.exceptions.AMQPConnectionError:
                    continue

            if self.connected:
                self.log("Connection attempt successful, sending any unsent messages", self.autosolve_constants.SUCCESS)
                self.attempt_message_backlog_send()
            else:
                self.log("Connection attempts unsuccessful", self.autosolve_constants.ERROR)
                self.emitter.emit("AutoSolveError", self.autosolve_constants.CONNECTION_REESTABLISH_FAILED)

    def send(self, message, route, exchange):
        message["createdAt"] = round(time.time())
        message["apiKey"] = self.api_key
        message_string = json.dumps(message)
        byte_string = message_string.encode()
        if self.fanoutExchangeName == exchange:
            return self.cancel_channel.basic_publish(exchange=exchange,
                                            routing_key=route,
                                            body=byte_string)
        return self.channel.basic_publish(exchange=exchange,
                                          routing_key=route,
                                          body=byte_string)

    def send_token_request(self, message):
        self.log("Sending request message for task: " + message['taskId'], self.autosolve_constants.STATUS)
        try:
            send_result = self.send(message, self.token_send_routing_key,
                                    self.directExchangeName)
            if send_result is None:
                self.log("Message with TaskId: " + message['taskId'] + " sent successfully",
                         self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.token_send_routing_key, self.directExchangeName)

    def cancel_token_request(self, taskId):
        message = dict()
        message["taskId"] = taskId
        message["responseRequired"] = self.should_alert_on_cancel

        self.log("Sending cancel message for task: " + message['taskId'], self.autosolve_constants.STATUS)
        try:
            send_result = self.send(message, self.cancel_send_routing_key,
                                    self.fanoutExchangeName)
            if send_result is None:
                self.log("Cancel message with TaskId: " + message['taskId'] + " sent successfully",
                         self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.cancel_send_routing_key, self.fanoutExchangeName)

    def cancel_all_requests(self):
        message = {"apiKey": self.api_key}
        self.log("Sending cancel all request for api key ::  " + message['apiKey'], self.autosolve_constants.STATUS)
        try:
            send_result = self.send(message, self.cancel_send_routing_key,
                                    self.fanoutExchangeName)
            if send_result is None:
                self.log("Cancel all requests sent successfully", self.autosolve_constants.SUCCESS)
        except Exception as e:
            self.log(e, self.autosolve_constants.WARNING)
            self.resend(message, self.cancel_send_routing_key, self.fanoutExchangeName)

    def resend(self, message, route, exchange):
        time.sleep(5)
        result = self.send(message, route, exchange)
        if result is None:
            self.log("Resend attempt successful", self.autosolve_constants.SUCCESS)
        else:
            self.log("Attempt to resend after wait unsuccessful. Pushing message to backlog",
                     self.autosolve_constants.WARNING)
            self.add_message_to_backlog({"message": message, "route": route, "exchange": exchange})

    def add_message_to_backlog(self, message):
        self.message_backlog.append(message)

    def attempt_message_backlog_send(self):
        self.log("Sending messages from backlog", self.autosolve_constants.STATUS)
        message_cache = self.message_backlog
        for message in message_cache:
            result = self.send(message["message"], message["route"], message["exchange"])
            if result is None:
                self.message_backlog.remove(message)

    ## VALIDATION FUNCTIONS ##

    def check_input_values(self):
        if self.validate_inputs():
            return True
        else:
            self.log(self.autosolve_constants.INPUT_VALUE_ERROR, self.autosolve_constants.ERROR)
            raise InputValueException(self.autosolve_constants.INPUT_VALUE_ERROR)

    def validate_inputs(self):
        valid_access_token = self.validate_access_token()
        valid_client_key = self.client_key is not None
        valid_api_key = self.api_key is not None

        return valid_access_token and valid_client_key and valid_api_key

    def validate_access_token(self):
        if self.access_token is None:
            return False

        access_token_split = self.access_token.split("-")
        username_valid = access_token_split[0].isdigit()

        if username_valid is not True:
            return False

        return True

    def validate_connection(self):
        self.log("Validating input values with AutoSolve API", self.autosolve_constants.STATUS)
        url = "https://dashboard.autosolve.io/rest/" + self.access_token + "/verify/" + self.api_key + "?clientId=" + self.client_key
        response = requests.get(url)
        return response.status_code

    def build_prefix_with_credentials(self, prefix):
        return prefix + "." + self.account_id + "." + self.routing_key

    def build_with_access_token(self, prefix):
        return prefix + "." + self.send_routing_key

    def build_with_account_id(self, prefix):
        return prefix + "." + self.account_id

    def log(self, message, type):
        if type == self.autosolve_constants.ERROR:
            logger.error(message)
        if type == self.autosolve_constants.WARNING:
            logger.warning(message)
        if self.debug:
            if type == self.autosolve_constants.STATUS:
                logger.debug(message)
            if type == self.autosolve_constants.SUCCESS:
                logger.info(message)


class AuthException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'AuthException: {}'.format(self.value)


class InputValueException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'InputValueException: {}'.format(self.value)
