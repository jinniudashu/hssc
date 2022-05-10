from rest_framework import serializers
from icpc.models import *

class IcpcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc
        fields = 'iname'