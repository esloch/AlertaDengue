import pytest
from AlertaDengue.ad_main import settings


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'db.example.com',
        'NAME': 'external_db',
    }
