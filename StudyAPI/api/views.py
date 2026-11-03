from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import PhotoTest, Article, Subject_Info_Type, Subject, Assignment
from .serializers import PhotoTestSerializer, Subject_Info_TypeSerializer, SubjectSerializer, AssignmentSerializer
from .serializers import ArticleSerializer
from rest_framework.permissions import IsAuthenticated


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]

class SubjectView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

class ListSubjectView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]


class AssignmentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

class ListAssignmentView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]


class Subject_Info_TypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject_Info_Type.objects.all()
    serializer_class = Subject_Info_TypeSerializer
    permission_classes = [IsAuthenticated]

class ListSubject_Info_TypeView(generics.ListCreateAPIView):
    queryset = Subject_Info_Type.objects.all()
    serializer_class = Subject_Info_TypeSerializer
    permission_classes = [IsAuthenticated]


class PhotoTestView(generics.ListCreateAPIView):
    queryset = PhotoTest.objects.all()
    serializer_class = PhotoTestSerializer
    permission_classes = [IsAuthenticated]
