from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated

from .models import Listing
from .serializers import ListingSerializer
from .permissions import IsOwnerOrReadOnly


def home(request):
    """
    Главная страница сайта (шаблонный view).

    Показывает последние опубликованные объявления (до 50 штук).
    """
    listings = Listing.objects.filter(status="published")[:50]
    return render(request, "home.html", {"listings": listings})


class ListingListView(ListAPIView):
    """
    Список опубликованных объявлений.

    - Возвращает только объявления со статусом published
    - Оптимизирован запросами: select_related + prefetch_related
    - Поддерживает фильтрацию через django-filter
    """

    serializer_class = ListingSerializer
    queryset = (
        Listing.objects
        .filter(status="published")
        .select_related(
            "city", "make", "car_model", "generation",
            "body_type", "fuel_type", "transmission",
            "drive_type", "color"
        )
        .prefetch_related("features")
    )

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "make", "car_model", "city",
        "body_type", "fuel_type", "transmission",
        "drive_type", "color"
    ]


class ListingCreateView(CreateAPIView):
    """
    Создание объявления.

    Доступно только авторизованным пользователям.
    Владелец объявления (user) проставляется автоматически
    из request.user.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Сохраняет объявление и привязывает его к текущему пользователю.
        """
        serializer.save(user=self.request.user)


class ListingDetailView(RetrieveAPIView):
    """
    Детальная информация об объявлении.

    Используется оптимизация запросов (select_related/prefetch_related).
    Доступ ограничен разрешением IsOwnerOrReadOnly:
    - читать может любой (GET)
    - изменять/удалять — только владелец
    """

    queryset = (
        Listing.objects
        .all()
        .select_related(
            "city", "make", "car_model", "generation",
            "body_type", "fuel_type", "transmission",
            "drive_type", "color"
        )
        .prefetch_related("features")
    )
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ListingUpdateView(UpdateAPIView):
    """
    Обновление объявления.

    Изменять может только владелец (IsOwnerOrReadOnly).
    """

    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Listing.objects.all()


class ListingDeleteView(DestroyAPIView):
    """
    Удаление объявления.

    Удалять может только владелец (IsOwnerOrReadOnly).
    """

    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Listing.objects.all()


class MyListingsView(ListAPIView):
    """
    Список объявлений текущего пользователя.

    Доступно только авторизованным пользователям.
    Возвращает объявления, где user = request.user.
    """

    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает queryset объявлений текущего пользователя
        с оптимизацией select_related/prefetch_related.
        """
        return (
            Listing.objects
            .filter(user=self.request.user)
            .select_related("city", "make", "car_model")
            .prefetch_related("features")
        )
