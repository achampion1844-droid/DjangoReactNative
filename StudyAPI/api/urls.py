from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, PhotoTestView, ArticleViewSet, Subject_Info_TypeView, SubjectView, AssignmentView, ListSubjectView, ListAssignmentView, ListSubject_Info_TypeView, ChatView, ListChatView, MessageView, ListMessageView, ChatMembershipView, ListChatMembershipView

# router = DefaultRouter()
# router.register(r'articles', ArticleViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('Subject/', ListSubjectView.as_view(), name='ListSubjectView'),
    path('Subject/<uuid:pk>/', SubjectView.as_view(), name='SubjectView'),
    path('Subject_Info/', ListSubject_Info_TypeView.as_view(), name='List_Subject_Info'),
    path('Subject_Info/<uuid:pk>/', Subject_Info_TypeView.as_view(), name='Subject_Info'),
    path('Assignment/', ListAssignmentView.as_view(), name='ListAssignmentView'),
    path('Assignment/<uuid:pk>/', AssignmentView.as_view(), name='AssignmentView'),

    path('Message/', ListMessageView.as_view(), name='list-messages'),
    path('Message/<uuid:message_id>/', MessageView.as_view(), name='message-detail'),
    path('Chat/', ListChatView.as_view(), name='list-chats'),
    path('Chat/<uuid:chat_id>/', ChatView.as_view(), name='chat-detail'),
    path('ChatMembership/', ListChatMembershipView.as_view(), name='list-chat-memberships'),
    path('ChatMembership/<int:pk>/', ChatMembershipView.as_view(), name='chat-membership-detail'),

    path('Users/', UserView.as_view(), name='list-users'),

    path('photo', PhotoTestView.as_view()),
]

