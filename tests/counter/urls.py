from django.urls import reverse


def get_pull_up_counter_list_url(pullupbar_id: int) -> str:
    return reverse(
        'pullupbars:pullupbars-counter-list',
        kwargs={'pullupbar_pk': pullupbar_id},
    )


def get_pull_up_counter_detail_url(pullupbar_id: int, counter_id: int) -> str:
    return reverse(
        'pullupbars:pullupbars-counter-detail',
        kwargs={'pullupbar_pk': pullupbar_id, 'pk': counter_id}
    )


def get_dip_counter_list_url(dipstation_id: int) -> str:
    return reverse(
        'dipstations:dipstations-counter-list',
        kwargs={'dipstation_pk': dipstation_id},
    )


def get_dip_counter_detail_url(dipstation_id: int, counter_id: int) -> str:
    return reverse(
        'dipstations:dipstations-counter-detail',
        kwargs={'dipstation_pk': dipstation_id, 'pk': counter_id}
    )
