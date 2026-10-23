from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Article, Subject_Info_Type, Subject, Assignment
from .serializers import Subject_Info_TypeSerializer, SubjectSerializer, AssignmentSerializer
from .serializers import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class SubjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class ListSubjectView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class AssignmentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class ListAssignmentView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class Subject_Info_TypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject_Info_Type.objects.all()
    serializer_class = Subject_Info_TypeSerializer

class ListSubject_Info_TypeView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
