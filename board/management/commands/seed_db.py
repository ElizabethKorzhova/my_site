"""Database Seeding Management Command.
This module provides the command seed_db for filling the database
with fake data using the faker package."""
import random
from typing import List

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth.models import User
from faker import Faker

from board import models

fake = Faker()
PASSWORD = "12345pass"


class Command(BaseCommand):
    """
    Custom Django management command to seed the database with fake data.
    """
    help = "Generate fake data"

    def add_arguments(self, parser: CommandParser) -> None:
        """Defines the command line arguments."""
        parser.add_argument("--clear", type=bool, default=False, help="Clear database")
        parser.add_argument("--users", type=int, default=20, help="Number of users")
        parser.add_argument("--categories", type=int, default=10, help="Number of categories")
        parser.add_argument("--ads", type=int, default=50, help="Number of ads")
        parser.add_argument("--comments", type=int, default=50, help="Number of comments")

    def handle(self, *args, **options) -> None:
        """Executes the seeding of the database."""
        if options["clear"]:
            models.CustomUser.objects.filter(user__is_superuser=False).delete()
            models.Category.objects.all().delete()

        categories = self.generate_categories(options["categories"])
        users = self.generate_users(options["users"])
        ads = self.generate_ads(options["ads"], categories, users)
        self.generate_comments(options["comments"], ads, users)

    @staticmethod
    def generate_categories(categories_count: int) -> List[models.Category]:
        """
        Generates the specified number of categories.

        Args:
            categories_count (int): number of categories to generate
        Returns:
            List[models.Category]: list of categories
        """
        categories = []
        for _ in range(categories_count):
            categories.append(models.Category.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.text(max_nb_chars=200)
            ))
        return categories

    @staticmethod
    def generate_users(users_count: int) -> List[models.CustomUser]:
        """
        Generates the specified number of users.

        Args:
             users_count (int): number of users to generate
        Returns:
            List[models.CustomUser]: list of users
        """
        users = []
        for _ in range(users_count):
            base_user = User.objects.create(
                username=fake.unique.user_name(),
                password=make_password(PASSWORD)
            )
            users.append(models.CustomUser.objects.create(
                user=base_user,
                phone=fake.unique.msisdn(),
                address=fake.address()
            ))
        return users

    @staticmethod
    def generate_ads(ads_count: int, categories: List[models.Category], users: List[models.CustomUser]) -> List[
        models.Ad]:
        """
        Generates the specified number of ads.

        Args:
            ads_count (int): number of ads to generate
            categories (List[models.Category]): list of categories
            users (List[models.CustomUser]): list of users
        Returns:
            List[models.Ad]: list of ads
        """
        ads = []
        for _ in range(ads_count):
            ads.append(models.Ad.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.text(max_nb_chars=200),
                price=fake.random_int(1, 1000),
                is_active=fake.boolean(chance_of_getting_true=70),
                category=random.choice(categories),
                user=random.choice(users),
            ))
        return ads

    @staticmethod
    def generate_comments(comments_count: int, ads: List[models.Ad], users: List[models.CustomUser]) -> None:
        """
        Generates the specified number of comments.

        Args:
            comments_count (int): number of comments to generate
            ads (List[models.Ad]): list of ads
            users (List[models.CustomUser]): list of users
        """
        for _ in range(comments_count):
            models.Comment.objects.create(
                content=fake.text(max_nb_chars=200),
                ad=random.choice(ads),
                user=random.choice(users),
            )
