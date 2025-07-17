from django.utils import timezone


def safe_aware(dt):
    if timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt
