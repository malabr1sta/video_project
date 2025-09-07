from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
import random

from accounts import models as accounts_models
from videos import models as videos_models


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей и опубликованные видео"

    def add_arguments(self, parser):
        parser.add_argument(
            "--users",
            type=int,
            default=10_000,
        )
        parser.add_argument(
            "--videos",
            type=int,
            default=100_000,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker()
        num_users = options["users"]
        num_videos = options["videos"]

        self.stdout.write(f"Создаём {num_users} пользователей...")
        users = [
            accounts_models.User(username=f"user_{i}_{fake.user_name()}")
            for i in range(num_users)
        ]
        accounts_models.User.objects.bulk_create(users, batch_size=1000)

        user_ids = list(
            accounts_models.User.objects.values_list("id", flat=True)
        )

        self.stdout.write(f"Создаём {num_videos} видео...")
        videos = [
            videos_models.Video(
                name=fake.sentence(nb_words=5),
                owner_id=random.choice(user_ids),
                is_published=True,
            )
            for _ in range(num_videos)
        ]
        videos_models.Video.objects.bulk_create(videos, batch_size=1000)

        self.stdout.write("Данные успешно созданы.")
