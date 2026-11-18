from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import timedelta
from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subject_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"{self.name}-{self.user}"


def default_internals():
    return {0:[False], 1:[False],3:[False],7:[False],14:[False],28:[False],84:[False]}


class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment_description = models.CharField(max_length=60)
    assignment_name = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True)
    date_started = models.DateField(auto_now_add=True)
    remaining_study_sessions = models.PositiveIntegerField(default=5)
    subject = models.ForeignKey(Subject, related_name='subjects', on_delete=models.CASCADE)
    icon = models.ImageField(upload_to='assignment_icons/', blank=True)
    is_Completed = models.BooleanField(default=False)

    intervals = models.JSONField(default=default_internals)


    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
    
    def __str__(self):
        return self.assignment_name

    def date_for(self, days):
        print(days)
        return self.date_started + timedelta(days=days)


class Subject_Info_Type(models.Model):
    icon = models.ImageField(upload_to='assignment_icons/', blank=True)
    subject_name = models.ForeignKey(Subject, related_name='subject', on_delete=models.CASCADE)
    num_sub_study_items = models.PositiveIntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)



class PhotoTest(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='PhotoTest/')





def new_id():
    return uuid.uuid4().hex

class Chat(models.Model):
    chat_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    is_dm = models.BooleanField(default=True)
    dm_key = models.CharField(max_length=64, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ChatMembership", related_name="chats",)

    def __str__(self):
        return str(self.chat_id) or str(self.chat_id)

class ChatMembership(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    last_read_at = models.DateTimeField(null=True, blank=True)  # drives isSeen

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["chat", "user"], name="unique_chat_membership")
        ]

class Message(models.Model):
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, db_index=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="messages")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['chat', 'created_at'])
        ]
