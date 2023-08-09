from django.contrib import admin

from theatre.models import Genre, Actor, Play, TheatreHall, Performance, Ticket, Reservation

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Play)
admin.site.register(TheatreHall)
admin.site.register(Performance)
admin.site.register(Ticket)
admin.site.register(Reservation)
