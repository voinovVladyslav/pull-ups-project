from django.urls import reverse


CREATE_USER_URL = reverse('user:create')
LOGIN_USER_URL = reverse('user:token')
ME_URL = reverse('user:me')
