from django.conf.urls import re_path

# local
from .views import (
    NotificationReducedCSV_View,
    AlertCityView,
    EpiYearWeekView,
    InfoStateView,
)


app_name = "api"

__geocode = r'(?P<geocodigo>\d{7})'  # Variable endpoint

urlpatterns = [
    re_path(
        r'^notif_reduced$',
        NotificationReducedCSV_View.as_view(),
        name='notif_reduced',
    ),
    re_path(r'^alertcity', AlertCityView.as_view(), name='alertcity'),
    re_path(
        r'^epi_year_week$', EpiYearWeekView.as_view(), name='epi_year_week'
    ),
    re_path(
        r'^app_info_state$', InfoStateView.as_view(), name='app_info_state'
    ),
]
