from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import PhotoTest, Article, Subject_Info_Type, Subject, Assignment, Message, ChatMembership, Chat
from .serializers import PhotoTestSerializer, Subject_Info_TypeSerializer, SubjectSerializer, AssignmentSerializer, MessageSerializer, ChatMembershipSerializer, ChatSerializer
from .serializers import ArticleSerializer, AddMemberSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from django.db import transaction
from rest_framework.pagination import CursorPagination
from django.utils import timezone
import uuid
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


User = get_user_model()
class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '').strip()

        if len(query) < 2:
            return User.objects.none()

        print(self.request.user.pk)

        return (
            User.objects
            .filter(is_active=True)
            .exclude(pk=self.request.user.pk)
            .filter(
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
            ).order_by('username')
        )




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













class MessageCursorPagination(CursorPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100
    ordering = "-created_at"


class ChatView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "chat_id" #How does lookup_field work?

    def get_queryset(self):
        return (
            Chat.objects.filter(members=self.request.user)
            .prefetch_related("members") #how does prefetch work?
        )

    def perform_update(self, serializer):
        if serializer.instance.is_dm: #shouldn't this check to see if the message content itself is being updated?
            raise PermissionDenied("Direct messages cannot be renamed.")
        serializer.save() #when do you save a serializer at the end of a function?


class ListChatView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Chat.objects.filter(members=self.request.user)
            .prefetch_related("members")
            .order_by("-updated_at")
        )

    @transaction.atomic
    def perform_create(self, serializer): #what is the serializer in this case?
        chat = serializer.save() #Why are we saving a serializer and where is it finding this serializer
        ChatMembership.objects.create(chat=chat, user=self.request.user, last_read_at=timezone.now(),)


class ChatMembershipView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ChatMembership.objects.all()
    serializer_class = ChatMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ChatMembership.objects.filter(user=self.request.user)
            .select_related("chat", "user") #used for single-object relationships like foreignKey or OneToOneField relationships
        )


class ListChatMembershipView(generics.ListCreateAPIView):
    queryset = ChatMembership.objects.all()
    serializer_class = ChatMembershipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            ChatMembership.objects.filter(user=self.request.user)
            .select_related("chat", "user")
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddMemberSerializer
        return ChatMembershipSerializer
    


