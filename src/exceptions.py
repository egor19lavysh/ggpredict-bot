"""Кастомные исключения приложения"""


class MessageLimitExceeded(Exception):
    pass


class MessageNotFound(Exception):
    pass