from django.core.management import BaseCommand

from appel_crises.mailer import get_delivered_emails
from appel_crises.models import EmailOffset, Signature


class Command(BaseCommand):
    help = "Fetch all the delivered emails and mark them as verified"

    def handle(self, *args, **kwargs):
        """Do the job."""
        limit = 100
        offset = EmailOffset.get_max_offset()
        last_fetched = limit
        counter = 0

        # While there may be emails to mark as verified, do:
        while last_fetched == limit:
            results = get_delivered_emails(offset, limit)

            offset += len(results)
            last_fetched = len(results)

            for (email, date) in results:
                if Signature.mark_email_as_verified(email, date):
                    counter += 1
                else:
                    self.stdout.write(f"Error: email not in the database: {email}")

        EmailOffset(offset=offset).save()
        self.stdout.write(f"Total: verified {counter} emails")
