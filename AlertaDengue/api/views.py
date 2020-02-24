from collections import defaultdict
from datetime import datetime

from django.http import HttpResponse
from django.views.generic.base import View


# local
from dados import dbdata
from dados.dbdata import variation_p
from .db import NotificationQueries, STATE_NAME, AlertCity, MRJ_GEOCODE
from dados.episem import episem

import json


class _GetMethod:
    """

    """

    def _get(self, param, default=None, cast=None, error_message=None):
        """

        :param param:
        :param default:
        :return:
        """
        if error_message is not None and param not in self.request.GET:
            raise Exception(error_message)

        result = (
            self.request.GET[param] if param in self.request.GET else default
        )

        return result if cast is None or result is None else cast(result)


class NotificationReducedCSV_View(View, _GetMethod):
    """

    """

    _state_name = STATE_NAME

    request = None

    def get(self, request):
        """

        :param kwargs:
        :return:
        """
        self.request = request

        state_name = self._get('state_abv', default='').upper()

        if state_name not in self._state_name:
            return HttpResponse(
                'ERROR: The parameter state_abv not found. '
                + 'This parameter must have 2 letters (e.g. RJ).',
                content_type="text/plain",
                status=404,
            )

        uf = self._state_name[state_name]

        chart_type = self._get('chart_type')

        notifQuery = NotificationQueries(
            uf=uf,
            disease_values=self._get('diseases'),
            age_values=self._get('ages'),
            gender_values=self._get('genders'),
            city_values=self._get('cities'),
            initial_date=self._get('initial_date'),
            final_date=self._get('final_date'),
        )

        result = None

        if chart_type == 'disease':
            result = notifQuery.get_disease_dist().to_csv()
        elif chart_type == 'age':
            result = notifQuery.get_age_dist().to_csv()
        elif chart_type == 'age_gender':
            result = notifQuery.get_age_gender_dist().to_csv()
        elif chart_type == 'age_male':
            result = notifQuery.get_age_male_dist().to_csv()
        elif chart_type == 'age_female':
            result = notifQuery.get_age_female_dist().to_csv()
        elif chart_type == 'gender':
            result = notifQuery.get_gender_dist().to_csv()
        elif chart_type == 'period':
            result = notifQuery.get_period_dist().to_csv(
                date_format='%Y-%m-%d'
            )
        elif chart_type == 'epiyears':
            # just filter by one disease
            result = notifQuery.get_epiyears(uf, self._get('disease')).to_csv()
        elif chart_type == 'total_cases':
            result = notifQuery.get_total_rows().to_csv()
        elif chart_type == 'selected_cases':
            result = notifQuery.get_selected_rows().to_csv()

        return HttpResponse(result, content_type="text/plain")


class AlertCityView(View, _GetMethod):
    """

    """

    request = None

    def get(self, request):
        self.request = request
        format = ''

        try:
            disease = self._get(
                'disease', error_message='Disease sent is empty.'
            ).lower()
            geocode = self._get(
                'geocode', cast=int, error_message='GEO-Code sent is empty.'
            )
            format = self._get(
                'format', error_message='Format sent is empty.'
            ).lower()
            ew_start = self._get(
                'ew_start',
                cast=int,
                error_message='Epidemic start week sent is empty.',
            )
            ew_end = self._get(
                'ew_end',
                cast=int,
                error_message='Epidemic end week sent is empty.',
            )
            ey_start = self._get(
                'ey_start',
                cast=int,
                error_message='Epidemic start year sent is empty.',
            )

            ey_end = self._get(
                'ey_end',
                cast=int,
                error_message='Epidemic end year sent is empty.',
            )

            if format not in ['csv', 'json']:
                raise Exception(
                    'The output format available are: `csv` or `json`.'
                )

            eyw_start = ey_start * 100 + ew_start
            eyw_end = ey_end * 100 + ew_end

            if geocode == MRJ_GEOCODE:
                df = AlertCity.search_rj(
                    disease=disease, ew_start=eyw_start, ew_end=eyw_end
                )
            else:
                df = AlertCity.search(
                    geocode=geocode,
                    disease=disease,
                    ew_start=eyw_start,
                    ew_end=eyw_end,
                )
                # change all keys to lower case
                df.drop(
                    columns=['municipio_geocodigo', 'municipio_nome'],
                    inplace=True,
                )

            if format == 'json':
                result = df.to_json(orient='records')
            else:
                result = df.to_csv(index=False)
        except Exception as e:
            if format == 'json':
                result = '{"error_message": "%s"}' % e
            else:
                result = '[EE] error_message: %s' % e

        content_type = 'application/json' if format == 'json' else 'text/plain'

        return HttpResponse(result, content_type=content_type)


