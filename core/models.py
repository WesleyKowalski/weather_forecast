from django.db import models

class SearchLog(models.Model):
    city_description = models.CharField(max_length=100)
    date_search = models.DateTimeField(null=False)
    log = models.CharField(max_length=50000)