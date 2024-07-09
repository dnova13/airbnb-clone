from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    help = "This command creates superuser"

    def handle(self, *args, **options):
        
        adminId="admin"
        adminPW="1q2w3e4r"
        adminMail="testnova0713@gmail.com"
        
        admin = User.objects.get_or_none(username=adminId)
        
        if not admin:
            User.objects.create_superuser(
                adminId, adminMail, adminPW
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser Created"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser Exists"))