class MessageView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "message_id"


    def get_queryset(self):
        return (
            Message.objects.filter(chat__members=self.request.user)
            .select_related("creator", "chat")
        )

    def perform_update(self, serializer):
        if serializer.instance.creator_id != self.request.user.id:
            raise PermissionDenied("You can only edit your own messages.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.creator_id != self.request.user.id: #why is it creator ID and not creator like the model says or creator__id
            raise PermissionDenied("You can only delete your own messages.")
        instance.delete()


class ListMessageView(generics.ListCreateAPIView):
    
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessageCursorPagination

    def get_queryset(self):
        chat_id = self.request.query_params.get("chat_id")
        if not chat_id:
            raise ValidationError({"chat_id": "This query parameter is required."})
        try:
            uuid.UUID(chat_id)
        except ValueError:
            raise ValidationError({"chat_id": "Must be a valid UUID."})

        if not ChatMembership.objects.filter(
            chat__chat_id=chat_id, user=self.request.user
        ).exists():
            raise NotFound("Chat not found.")

        return Message.objects.filter(chat__chat_id=chat_id).select_related("creator", "chat")
    
    @transaction.atomic
    def perform_create(self, serializer):
        chat = serializer.validated_data["chat"]
        now = timezone.now()

        updated = ChatMembership.objects.filter(
            chat=chat,
            user=self.request.user,
        ).update(last_read_at=now)

        if not updated:
            raise PermissionDenied("You are not a member of this chat.")

        serializer.save(creator=self.request.user)
        Chat.objects.filter(pk=chat.pk).update(updated_at=now)




# class ExampleMultiView(generics.ListCreateAPIView):
#     serializer_class = MessageLifecycleSerializer
#     permission_classes = [IsAuthenticated]

#     # 1. Runs first to check if user is allowed to hit this endpoint at all
#     def check_permissions(self, request):
#         super().check_permissions(request)
#         # ACCESS: request.user, request.method, request.query_params, self.kwargs
#         # ACCESS (also): request.headers, request.data, self.request, self.args
#         if request.user.is_banned:
#             raise PermissionDenied("Your account is suspended.")

#     # 2. Runs on GET to decide which database rows are visible
#     def get_queryset(self):
#         # ACCESS:
#         # - self.request.user (logged-in user)
#         # - self.request.query_params.get("...") (URL ?key=value parameters)
#         # - self.kwargs["..."] (variables captured in urls.py like /chats/<uuid:chat_id>/)
#         # - self.request.method (HTTP verb)
#         # - self.request.headers (request headers)
#         chat_id = self.request.query_params.get("chat_id")
#         return (
#             Message.objects.filter(chat__chat_id=chat_id, chat__members=self.request.user)
#             .select_related("creator", "chat")
#         )

#     # 3. Dynamically choose which serializer to use
#     def get_serializer_class(self):
#         # ACCESS: self.request.method, self.request.user
#         if self.request.method == "POST":
#             return MessageLifecycleSerializer
#         return ReadOnlyMessageSerializer

#     # 4. Inject extra variables into serializer's self.context
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         # ACCESS: anything on self or self.request
#         # ACCESS (context keys from super()): context["request"], context["view"], context["format"]
#         # ACCESS (also): self.request.headers, self.request.user
#         context["is_mobile"] = self.request.headers.get("User-Agent") == "MobileApp"
#         return context

#     # 5. Runs on POST right before writing to the database
#     def perform_create(self, serializer):
#         # ACCESS:
#         # - serializer.validated_data["chat"] (pre-save validated data)
#         # - self.request.user
#         # ACCESS (also): serializer.validated_data (full cleaned dict),
#         #   serializer.initial_data (raw unvalidated input), self.kwargs
#         # Passing creator=... injects it directly into validated_data inside serializer.create()
#         message = serializer.save(creator=self.request.user)
#         # ACCESS post-save: 'message' is now the saved database object with message.id
#         # ACCESS (also): message.id (database primary key), message.message_id (UUID field)
#         print(f"Saved message {message.message_id}")




# class SingleMessageLifecycleView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = MessageLifecycleSerializer
#     permission_classes = [IsAuthenticated]
    
#     # Tells DRF which model column matches the URL variable (defaults to 'pk')
#     lookup_field = "message_id"
#     # Optional: name of the variable in urls.py if different from lookup_field
#     lookup_url_kwarg = "message_id"

#     # 1. Narrows down the pool of allowed records before looking up the single item
#     def get_queryset(self):
#         # ACCESS: self.request.user, self.kwargs
#         # ACCESS (also): self.kwargs["message_id"] (UUID from URL), self.request.method
#         # If the message doesn't belong to one of the user's chats, DRF automatically returns 404
#         return (
#             Message.objects.filter(chat__members=self.request.user)
#             .select_related("creator", "chat")
#         )

#     # 2. Fetches the exact single object from get_queryset() using lookup_field
#     def get_object(self):
#         # Usually you don't need to override this, unless you want custom lookup logic
#         # ACCESS: self.kwargs["message_id"] (the UUID captured from the URL)
#         # ACCESS (also): self.request (full request object)
#         obj = super().get_object()
#         # ACCESS (also): obj (the fetched Message), obj.message_id, obj.id, obj.chat, obj.creator
        
#         # Example: run object-level permission checks right after fetching it
#         self.check_object_permissions(self.request, obj)
#         return obj

#     # 3. Runs on PUT or PATCH right before writing updates to the database
#     def perform_update(self, serializer):
#         # ACCESS:
#         # - serializer.instance: the EXISTING Message object currently in the database
#         # - serializer.validated_data: dictionary of NEW values the user wants to save
#         # - self.request.user: the logged-in user
#         # ACCESS (also): serializer.instance.creator_id (owner ID),
#         #   serializer.instance.text (current text before the change),
#         #   serializer.initial_data (raw unvalidated input)
        
#         if serializer.instance.creator_id != self.request.user.id:
#             raise PermissionDenied("You can only edit your own messages.")

#         # Example: compare old text vs new text before saving
#         old_text = serializer.instance.text
#         new_text = serializer.validated_data.get("text", old_text)
        
#         # You MUST call serializer.save() here, otherwise changes are never written to the DB
#         updated_message = serializer.save()
#         # ACCESS post-save: updated_message (saved object), updated_message.text (new text)
#         print(f"Updated '{old_text}' to '{updated_message.text}'")

#     # 4. Runs on DELETE right before removing the row from the database
#     def perform_destroy(self, instance):
#         # ACCESS:
#         # - instance: the exact Message object fetched by get_object()
#         # - self.request.user: the logged-in user
#         # ACCESS (also): instance.creator_id, instance.message_id, instance.id,
#         #   instance.text, instance.chat (all fields on the row before deletion)
        
#         if instance.creator_id != self.request.user.id:
#             raise PermissionDenied("You can only delete your own messages.")

#         # You MUST call instance.delete() (or do a soft-delete like instance.is_deleted = True; instance.save())
#         instance.delete()













































    #   request = self.request
    #     print("method:", request.method)
    #     print("path:", request.path)
    #     print("user:", request.user)
    #     print("auth:", request.auth)
    #     print("query params:", request.query_params)   # same as request.GET
    #     print("data:", request.data)   
    #     # for m in Message.objects.filter(creator=self.request.user):
    #     #     print('_____________________________________________',m.__dict__['text'])
    #     print(serializer.validated_data['chat'].members.filter(id=self.request.user.pk).exists())



