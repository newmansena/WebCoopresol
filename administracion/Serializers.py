from pyexpat import model
from rest_framework.serializers import ModelSerializer
from inicio.models import Contactos

class SalaSerializer(ModelSerializer):
    class Meta:
        model= Contactos
        fields='__all__'
