from django.utils import timezone
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from plant.notifications.models import Notification
from plant.users.tests.factories import UserFactory


class NotificationFactory(DjangoModelFactory):
    text = Faker("word")
    is_read = Faker("boolean")
    is_sent = Faker("boolean")
    recipient = SubFactory(UserFactory)
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Notification
