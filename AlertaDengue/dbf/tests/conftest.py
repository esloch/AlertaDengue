import os
import psycopg2
import sqlalchemy
from sqlalchemy import create_engine



import pytest
from django.db import connections
from django.conf import settings
from AlertaDengue.ad_main import settings

import pdb; pdb.set_trace()
PSQL_URI = "postgresql://{}:{}@{}:{}/{}".format(
    settings.PSQL_USER,
    settings.PSQL_PASSWORD,
    settings.PSQL_HOST,
    settings.PSQL_PORT,
    'postgres',
)


def run_sql(sql):
    conn = create_engine(PSQL_URI)
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(sql)


@pytest.fixture(scope='module')
def django_db_setup():

    db_name = settings.DATABASES['infodengue']['NAME']
    run_sql('DROP DATABASE IF EXISTS {}'.format(db_name))
    run_sql("CREATE DATABASE {} WITH OWNER dengueadmin ENCODING 'utf-8'".format(db_name))
    os.system('DJANGO_SETTINGS_MODULE=AlertaDengue.ad_main.test_settings ENV_FILE=.env_staging python AlertaDengue/manage.py migrate --database=infodengue')
