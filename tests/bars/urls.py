from django.urls import reverse


BARS_LIST_URL = reverse('bars:bars-list')


def get_bars_detail_url(id):
    return reverse('bars:bars-detail', kwargs={'pk': id})
