from datetime import datetime

from django.db import models
from django.db.models import Max
from django.utils import timezone


class Signature(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email_sent_at = models.DateTimeField(null=True, blank=True, db_index=True)
    verified_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.first_name} {self.surname} {'(verified) ' if self.verified_at else ''}: " \
               f"{self.email} "

    @staticmethod
    def get_count() -> int:
        """Returns the number of verified signatures."""
        return Signature.objects.filter(verified_at__isnull=False).count()

    @staticmethod
    def mark_email_as_verified(email: str, date: datetime):
        """Mark email as verified."""
        try:
            signature = Signature.objects.get(email=email)
        except Signature.DoesNotExist:
            return False

        signature.verified_at = date
        signature.save()

        return True


class EmailOffset(models.Model):
    """Stores the last offset of events fetched by get_delivered_emails."""
    created_at = models.DateTimeField(default=timezone.now)
    offset = models.IntegerField(default=0, db_index=True)

    @staticmethod
    def get_max_offset() -> int:
        """Return the maximum offset stored in the table."""
        result = EmailOffset.objects.aggregate(Max('offset'))['offset__max']

        if result is None:
            return 0
        else:
            return result
