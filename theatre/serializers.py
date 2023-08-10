import datetime

from django.db import transaction
from pytz import utc
from rest_framework import serializers

from theatre.models import (
    Genre,
    Actor,
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "poster")


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors", "poster")


class PlayPosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "poster")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ("id", "play", "theatre_hall", "show_time")

    def validate(self, attrs):
        data = super(PerformanceSerializer, self).validate(attrs)
        show_time_value = attrs["show_time"].replace(tzinfo=utc)
        print(show_time_value)
        minimum_show_time = datetime.datetime.now().replace(tzinfo=utc)
        print(minimum_show_time)
        Performance.validate_show_time(
            show_time_value, minimum_show_time, serializers.ValidationError
        )

        return data


class PerformanceListSerializer(PerformanceSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name",
        read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity",
        read_only=True
    )
    available_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "available_tickets",
            "show_time"
        )


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer()
    theatre_hall = TheatreHallSerializer()


class PerformanceReservationSerializer(PerformanceListSerializer):
    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "theatre_hall_name",
            "show_time"
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        row_value = attrs["row"]
        maximal_row_capacity = attrs["performance"].theatre_hall.rows
        Ticket.validate_row(
            row_value, maximal_row_capacity, serializers.ValidationError
        )

        seat_value = attrs["seat"]
        maximal_seat_capacity = attrs["performance"].theatre_hall.seats_in_row
        Ticket.validate_seat(
            seat_value, maximal_seat_capacity, serializers.ValidationError
        )

        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance")


class TicketListSerializer(TicketSerializer):
    performance = PerformanceReservationSerializer(many=False, read_only=True)


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")


class ReservationCreateSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")