class EpiYearWeekView(View, _GetMethod):
    """
    JSON output
    """

    request = None

    def get(self, request):
        self.request = request
        output_format = 'json'

        try:
            epidate_s = self._get(
                'epidate', error_message='epidate sent is empty.'
            )

            epidate = datetime.strptime(epidate_s, '%Y-%m-%d')
            epi_year_week = episem(epidate, sep='')

            if output_format == 'json':
                result = json.dumps(
                    dict(
                        epi_year_week=epi_year_week,
                        epi_year=epi_year_week[:4],
                        epi_week=epi_year_week[4:],
                    )
                )
            else:
                result = '' % epi_year_week

        except Exception as e:
            if output_format == 'json':
                result = '{"error_message": "%s"}' % e
            else:
                result = '[EE] error_message: %s' % e

        content_type = (
            'application/json' if output_format == 'json' else 'text/plain'
        )

        return HttpResponse(result, content_type=content_type)


class InfoStateView(View, _GetMethod):

    _state_names = sorted(dbdata.STATE_NAME.values())
    _state_initials = {v: k for k, v in dbdata.STATE_NAME.items()}

    def get(self, request, *args, **kwargs):
        self.request = request
        output_format = 'json'

        # format = self._get(
        #     'format', error_message='Format sent is empty.'
        # ).lower()

        diseases = tuple(dbdata.CID10.keys())
        '''
        from dados.maps import get_city_info
        geocode = context['geocodigo']
        'state': city_info['uf'],
        city_info = get_city_info(geocode)
        'populacao': city_info['populacao'],

        '''
        # today
        last_se = {}

        case_series = defaultdict(dict)
        case_series_state = defaultdict(dict)

        count_cities = defaultdict(dict)
        current_week = defaultdict(dict)
        estimated_cases_next_week = defaultdict(dict)
        variation_to_current_week = defaultdict(dict)
        variation_4_weeks = defaultdict(dict)
        v1_week_fixed = defaultdict(dict)
        v1_4week_fixed = defaultdict(dict)

        notif_resume = dbdata.NotificationResume
        '''

        municipios, geocodigos = list(mundict.values()), list(mundict.keys())

        '''
        mundict = dict(dbdata.get_all_active_cities())
        # results[d] = dbdata.load_serie_cities(geocodigos, d)

        for d in diseases:
            case_series[d] = dbdata.get_series_by_UF(d)

            for s in self._state_names:
                df = case_series[d]  # alias
                df_state = df[df.uf == s]
                cases = df_state.casos_s.values

                # cases estimation
                cases_est = df_state.casos_est_s.values

                case_series_state[d][s] = cases[:-52]

                if d == 'dengue':
                    if not df_state.empty:
                        last_se[s] = df_state.tail(1).data.iloc[0]
                    else:
                        last_se[s] = ''

                count_cities[d][s] = notif_resume.count_cities_by_uf(s, d)
                current_week[d][s] = {
                    'casos': cases[-1] if cases.size else 0,
                    'casos_est': cases_est[-1] if cases_est.size else 0,
                }
                # estimated_cases_next_week[d][s] = int(0)
                v1 = 0 if not cases_est.size else cases_est[-2]
                v2 = 0 if not cases_est.size else cases_est[-1]

                v1_week_fixed[d][s] = v1 == 0 and v2 != 0

                variation_to_current_week[d][s] = variation_p(v1, v2)

                if cases_est.size < 55:
                    variation_4_weeks[d][s] = 0
                else:
                    v2 = cases_est[-4:-1].sum()
                    v1 = cases_est[-55:-52].sum()

                    v1_4week_fixed[d][s] = v1 == 0 and v2 != 0

                    variation_4_weeks[d][s] = variation_p(v1, v2)

        result = {
            'estado': self._state_initials,
            'municipios participantes': str(count_cities),
            'num_mun': len(mundict),
            'current_week': str(current_week),
            'estimated_cases_next_week': estimated_cases_next_week,
            'ultima atualização': {
                k: d.isoformat() for k, d in last_se.items()
            },
            'variação na semana': variation_to_current_week,
            'variação 4 semanas': variation_4_weeks,
            'case_series': {
                k: v.to_json('record') for k, v in case_series.items()
            },
        }
        # import pdb; pdb.set_trace()

        content_type = (
            'application/json' if output_format == 'json' else 'text/plain'
        )

        return HttpResponse(json.dumps(result), content_type=content_type)
        # json.dumps
