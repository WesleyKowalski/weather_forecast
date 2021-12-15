import datetime

from django.shortcuts import render
from rest_framework import viewsets
from core.serializer import SearchLogSerializer
from core.models import SearchLog
from rest_framework.response import Response
from core.domain import CommunicationWithServerWeatherForecast, Utils
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from datetime import timedelta

class SearchLogViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if ('data_log_min' in request.query_params) or ('data_log_max' in request.query_params):
            #Se for preenchido algum parâmetro de data, então valida se os dois estão preenchidos.
            if not('data_log_min' in request.query_params and 'data_log_max' in request.query_params):
                return Response(status=200, data={
                    "error": "Para usar parâmetros de data, deverá ser usado os dois parâmetros data_log_min para data e hora inicial, e data_log_max para data e hora final"})

            try:
                data_min = request.query_params['data_log_min']
                data_min = datetime.datetime.strptime(data_min, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)

                data_max = request.query_params['data_log_max']
                data_max = datetime.datetime.strptime(data_max, '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)

                log = SearchLog.objects.filter(date_search__gte=data_min, date_search__lte=data_max)
                log_serializer = SearchLogSerializer(log, many=True)
                return Response(status=200, data=log_serializer.data)

            except Exception as e:
                return Response(status=200, data={
                    "error": "Erro ao processar parâmetros de data(data_log_min ou data_log_max)",
                    "exception": str(e)
                })

        log = SearchLog.objects.all().order_by("date_search")
        log_serializer = SearchLogSerializer(log, many=True)
        return Response(status=200, data=log_serializer.data)

class ForecastForCity(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.query_params['city']:
            response = CommunicationWithServerWeatherForecast().get_forecast_for_city(request.query_params['city'])
            log = SearchLog(city_description=request.query_params['city'],
                            date_search=datetime.datetime.now(),
                            log=str(response))
            log.save()
            return Response(status=200, data=response)
        else:
            return Response(status=500, data="Informe uma cidade válida")