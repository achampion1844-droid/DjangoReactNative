from rest_framework import serializers
from .models import Article, Subject, Subject_Info_Type, Assignment
from django.contrib.auth.models import User

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

class UserSerializerd(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'created_at', 'id']


class AssignmentSerializer(serializers.ModelSerializer):
    # subjects = SubjectSerializer(many=True, read_only=True)
    class Meta:
        model = Assignment
        fields = [
            'user', 
            'assignment_ID', 
            'assignment_description', 
            'assignment_name','date_added', 
            'date_started', 
            'remaining_study_sessions', 
            'subjects',
            'subject',
            'icon', 
            'is_Completed'
        ]

class Subject_Info_TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject_Info_Type
        fields = [
            'icon',
            'subject_name',
            'num_sub_study_items',
            'id',
        ]