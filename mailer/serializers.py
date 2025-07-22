from rest_framework import serializers

class EmailSerializer(serializers.Serializer):
    class Meta:
        fields = '__all__'