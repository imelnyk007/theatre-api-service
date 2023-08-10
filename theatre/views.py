from django.db.models import F, Count
from rest_framework import filters
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from theatre.filters import PlayFilter, PerformanceFilter
from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Reservation
)
from theatre.pagination import ReservationPagination
from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.serializers import (
    GenreSerializer,
    ActorSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    ReservationCreateSerializer,
    ReservationListSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_class = PlayFilter

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("genres", "actors")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return self.serializer_class


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    filterset_class = PerformanceFilter
    ordering_fields = ["show_time"]

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ("list", "retrieve"):
            queryset = (
                queryset
                .select_related("play", "theatre_hall")
                .annotate(available_tickets=(
                    F("theatre_hall__rows")
                    * F("theatre_hall__seats_in_row")
                    - Count("tickets")
                ))
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return self.serializer_class


class ReservationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Reservation.objects.all()
    serializer_class = ReservationListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["show_time"]
    pagination_class = ReservationPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("tickets", "tickets__performance")

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ReservationCreateSerializer
        return ReservationListSerializer
