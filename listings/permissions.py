from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее редактировать объект
    только его владельцу.

    - Безопасные методы (GET, HEAD, OPTIONS) разрешены всем
    - Изменение и удаление разрешены только владельцу объекта
    """

    def has_object_permission(self, request, view, obj):
        """
        Проверяет права доступа к конкретному объекту.

        :param request: HTTP-запрос
        :param view: представление
        :param obj: объект, к которому осуществляется доступ
        :return: True, если доступ разрешён, иначе False
        """
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
