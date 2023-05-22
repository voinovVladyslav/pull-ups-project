from django.urls import reverse


TAG_LIST_URL = reverse('tag:tag-list')


def get_tags_detail_url(id):
    return reverse('tag:tag-detail', kwargs={'pk': id})
