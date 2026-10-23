from django.db import models
from django.contrib.auth.models import User
import uuid

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# class date_obj_type(models.Model):

#     MONTHS = [
#         ('Jan', 'Jan'),
#         ('Feb', 'Feb'),
#         ('Mar', 'Mar'),
#         ('Apr', 'Apr'),
#         ('May', 'May'),
#         ('Jun', 'Jun'),
#         ('Jul', 'Jul'),
#         ('Aug', 'Aug'),
#         ('Sep', 'Sep'),
#         ('Oct', 'Oct'),
#         ('Nov', 'Nov'),
#         ('Dec', 'Dec'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     date = models.PositiveIntegerField()
#     month = models.CharField(max_length=4, choices=MONTHS)
#     year = models.PositiveIntegerField()
#     last_day_of_month = models.PositiveIntegerField()
#     full_date = models.DateField()



class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_ID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment_description = models.CharField(max_length=60)
    assignment_name = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True)
    date_started = models.DateField()
    remaining_study_sessions = models.PositiveIntegerField(default=5)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    icon = models.ImageField(upload_to='assignment_icons/', blank=True)
    is_Completed = models.BooleanField(default=False)


    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
    def __str__(self):
        return self.assignment_name


class Subject_Info_Type(models.Model):
    icon = models.ImageField(upload_to='assignment_icons/', blank=True)
    subject_name = models.ForeignKey(Subject, on_delete=models.PROTECT)
    num_sub_study_items = models.PositiveIntegerField()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.subject_name




