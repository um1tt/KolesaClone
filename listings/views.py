from django.shortcuts import render
from .models import Listing

def home(request):
    listings = Listing.objects.filter(status="published")[:50]
    return render(request, "home.html", {"listings": listings})


from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import ListingSerializer
from .permissions import IsOwnerOrReadOnly


class ListingListView(ListAPIView):
    serializer_class = ListingSerializer

    queryset = Listing.objects.filter(status='published').select_related(
        'city', 'make', 'car_model', 'generation',
        'body_type', 'fuel_type', 'transmission',
        'drive_type', 'color'
    ).prefetch_related('features')

    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        'make', 'car_model', 'city',
        'body_type', 'fuel_type', 'transmission',
        'drive_type', 'color'
    ]


class ListingCreateView(CreateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListingDetailView(RetrieveAPIView):
    queryset = Listing.objects.all().select_related(
        'city', 'make', 'car_model', 'generation',
        'body_type', 'fuel_type', 'transmission',
        'drive_type', 'color'
    ).prefetch_related('features')

    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]


class ListingUpdateView(UpdateAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Listing.objects.all()


class ListingDeleteView(DestroyAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Listing.objects.all()


class MyListingsView(ListAPIView):
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Listing.objects.filter(user=self.request.user).select_related(
            'city', 'make', 'car_model'
        ).prefetch_related('features')
