from django.core.management.base import BaseCommand

from ...utils import get_random_url_password


class Command(BaseCommand):
    help = "Generates a random password that can be safely used in a URL."
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument("num", default=1, nargs="?", type=int, help="Number of passwords to generate.")
        parser.add_argument("--length", default=50, dest="length", type=int, help="Password length.")

    def handle(self, *args, **options):
        for i in range(0, options["num"]):
            password = get_random_url_password(length=options["length"])
            self.stdout.write(password)
