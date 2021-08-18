from rest_framework import serializers
from .models import Submission, Page, Comment

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.students = validated_data.get('students', instance.students)
        instance.template = validated_data.get('template', instance.template)
        instance.submitted_url = validated_data.get('url', instance.submitted_url)
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.semester = validated_data.get('semester', instance.semester)
        instance.upload_time = validated_data.get('upload_time', instance.upload_time)
        instance.export_id = validated_data.get('export_id', instance.export_id)
        instance.matched = validated_data.get('matched', instance.matched)
        instance.save()
        return instance

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url', instance.url)
        instance.name = validated_data.get('name', instance.name)
        instance.html = validated_data.get('html', instance.html)
        instance.save()
        return instance

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
