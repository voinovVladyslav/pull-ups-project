from django.urls import reverse


BARS_LIST_URL = reverse('bars:bars-list')
FAVORITE_BARS = reverse('bars:favorites')
ADD_FAVORITE_BARS = reverse('bars:favorites-add')
REMOVE_FAVORITE_BARS = reverse('bars:favorites-remove')


def get_bars_detail_url(id):
    return reverse('bars:bars-detail', kwargs={'pk': id})
