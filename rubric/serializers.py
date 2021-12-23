from rest_framework import serializers
from .models import Rubric

class RubricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rubric
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.template = validated_data.get('template', instance.template)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.upload_time = validated_data.get('upload_time', instance.upload_time)
        instance.assignment_name = validated_data.get('assignment_name', instance.assignment_name)
        instance.save()
        return instance