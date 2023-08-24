import datetime
from django.utils import timezone

import django_filters

from theatre.models import Play, Actor, Genre, Performance


class PlayFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all()
    )
    actors = django_filters.ModelMultipleChoiceFilter(
        queryset=Actor.objects.all()
    )

    class Meta:
        model = Play
        fields = ["title", "genres", "actors"]


class DateRangeFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value:
            today = timezone.now().date()
            end_date = today + datetime.timedelta(days=int(value))
            qs = qs.filter(show_time__date__range=[today, end_date])
        return qs


class PerformanceFilter(django_filters.FilterSet):
    date_range = DateRangeFilter(
        field_name="show_time",
        lookup_expr="date"
    )
    play = django_filters.CharFilter(
        field_name="play__title",
        lookup_expr="icontains"
    )

    class Meta:
        model = Performance
        fields = ["date_range", "play"]
