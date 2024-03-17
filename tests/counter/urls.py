from django.urls import reverse


def get_pull_up_counter_list_url(bar_id):
    return reverse(
        'pullupbars:pullupbars-counter-list', kwargs={'pullupbar_pk': bar_id}
    )


def get_pull_up_counter_detail_url(bar_id, counter_id):
    return reverse(
        'pullupbars:pullupbars-counter-detail',
        kwargs={'pullupbar_pk': bar_id, 'pk': counter_id}
    )
