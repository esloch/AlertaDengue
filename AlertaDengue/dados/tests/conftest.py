import pytest
from AlertaDengue.ad_main import settings


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': '172.19.0.2',
        'NAME': 'dengue',
        'PORT': '25432'
    }
