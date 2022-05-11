from rest_framework import serializers
from .models import *

class Icpc1_register_loginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc1_register_logins
        fields = 'iname'

class Icpc2_reservation_investigationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc2_reservation_investigations
        fields = 'iname'

class Icpc3_symptoms_and_problemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc3_symptoms_and_problems
        fields = 'iname'

class Icpc4_physical_examination_and_testsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc4_physical_examination_and_tests
        fields = 'iname'

class Icpc5_evaluation_and_diagnosesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc5_evaluation_and_diagnoses
        fields = 'iname'

class Icpc6_prescribe_medicinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc6_prescribe_medicines
        fields = 'iname'

class Icpc7_treatmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc7_treatments
        fields = 'iname'

class Icpc8_other_health_interventionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc8_other_health_interventions
        fields = 'iname'

class Icpc9_referral_consultationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc9_referral_consultations
        fields = 'iname'

class Icpc10_test_results_and_statisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icpc10_test_results_and_statistics
        fields = 'iname'
