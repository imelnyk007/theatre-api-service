from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import Play, Genre, Actor, TheatreHall, Performance
from theatre.serializers import PlayListSerializer, PlayDetailSerializer

PlAY_URL = reverse("theatre:play-list")
PERFORMANCE_URL = reverse("theatre:performance-list")


def sample_play(**params):
    defaults = {
        "title": "Sample movie",
        "description": "Sample description",
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Drama",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "George", "last_name": "Clooney"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_performance(**params):
    theatre_hall = TheatreHall.objects.create(
        name="Blue", rows=20, seats_in_row=20
    )

    defaults = {
        "show_time": "2022-06-02 14:00:00",
        "play": None,
        "theatre_hall": theatre_hall,
    }
    defaults.update(params)

    return Performance.objects.create(**defaults)


def detail_url(play_id):
    return reverse("theatre:play-detail", args=[play_id])


class UnauthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PlAY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="1qazcde3"
        )

        self.client.force_authenticate(self.user)

    def test_list_play(self):
        play1 = sample_play()
        play2 = sample_play()

        genre = sample_genre()
        actors = sample_actor()

        play1.genres.add(genre)
        play2.actors.add(actors)

        res = self.client.get(PlAY_URL)
        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_detail_play(self):
        play = sample_play()
        play.genres.add(sample_genre())
        play.actors.add(sample_actor())

        serializer = PlayDetailSerializer(play)

        url = detail_url(play.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        movie_data = {
            "title": "Test1",
            "description": "Test",
        }

        res = self.client.post(PlAY_URL, movie_data)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminPlayApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="1qazcde3",
            is_staff=True
        )

        self.client.force_authenticate(self.user)

    def test_create_play(self):
        play_data = {
            "title": "Test1",
            "description": "Test",
        }

        res = self.client.post(PlAY_URL, play_data)
        play = Play.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in play_data:
            self.assertEqual(play_data[key], getattr(play, key))

    def test_create_play_with_gender_and_actor(self):
        genre = sample_genre()
        actor = sample_actor()

        play_data = {
            "title": "Test1",
            "description": "Test",
            "genres": [genre.id],
            "actors": [actor.id]
        }

        res = self.client.post(PlAY_URL, play_data)
        play = Play.objects.get(id=res.data["id"])
        actors = play.actors.all()
        genres = play.genres.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(actors.count(), 1)
        self.assertEqual(genres.count(), 1)
        self.assertIn(actor, actors)
        self.assertIn(genre, genres)
