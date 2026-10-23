from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, Subject_Info_TypeView, SubjectView, AssignmentView, ListSubjectView, ListAssignmentView, ListSubject_Info_TypeView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('Subject/', ListSubjectView.as_view(), name='ListSubjectView'),
    path('Subject/<int:pk>/', SubjectView.as_view(), name='SubjectView'),
    path('Subject_Info/', ListSubject_Info_TypeView.as_view(), name='List_Subject_Info'),
    path('Subject_Info/<int:pk>/', Subject_Info_TypeView.as_view(), name='Subject_Info'),
    path('Assignment/', ListAssignmentView.as_view(), name='ListAssignmentView'),
    path('Assignment/<int:pk>/', AssignmentView.as_view(), name='AssignmentView'),
]

'hi'