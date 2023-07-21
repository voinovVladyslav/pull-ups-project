from django.urls import reverse


def get_pull_up_counter_list_url(bar_id):
    return reverse('bars:bars-pull-up-counter-list', kwargs={'pk': bar_id})


def get_pull_up_counter_detail_url(bar_id, counter_id):
    return reverse('bars:bars-pull-up-counter-detail', kwargs={'pk': bar_id})
