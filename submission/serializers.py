from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.x = validated_data.get('x', instance.x)
        instance.y = validated_data.get('y', instance.y)
        instance.text = validated_data.get('text', instance.text)
        instance.sectionName = validated_data.get('sectionName', instance.sectionName )
        instance.points = validated_data.get('points', instance.points)
        instance.commentArray = validated_data.get('commentArray', instance.commentArray)
        instance.save()
        return instance
