from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import SearchLog

class SearchLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SearchLog
        fields = ['city_description', 'date_search', 'log']

