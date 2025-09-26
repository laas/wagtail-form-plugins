"Define the `init` Django command used to initialize an example database for demonstration."

import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from wagtail.models import Page

from demo.models import FormIndexPage


class Command(BaseCommand):
    """The management command class."""

    help = "Initialize an example database for demonstration."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("demo.commands.init")

    def handle(self, *args, **options) -> None:
        """The actual logic of the "init" command."""
        if not settings.DEBUG:
            print("This command is only available in debug mode.")
            return

        self.init_pages()
        self.init_users("Myra Webster", "Shawn Hobbs", "Lacey Andrade", "Abdiel Rosales")
        self.init_groups(["myra-webster", "shawn-hobbs"])

    def init_pages(self) -> None:
        """Initialize Wagtail pages."""
        self.logger.info("\ninitializing pages...")

        Page.objects.exclude(slug="root").exclude(slug="home").delete()

        home_page = Page.objects.get(slug="home")
        FormIndexPage.create_if_missing(home_page, self.stdout)

    def init_users(self, *users_names) -> None:
        """Initialize users."""
        self.logger.info("\ninitializing users...")

        User: AbstractUser = get_user_model()  # type: ignore # noqa: N806
        User.objects.all().delete()

        self.logger.info("  admin user")
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
            first_name="Admin",
            last_name="Admin",
        )

        for user_names in users_names:
            first_name, last_name = user_names.split(" ")
            self.logger.info("  user %s", user_names)
            User.objects.create_user(
                username=slugify(user_names),
                email=f"{slugify(user_names)}@example.com",
                password="1234",
                first_name=first_name,
                last_name=last_name,
            )

    def init_groups(self, moderator_usernames: list[str]) -> None:
        """Initialize user groups."""
        self.logger.info("\ninitializing groups...")

        access_admin = Permission.objects.get(codename="access_admin")
        Group.objects.exclude(name="Moderators").delete()

        moderators = Group.objects.get(name="Moderators")
        for permission in moderators.permissions.all():
            moderators.permissions.remove(permission)
        moderators.permissions.add(access_admin)

        everyone = Group.objects.create(name="Everyone")
        everyone.permissions.add(access_admin)

        self.logger.info("\naffecting users to groups...")

        User: AbstractUser = get_user_model()  # type: ignore # noqa: N806
        for username in moderator_usernames:
            User.objects.get(username=username).groups.add(moderators)

        for user in User.objects.all():
            user.groups.add(everyone)
