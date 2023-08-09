from django.conf import settings
from django.db import models
from rest_framework.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)

    def __str__(self):
        return self.title


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE, related_name="performances")
    show_time = models.DateTimeField()

    @staticmethod
    def validate_show_time(show_time, minimum_show_time, error_to_raise):
        if not (show_time >= minimum_show_time):
            raise error_to_raise(
                {
                    "Show time":
                        f"Show time can't be in past date"
                }
            )


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name="tickets")

    @staticmethod
    def validate_seat(seat_value, maximal_seat_capacity, error_to_raise):
        if not (1 <= seat_value <= maximal_seat_capacity):
            raise error_to_raise(
                {
                    "Seats":
                        f"Seat number must be in available range: "
                        f"(1, {maximal_seat_capacity})"
                }
            )

    @staticmethod
    def validate_row(row_value, maximal_row_capacity, error_to_raise):
        if not (1 <= row_value <= maximal_row_capacity):
            raise error_to_raise(
                {
                    "Rows":
                        f"Row number must be in available range: "
                        f"(1, {maximal_row_capacity})"
                }
            )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None,
    ):
        self.full_clean()
        super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("performance", "row", "seat")
