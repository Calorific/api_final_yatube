from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_messages = {
            status.HTTP_400_BAD_REQUEST: 'Неверные данные',
            status.HTTP_401_UNAUTHORIZED: 'Данные не были предоставлены',
            status.HTTP_403_FORBIDDEN: 'У вас нет прав на это действие',
            status.HTTP_404_NOT_FOUND: 'Страница не найдена',
            status.HTTP_405_METHOD_NOT_ALLOWED: 'Метод не разрешен',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Ошибка сервера'
        }

        if response.status_code in custom_messages:
            response.data = {'detail': custom_messages[response.status_code]}

    return response
