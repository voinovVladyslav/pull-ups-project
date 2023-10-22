from django.urls import reverse


CREATE_USER_URL = reverse('user:create')
LOGIN_USER_URL = reverse('user:token')
STATS_URL = reverse('user:stats')
ME_URL = reverse('user:me')
