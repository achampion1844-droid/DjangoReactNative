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

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ListSubjectView(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)





class AssignmentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects.filter(user=self.request.user)


class ListAssignmentView(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Assignment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class Subject_Info_TypeView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject_Info_Type.objects.all()
    serializer_class = Subject_Info_TypeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
            return Subject_Info_Type.objects.filter(subject_name__user=self.request.user)


class ListSubject_Info_TypeView(generics.ListCreateAPIView):
    queryset = Subject_Info_Type.objects.all()
    serializer_class = Subject_Info_TypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subject_Info_Type.objects.filter(subject_name__user=self.request.user) #subject_name is the name for the subject in Subject_info_types and it points to the Subject model and in the subject model we have the user row
    
    def perform_create(self, serializer):
        serializer.save()





class PhotoTestView(generics.ListCreateAPIView):
    queryset = PhotoTest.objects.all()
    serializer_class = PhotoTestSerializer
    permission_classes = [IsAuthenticated]
