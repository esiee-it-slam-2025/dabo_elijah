from rest_framework import serializers
from .models import Stadium

class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'  # On récupère tous les champs du modèle Stadium
