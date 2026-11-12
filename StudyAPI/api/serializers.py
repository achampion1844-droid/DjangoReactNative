from rest_framework import serializers
from .models import Article, Subject, Subject_Info_Type, Assignment, PhotoTest
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
        fields = ['name', 'description', 'created_at', 'subject_ID']
        read_only_fields = ['user']


class AssignmentSerializer(serializers.ModelSerializer):
    # use multiple=True only if it is a many to many relationship
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), #primary key related fields looks up the uuid primary key in all the subject objects, validates it exists and returns the subject objects with that primary key
        source='subject', #saves the subject object just gotten to the subject field in the assignment model
        write_only=True #means only post or put requests need this field
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # extra_dates = serializers.SerializerMethodField()




    class Meta:
        model = Assignment
        fields = [
            'user', 
            'assignment_ID', 
            'assignment_description', 
            'assignment_name','date_added', 
            'date_started', 
            'remaining_study_sessions', 
            'subject',
            'subject_id', 
            'icon', 
            'is_Completed',
            # 'extra_dates',
            'intervals',
        ]

    def validate_intervals(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Intervals must be an object.")
        for key, val in value.items():
            if not str(key).isdigit():
                raise serializers.ValidationError(
                    f"Interval key '{key}' must be a whole number of days."
                )
            if not isinstance(val, list) or not val:
                raise serializers.ValidationError(
                    f"Interval '{key}' must be a non-empty list."
                )
        return value

    # def get_extra_dates(self, obj):
    #     result = {}
    #     for d, value in obj.intervals.items():
    #         try:
    #             days = int(d)
    #         except (TypeError, ValueError):
    #             continue
    #         result[f"{days}_days"] = [obj.date_for(days), value[0]]
    #     return result


class Subject_Info_TypeSerializer(serializers.ModelSerializer):
    subject_name = SubjectSerializer(read_only=True)
    subject_details = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='subject_name')
    
    class Meta:
        model = Subject_Info_Type
        fields = [
            'icon',
            'subject_name',
            'num_sub_study_items',
            'id',
            'subject_details',
        ]


class PhotoTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoTest
        fields = [
            'name',
            'image',
        ]