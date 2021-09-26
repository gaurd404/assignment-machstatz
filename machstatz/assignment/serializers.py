from rest_framework import serializers


class InputSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    production_A = serializers.BooleanField()
    production_B = serializers.BooleanField()


class InputSerializer2(serializers.Serializer):
    time = serializers.DateTimeField()
    runtime = serializers.IntegerField()
    downtime = serializers.IntegerField()


class InputSerializer3(serializers.Serializer):
    time = serializers.DateTimeField()
    id = serializers.CharField()
    state = serializers.BooleanField()
    belt1 = serializers.IntegerField()
    belt2 = serializers.IntegerField()
