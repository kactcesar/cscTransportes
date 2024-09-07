
from rest_framework import serializers
from.models import*


class viagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosViagem
        fields = '__all__'  