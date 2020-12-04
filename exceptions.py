class InvalidDateFormatError(Exception):
    """Неверный формат даты. (Пример: 05.12.2020)"""
    pass


class RequestLimitExceededError(Exception):
    """Превышен лимит запросов."""
    pass


class UnknownResponseCodeError(Exception):
    """Получен неизвестный код ответа от внешнего api"""
    pass


class UnknownErrorWhenRequestError(Exception):
    """Неизвестная ошибка при запросе в внешнему api."""
    pass
