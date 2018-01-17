import json
ERROR_MSG = "ERROR"
UPDATE_MSG = "UPDATE"
WINNER = "winner"


class Message(object):
    MESSAGE_TYPE = None

    def __init__(self, content):
        self.content = content

    def to_json(self):
        return json.dumps(
            {
                "message_type": self.MESSAGE_TYPE,
                "content": self.content
            }
        )

    @classmethod
    def from_json(cls, content_dict):
        if content_dict.get("message_type") != cls.MESSAGE_TYPE or content_dict.get("content") is None:
            raise ValueError("illegal message format: %s" % str(content_dict))
        return cls(content_dict["content"])


# class ErrorMessage(Message):
#     MESSAGE_TYPE = "error"
#
#
# class UpdateMessage(Message):
#     MESSAGE_TYPE = "update"
#
#     @property
#     def coordinates(self):
#         i, j = self.content.split(",")
#         return int(i), int(j)

#
# class WinnerMessage(Message):
#     MESSAGE_TYPE = "winner"
#
#     @property
#     def winner(self):
#         return self.content


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
            client_choice_handler(message.content)

        self.__communicator.bind_action_to_message(__handle_client_message)

    def send_choice(self, column):
        self.send_message(ChoiceMessage(str(column)))

    # def send_winner(self, winner):
    #     message = WinnerMessage(winner)
    #     self.send_message(message)
    #
    # def send_error(self, error_msg):
    #     message = ErrorMessage(error_msg)
    #     self.send_message(message)
    #
    # def send_board_state(self, game):
    #     board = {}
    #     for i in range(game.ROWS):
    #         for j in range(game.COLUMNS):
    #             board[(i, j)] = game.get_player_at(i, j)
    #     message = UpdateMessage(board)
    #     self.send_message(message)
    #

# class ClientCommunicationHandler(SocketCommunicatorHandler):
#     def __init__(self, *args, **kwargs):
#         super(ClientCommunicationHandler, self).__init__(*args, **kwargs)
#
#     def set_server_answer_handler(self, server_answer_handler):
#         def handler_wrapper(message):
#             message_options = [UpdateMessage, ErrorMessage, WinnerMessage]
#             for message_option in message_options:
#                 try:
#                     message =  message_option.from_json(message)
#                     server_answer_handler(message)
#                     return
#                 except ValueError:
#                     pass
#             raise ValueError("illegal message format: %s" % message)
#         return self.__communicator.bind_action_to_message(handler_wrapper)
