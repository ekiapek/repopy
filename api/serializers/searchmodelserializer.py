from rest_framework import serializers
from api.models import SearchModel

class SearchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchModel