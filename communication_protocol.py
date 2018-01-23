import json

ERROR_MSG = "ERROR"
UPDATE_MSG = "UPDATE"
WINNER = "winner"

MESSAGE_TYPE_TITLE = "message_type"
CONTENT_TITLE = "content"
ILLEGAL_MESSAGE_ERR = "illegal message format: %s"


class Message(object):
    MESSAGE_TYPE = None

    def __init__(self, content):
        self.content = content

    def to_json(self):
        return json.dumps(
            {
                MESSAGE_TYPE_TITLE: self.MESSAGE_TYPE,
                CONTENT_TITLE: self.content
            }
        )

    @classmethod
    def from_json(cls, content):
        content_dict = json.loads(content)
        if content_dict.get(MESSAGE_TYPE_TITLE) != cls.MESSAGE_TYPE or content_dict.get(CONTENT_TITLE) is None:
            raise ValueError(ILLEGAL_MESSAGE_ERR  % str(content_dict))
        return cls(content_dict[CONTENT_TITLE])


class ChoiceMessage(Message):
    MESSAGE_TYPE = "choice"
    
    @property
    def column(self):
        return int(self.content)


class SocketCommunicatorHandler(object):
    def __init__(self, communicator):
        self.__communicator = communicator

    def send_message(self, message):
        self.__communicator.send_message(message.to_json())

    def set_client_choice_handler(self, client_choice_handler):
        def __handle_client_message(client_message):
            message = ChoiceMessage.from_json(client_message)
            client_choice_handler(message.column)

        self.__communicator.bind_action_to_message(__handle_client_message)

    def send_choice(self, column):
        self.send_message(ChoiceMessage(str(column)))

