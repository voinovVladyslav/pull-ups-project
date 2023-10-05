from django.urls import reverse


ACHIEVEMENTS_LIST_URL = reverse('achievements:achievements-list')
RESET_ACHIEVEMENTS_URL = reverse('achievements:achievements-reset-all')


def get_achievements_detail_url(id: int):
    return reverse('achievements:achievements-detail', kwargs={'pk': id})


def get_reset_achievement_detail_url(id: int):
    return reverse('achievements:achievements-reset-single', kwargs={'pk': id})
