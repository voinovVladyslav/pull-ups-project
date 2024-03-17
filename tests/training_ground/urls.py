from django.urls import reverse


TG_LIST_URL = reverse('training_ground:training-ground-list')


def get_training_ground_add_favorite_url(id: int) -> str:
    return reverse(
        'training_ground:training-ground-favorites-add', kwargs={'pk': id}
    )


def get_training_ground_remove_favorite_url(id: int) -> str:
    return reverse(
        'training_ground:training-ground-favorites-remove', kwargs={'pk': id}
    )
