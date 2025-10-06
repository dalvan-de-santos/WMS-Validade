from celery import shared_task
from django.utils import timezone
from .models import Batch

@shared_task
def check_expiry_and_notify(threshold_days=7):
    today = timezone.localdate()
    near = Batch.objects.filter(expiry_date__lte=today + timezone.timedelta(days=threshold_days))
    expired = Batch.objects.filter(expiry_date__lt=today)
    # TODO: Implement notification logic (e.g., send emails to admins)

    return {"near_count": near.count(), "expired_count": expired.count()}