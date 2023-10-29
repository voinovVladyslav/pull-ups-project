from django.urls import reverse


NOTIFICATIONS_URL = reverse('notifications:notifications-list')


def get_notification_detail_url(pk):
    return reverse('notifications:notifications-detail', kwargs={'pk': pk})
