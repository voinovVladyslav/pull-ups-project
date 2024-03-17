from django.urls import reverse


BARS_LIST_URL = reverse('pullupbars:pullupbars-list')
FAVORITE_BARS = reverse('pullupbars:pullupbars-favorites')
ADD_FAVORITE_BARS = reverse('pullupbars:pullupbars-favorites-add')
REMOVE_FAVORITE_BARS = reverse('pullupbars:pullupbars-favorites-remove')


def get_bars_detail_url(id):
    return reverse('pullupbars:pullupbars-detail', kwargs={'pk': id})
