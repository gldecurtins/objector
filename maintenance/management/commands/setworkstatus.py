from django.core.management.base import BaseCommand
from maintenance.models import Work


class Command(BaseCommand):
    help = "Sets the status of all work records"

    def handle(self, *args, **options):
        work_records = Work.objects.all()
        for work in work_records:
            new_work_status = Work.get_new_work_status(work)

            if work.status != new_work_status:
                work.status = new_work_status
                work.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        'Successfully updated work record "{0}" status to "{1}"'
                    ).format(work.id, work.status)
                )
