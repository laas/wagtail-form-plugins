import logging

from django.contrib.auth.models import Permission, Group
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

from wagtail.models import Page

from example.models import FormIndexPage, Team, Service


class Command(BaseCommand):
    help = "Initialize an example database for demonstration."

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("example.commands.init")

    def handle(self, *args, **options):
        if not settings.DEBUG:
            print("This command is only available in debug mode.")
            return

        users = self.init_users("Myra Webster", "Shawn Hobbs", "Lacey Andrade", "Abdiel Rosales")
        form_moderators = self.init_group()
        teams = self.init_teams("Team A", "Team B", "Team C")
        services = self.init_services("Service n°1", "Service n°2", "Service n°3")
        self.init_form_index_page("Forms")

        self.logger.info("\naffecting users to teams and services...")
        teams[0].members.add(users[0], users[1])
        teams[1].members.add(users[2])
        services[0].members.add(users[2], users[3])
        services[1].members.add(users[4])

        self.logger.info("\naffecting users to groups...")
        users[1].groups.add(form_moderators)
        users[2].groups.add(form_moderators)

    def init_users(self, *users_names):
        self.logger.info("\ninitializing users...")
        users = []
        user_model = get_user_model()
        user_model.objects.all().delete()

        self.logger.info("  admin user")
        admin = user_model.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
            first_name="Admin",
            last_name="Admin",
        )
        users.append(admin)

        for user_names in users_names:
            first_name, last_name = user_names.split(" ")
            self.logger.info("  user %s", user_names)
            user = user_model.objects.create_user(
                username=slugify(user_names),
                email=f"{slugify(user_names)}@example.com",
                password="1234",
                first_name=first_name,
                last_name=last_name,
            )
            users.append(user)

        return users

    def init_group(self):
        self.logger.info("\ninitializing permissions...")
        form_moderators, _ = Group.objects.get_or_create(name="Forms moderators")

        for model in ["formpage", "formindexpage", "customformsubmission"]:
            self.logger.info("  on %s", model)
            for permission_verb in ["view", "change", "add", "delete"]:
                permission = Permission.objects.get(codename=f"{permission_verb}_{model}")
                print(permission)
                form_moderators.permissions.add(permission)

        return form_moderators

    def init_teams(self, *teams_name):
        self.logger.info("\ninitializing teams...")
        Team.objects.all().delete()
        teams = []

        for team_name in teams_name:
            self.logger.info("  team %s", team_name)
            team, _ = Team.objects.get_or_create(name=team_name)
            teams.append(team)

        return teams

    def init_services(self, *services_name):
        self.logger.info("\ninitializing services...")
        Service.objects.all().delete()
        services = []

        for service_name in services_name:
            self.logger.info("  service %s", service_name)
            service, _ = Service.objects.get_or_create(name=service_name)
            services.append(service)

        return services

    def init_form_index_page(self, title):
        self.logger.info("\ninitializing form index page...")
        FormIndexPage.objects.all().delete()

        home, _ = Page.objects.get_or_create(slug="home")
        forms_index_page = FormIndexPage(
            title=title,
            slug=slugify(title),
            depth=home.depth + 1,
            locale_id=home.locale_id,
            intro="Here is the list of all published forms.",
        )
        home.add_child(instance=forms_index_page)

        return forms_index_page
