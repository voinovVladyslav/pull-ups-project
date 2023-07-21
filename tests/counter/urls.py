from django.urls import reverse


def get_pull_up_counter_list_url(bar_id):
    return reverse('bars:bars-counter-list', kwargs={'bar_pk': bar_id})


def get_pull_up_counter_detail_url(bar_id, counter_id):
    return reverse(
        'bars:bars-counter-detail',
        kwargs={'bar_pk': bar_id, 'pk': counter_id}
    )
